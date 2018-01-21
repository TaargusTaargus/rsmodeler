from os.path import sep
from json import load
from time import sleep
from utilities import column_names, load_json_from_url, query_to_array, replace_keys
from datetime import datetime

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
REQUEST_TIMER = 5
ROUTES_FILE_PATH = "configs" + sep + "routes"

## this needs to be remote to in memory, not to db...
def extract( routes=ROUTES_FILE_PATH, db=None, verbose=True ):

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
					results[ item[ 'id' ] ] = {
						"name": item[ "name" ],
						"itemid": item[ 'id' ],
						#"date": datetime.fromtimestamp( int( int( point ) / 1000 ) ).strftime( "%Y-%m-%d %H:%M:%S" ),
						#"timestamp": point,
						"price": graph[ "daily" ]
					}
				else:
					print( "could not load graph on item: " + str( item[ 'id' ] ) )

				sleep( REQUEST_TIMER )

			catalog_keys[ "page" ] = catalog_keys[ "page" ] + 1
 
	return results


def transform( item_dataset, verbose=True ):

	by_item = []
	item_summary = []
	price_summary = []
	
	for item in item_dataset:

		if verbose:
			print( "processing item " + str( item ) + " ..." )		

		item_info = item_dataset[ item ]

		price_info = [ e[ "price" ] for e in item_info ]
		delta_1day = [ a - b for a, b in zip( price_info[ :-1 ], price_info[ 1: ] ) ] + [ 0 ]
		plus = [ ( 1 if e > 0  else 0 ) for e in delta_1day ]
		minus = [ ( 1 if e < 0 else 0 ) for e in delta_1day ]
		price_average = sum( price_info ) / len( price_info )
		crossed_average = [ ( 1 if dp and min( [ p, p + dp ] ) <= price_average and price_average <= max( [ p, p + dp ] ) else 0 ) for p, dp in zip( price_info, delta_1day ) ] 


		for item_info, delta_1day, positive, negative, crossed_avg in zip( item_info, delta_1day, plus, minus, crossed_average ):
			by_item.append( {
				"itemid": item_info[ "itemid" ],
				"name": item_info[ "name" ],
				"timestamp": item_info[ "timestamp" ],
				"date": item_info[ "date" ],
				"price": item_info[ "price" ],
				"delta_1day": delta_1day,
				"plus": positive,
				"minus": negative,
				"crossed_average": crossed_avg
			} )

		item_summary.append( {
			"itemid": item_info[ "itemid" ],
			"name": item_info[ "name" ],
			"price_average": price_average,
			"plus": sum( plus ),
			"minus": sum( minus ),
			"crossed_average": sum( crossed_average )
		} )

	return ( by_item, item_summary )

