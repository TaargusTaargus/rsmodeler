from os.path import sep
from json import load as jload
from time import sleep
from utilities import column_names, load_dict_from_url, load_json_from_url, query_to_array, replace_keys
from datetime import datetime
from db import MyModelTable, ItemDailyTable, ItemSummaryTable
#from pandas import DataFrame
#from statsmodels.tsa.arima_model import ARIMA

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
COUNT_KEY_REGEX = "trade180.*Date\('(.*)'\).*"
COUNT_VAL_REGEX = "trade180.*\), (.*)]"
LIMIT_KEY_REGEX = "<td><a.*>(.*)</a>.*"
LIMIT_VAL_REGEX = "</td><td>(.*)"
REQUEST_TIMER=3
ROUTES_FILE_PATH = "configs" + sep + "routes"
API = jload( open( ROUTES_FILE_PATH, 'rb' ) )

def extract( db_path, request_timer=REQUEST_TIMER, alphabet=ALPHABET, members=True, verbose=True, max_page=-1 ):

	item_daily_db = ItemDailyTable( db_path )
	item_summary_db = ItemSummaryTable( db_path )

	catalog_template = API[ "endpoints" ][ "catalog" ][ "url" ]
	catalog_keys = API[ "endpoints" ][ "catalog" ][ "keys" ]
	catalog_keys = dict( zip( catalog_keys, [ None ] * len( catalog_keys ) ) )

	detail_template = API[ "endpoints" ][ "detail" ][ "url" ]
	detail_keys = API[ "endpoints" ][ "detail" ][ "keys" ]
	detail_keys = dict( zip( detail_keys, [ None ] * len( detail_keys ) ) )

	graph_template = API[ "endpoints" ][ "graph" ][ "url" ]
	graph_keys = API[ "endpoints" ][ "graph" ][ "keys" ]
	graph_keys = dict( zip( graph_keys, [ None ] * len( graph_keys ) ) )

	count_template = API[ "endpoints" ][ "count" ][ "url" ]
	count_keys = API[ "endpoints" ][ "count" ][ "keys" ]
	count_keys = dict( zip( count_keys, [ None ] * len( count_keys ) ) )

        limits = load_dict_from_url( LIMIT_KEY_REGEX, LIMIT_VAL_REGEX, API[ "endpoints" ][ "limits" ][ "url" ] )

	placeholders = API[ "placeholders" ]

	for letter in alphabet:
		catalog_keys[ "alpha" ] = letter
		catalog_keys[ "page" ] = 1	
	
		while max_page - catalog_keys[ "page" ] + 1:
			catalog = replace_keys( catalog_template, placeholders, catalog_keys )
			catalog = load_json_from_url( catalog )

			if verbose:
				print( "catalog letter: " + catalog_keys[ "alpha" ]  +  ", page: " + str( catalog_keys[ "page" ] ) )

			if not catalog or not len( catalog[ "items" ] ):
				break
				
			for item in catalog[ "items" ]:
				#print( [ item["name"] for item in catalog[ "items" ] ] )	
	
				detail_keys[ "item" ] = item[ "id" ]
				detail = replace_keys( detail_template, placeholders, detail_keys )
				detail_response = load_json_from_url( detail )
	
				if not members and "true" in detail_response[ "item" ][ "members" ]: 
					continue

				if verbose:
					print( "loading item: " + str( item[ "id" ] ) + " ..." )

				graph_keys[ "item" ] = item[ "id" ]
				graph = replace_keys( graph_template, placeholders, graph_keys )
				graph_response = load_json_from_url( graph ) 

				count_keys[ "item" ] = item[ "id" ]
				count = replace_keys( count_template, placeholders, count_keys )
				count_response = load_dict_from_url( COUNT_KEY_REGEX, COUNT_VAL_REGEX, count )

				if graph_response:
					p0, u0 = None, None
					price_info, unit_info, delta_price, delta_units = [], [], [], []
					for el in sorted( graph_response[ "daily" ] ):
						date = datetime.utcfromtimestamp( float( el ) / 1000 ).strftime( "%Y/%m/%d" )
						p1 = int( graph_response[ "daily" ][ el ] )
						u1 = int( count_response[ date ] ) if count_response and date and date in count_response else 0
						dp = p1 - p0 if p0 and p1 else None
						du = u1 - u0 if u0 and u1 else None
						item_daily_db.insert_dict( {
							"name": item[ "name" ],
							"itemid": item[ "id" ],
							"timestamp": el,
							"price": p1,
							"units": u1,
							"price_delta_1day": dp,
							"units_delta_1day": du
						} )
						p0 = p1
						u0 = u1
						delta_price.append( abs( dp if dp else 0 ) )
						delta_units.append( abs( du if du else 0 ) )
						price_info.append( p1 if p1 else 0 )
						unit_info.append( u1 if u1 else 0 )

					buy_limit = None
					try:
						buy_limit =  int( limits[ item[ "name" ] ].replace( ",", '' ) ) if item[ "name" ] in limits else None
					except:
						buy_limit = None

					item_summary_db.insert_dict( {
						"itemid": item[ "id" ],
						"name": item[ "name" ],
						"members": "true" in detail_response[ "item" ][ "members" ],
						"price_average": sum( price_info ) / len( price_info ),
						"units_average": sum( unit_info ) / len( unit_info ),
						"price_min": min( price_info ),
						"price_max": max( price_info ),
						"units_min": min( unit_info ),
						"units_max": max( unit_info ),
						"price_avg_abs_delta1day": sum( delta_price ) / len( delta_price ),
						"units_avg_abs_delta1day": sum( delta_units ) / len( delta_units ),
						"units_daily_buy_limit": buy_limit
					} )
					print( "successfully loaded item " + str( item[ "id" ] ) + " ..." )
				else:
					print( "could not load graph on item: " + str( item[ 'id' ] ) )

				sleep( REQUEST_TIMER )

			catalog_keys[ "page" ] = catalog_keys[ "page" ] + 1
 
	return True


## i am un multi-coring this for now, will need to look back into making this multithreaded
def transform( db_name, verbose=True ):
	my_model = MyModelTable( db_name )
	by_item_daily = ItemDailyTable( db_name )	

	for item, name in by_item_daily.select( keys=["itemid", "name"], distinct=True )[ 0 ]:
		if verbose:
			print( "processing item " + str( item ) + " ..." )		

		item_info = by_item_daily.select( keys=["price", "price_delta_1day"], where={ "itemid": item } )[ 0 ]	
		price_info, delta_price_1day = zip( *item_info )
		plus = [ ( 1 if e > 0  else 0 ) for e in delta_price_1day ]
		minus = [ ( 1 if e < 0 else 0 ) for e in delta_price_1day ]
		price_average = sum( price_info ) / len( price_info )
		crossed_average = [ ( 1 if dp and min( [ p, p + dp ] ) <= price_average and price_average <= max( [ p, p + dp ] ) else 0 ) for p, dp in zip( price_info, delta_price_1day ) ] 
		my_model.insert_dict( {
			"itemid": item,
			"name": name,
			"price_plus": sum( plus ),
			"price_minus": sum( minus ),
			"price_crossed_average": sum( crossed_average )
		} )
		#item_df = DataFrame.from_dict( { 'time': time_info, 'price': price_info } )
		#model = ARIMA( item_df[ 'price' ].values, order=(5,1,0) )
		#model_fit = model.fit()	
		

	return True 

