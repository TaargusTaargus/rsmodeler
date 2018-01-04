from os.path import sep
from json import load
from time import sleep
from utilities import column_names, load_json_from_url, query_to_array, replace_keys
from datetime import datetime

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
REQUEST_TIMER = 5
ROUTES_FILE_PATH = "configs" + sep + "routes"

def extract( routes=ROUTES_FILE_PATH, db=None, verbose=True ):
	
	if db:
		cursor = db.cursor()
		cursor.execute( """
			CREATE TABLE IF NOT EXISTS ITEM_SALES
				( itemid int, name text, date text, timestamp int, price int )
		""" )
		db.commit()

	api = load( open( ROUTES_FILE_PATH ) )

	catalog_template = api[ "base" ] + api[ "endpoints" ][ "catalog" ][ "url" ]
	catalog_keys = api[ "endpoints" ][ "catalog" ][ "keys" ]
	catalog_keys = dict( zip( catalog_keys, [ None ] * len( catalog_keys ) ) )

	graph_template = api[ "base" ] + api[ "endpoints" ][ "graph" ][ "url" ]
	graph_keys = api[ "endpoints" ][ "graph" ][ "keys" ]
	graph_keys = dict( zip( graph_keys, [ None ] * len( graph_keys ) ) )

	results = {}

	placeholders = api[ "placeholders" ]

	for letter in ALPHABET:
		catalog_keys[ "alpha" ] = letter
		catalog_keys[ "page" ] = 0	
		
		while True:
			catalog = replace_keys( catalog_template, placeholders, catalog_keys )
			catalog = load_json_from_url( catalog )

			if verbose:
				print( "catalog letter: " + catalog_keys[ "alpha" ]  +  ", page: " + str( catalog_keys[ "page" ] ) )

			if not catalog or not len( catalog ):
				break
				
			for item in catalog[ "items" ]:
		
				if verbose:
					print( "loading item: " + str( item[ "id" ] ) + " ..." )	
				graph_keys[ "item" ] = item[ "id" ]
				graph = replace_keys( graph_template, placeholders, graph_keys )
				graph = load_json_from_url( graph )

				if graph:
					for point in graph[ "daily" ]:
						if db:
							cursor.execute( 
								"INSERT INTO ITEM_SALES VALUES ( " +
								str( item[ "id" ] ) + ", '" + item[ "name" ].replace( "'", "''" ) + "', '" +
								datetime.fromtimestamp( int( int( point ) / 1000 ) ).strftime( "%Y-%m-%d %H:%M:%S" ) +
								"', " + str( point ) + ", " + str( graph[ "daily" ][ str( point ) ] ) + " )" 
							)
						results[ item[ 'id' ] ] = {
							"name": item[ "name" ],
							"date": datetime.fromtimestamp( int( int( point ) / 1000 ) ).strftime( "%Y-%m-%d %H:%M:%S" ),
							"timestamp": point,
							"price": graph[ "daily" ][ str( point ) ]
						}
					db.commit()
				else:
					print( "could not load graph on item: " + str( item[ 'id' ] ) )

				sleep( REQUEST_TIMER )

			catalog_keys[ "page" ] = catalog_keys[ "page" ] + 1
 
	return results


def transform( db ):

	cursor = None

	try:
		cursor = db.cursor()
	except:
		print( "could not load result set ..." )
		return None

	cursor.execute( """
		CREATE TABLE IF NOT EXISTS ITEM_SUMMARY
		( itemid int )
	""" )
	
	items = query_to_array( db, "SELECT DISTINCT ITEMID FROM ITEM_SALES" )
	keys = column_names( db, "ITEM_SALES" ) 
	keys = dict( zip( keys, range( len( keys ) ) ) )

	for item in items:
		price_info = query_to_array( db, "SELECT PRICE FROM ITEM_SALES WHERE ITEMID=" + str( item ) + " ORDER BY TIMESTAMP ASC" )
		dt = [ 0 ] + price_info[ 1: ]
		dp = [ a - b for a, b in zip( price_info, dt ) ]
		ud = [ 1 if e > 0 else ( 0 if e == 0 else -1 ) for e in dp ]
