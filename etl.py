from os.path import sep
from json import load as jload
from time import sleep
from utilities import column_names, load_dict_from_url, load_json_from_url, query_to_array, replace_keys
from datetime import datetime
from db import ByItemRawTable, ByItemTable, ItemSummaryTable
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
COUNT_KEY_REGEX = "trade180.*Date\('(.*)'\).*"
COUNT_VAL_REGEX = "trade180.*\), (.*)]"
LIMIT_KEY_REGEX = "<td><a.*>(.*)</a>.*"
LIMIT_VAL_REGEX = "</td><td>(.*)"
REQUEST_TIMER=3
ROUTES_FILE_PATH = "configs" + sep + "routes"
API = jload( open( ROUTES_FILE_PATH, 'rb' ) )

def extract( db_path, request_timer=REQUEST_TIMER, alphabet=ALPHABET, verbose=True, max_page=-1 ):

	db = ByItemRawTable( db_path )

	catalog_template = API[ "endpoints" ][ "catalog" ][ "url" ]
	catalog_keys = API[ "endpoints" ][ "catalog" ][ "keys" ]
	catalog_keys = dict( zip( catalog_keys, [ None ] * len( catalog_keys ) ) )

	graph_template = API[ "endpoints" ][ "graph" ][ "url" ]
	graph_keys = API[ "endpoints" ][ "graph" ][ "keys" ]
	graph_keys = dict( zip( graph_keys, [ None ] * len( graph_keys ) ) )

	count_template = API[ "endpoints" ][ "count" ][ "url" ]
	count_keys = API[ "endpoints" ][ "count" ][ "keys" ]
	count_keys = dict( zip( count_keys, [ None ] * len( count_keys ) ) )

	placeholders = API[ "placeholders" ]

	for letter in alphabet:
		catalog_keys[ "alpha" ] = letter
		catalog_keys[ "page" ] = 0	
		
		while catalog_keys[ "page" ] - max_page:
			catalog = replace_keys( catalog_template, placeholders, catalog_keys )
			catalog = load_json_from_url( catalog )

			if verbose:
				print( "catalog letter: " + catalog_keys[ "alpha" ]  +  ", page: " + str( catalog_keys[ "page" ] ) )

			if not catalog or not len( catalog[ "items" ] ):
				break
				
			for item in catalog[ "items" ]:
		
				if verbose:
					print( "loading item: " + str( item[ "id" ] ) + " ..." )	
				graph_keys[ "item" ] = item[ "id" ]
				graph = replace_keys( graph_template, placeholders, graph_keys )
				graph_response = load_json_from_url( graph ) 

				count_keys[ "item" ] = item[ "id" ]
				count = replace_keys( count_template, placeholders, count_keys )
				count_response = load_dict_from_url( COUNT_KEY_REGEX, COUNT_VAL_REGEX, count )

				if graph_response:
					for el in graph_response[ "daily" ]:
						date = datetime.utcfromtimestamp( float( el ) / 1000 ).strftime( "%Y/%m/%d" )
						db.insert_dict( {
							"name": item[ "name" ],
							"itemid": item[ "id" ],
							"timestamp": el,
							"units": count_response[ date ] if count_response and date and date in count_response else 0,
							"price": graph_response[ "daily" ][ el ]
						} )
					print( "successfully loaded item " + str( item[ "id" ] ) + " ..." )
				else:
					print( "could not load graph on item: " + str( item[ 'id' ] ) )

				sleep( request_timer )

			catalog_keys[ "page" ] = catalog_keys[ "page" ] + 1
 
	return True


## i am un multi-coring this for now, will need to look back into making this multithreaded
def transform( db_name, verbose=True ):

	price_summary = []

	by_item_raw = ByItemRawTable( db_name )
	by_item = ByItemTable( db_name )
	item_summary = ItemSummaryTable( db_name )	

	limits = load_dict_from_url( LIMIT_KEY_REGEX, LIMIT_VAL_REGEX, API[ "endpoints" ][ "limits" ][ "url" ] )
	
	for item, name in by_item_raw.select( keys=["itemid", "name"], distinct=True )[ 0 ]:
		if verbose:
			print( "processing item " + str( item ) + " ..." )		

		item_info = by_item_raw.select( keys=["timestamp", "price", "units"], where={ "itemid": item }, orderby=["timestamp"] )[ 0 ]
		
		time_info, price_info, unit_info = zip( *item_info )
		delta_1day = [ 0 ] + [ price_info[ i ] - price_info[ i - 1 ]  for i in range( 1, len( price_info ) ) ]
		plus = [ ( 1 if e > 0  else 0 ) for e in delta_1day ]
		minus = [ ( 1 if e < 0 else 0 ) for e in delta_1day ]
		price_average = sum( price_info ) / len( price_info )
		average_abs_delta1day = sum( [ abs( e ) for e in delta_1day ] ) / len( delta_1day )
		crossed_average = [ ( 1 if dp and min( [ p, p + dp ] ) <= price_average and price_average <= max( [ p, p + dp ] ) else 0 ) for p, dp in zip( price_info, delta_1day ) ] 

		#item_df = DataFrame.from_dict( { 'time': time_info, 'price': price_info } )
		#model = ARIMA( item_df[ 'price' ].values, order=(5,1,0) )
		#model_fit = model.fit()	

		for timestamp, price, units, delta_1day, positive, negative, crossed_avg in zip( time_info, price_info, unit_info, delta_1day, plus, minus, crossed_average ):
			by_item.insert_dict( {
				"itemid": item,
				"name": name,
				"timestamp": timestamp,
				"price": price,
				"units": units,
				"delta_1day": delta_1day,
				"plus": positive,
				"minus": negative,
				"crossed_average": crossed_avg
			} )

		item_summary.insert_dict( {
			"itemid": item,
			"name": name,
			"price_average": price_average,
			"min": min( price_info ),
			"max": max( price_info ),
			"plus": sum( plus ),
			"minus": sum( minus ),
			"avg_abs_delta1day": average_abs_delta1day,
			"crossed_average": sum( crossed_average ),
			"buy_limit": int( limits[ name ].replace( ",", '' ) ) if name in limits else None
		} )

	return True 

