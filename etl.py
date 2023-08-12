from constants import BUY_LIMITS, OSRS_API_ROUTES
from datetime import datetime
from db import DataModelTable, ItemDailyFactsTable, ItemMasterTable
from os.path import sep
from json import load as jload
from time import sleep
from utilities import column_names, load_dict_from_text, load_html_from_url, load_json_from_url, query_to_array, replace_keys


ALPHABET = "abcdefghijklmnopqrstuvwxyz"
PRICE_KEY_REGEX = "average180.*Date\('(.*)'\).*"
PRICE_VAL_REGEX = "average180.*\), (.*?),"
UNITS_KEY_REGEX = "trade180.*Date\('(.*)'\).*"
UNITS_VAL_REGEX = "trade180.*\), (.*)]"
REQUEST_TIMER = 3

def extract( db_path, day=None, request_timer=REQUEST_TIMER, alphabet=ALPHABET, members=True, verbose=True, max_page=-1 ):

	item_daily_db = ItemDailyFactsTable( db_path )
	item_summary_db = ItemMasterTable( db_path )

	API = OSRS_API_ROUTES
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

	limits = BUY_LIMITS

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

				if not members and "true" in detail_response[ "item" ][ "members" ]: 
					continue

				if verbose:
					print( "loading item: '" + str( item[ "name" ] ) + "' ( " + str( item[ "id" ] ) + " ) ..." )

				## loading and inserting item master data
				detail_keys[ "item" ] = item[ "id" ]
				detail = replace_keys( detail_template, placeholders, detail_keys )
				detail_response = load_json_from_url( detail )
				buy_limit = None
				try:
					buy_limit =  int( limits[ item[ "name" ] ] ) * 6 if item[ "name" ] in limits else None
				except:
					buy_limit = None

				item_summary_db.insert_dict( {
					"itemid": item[ "id" ],
					"name": item[ "name" ],
					"description": item[ "description" ],
					"members": "true" in detail_response[ "item" ][ "members" ],
					"units_daily_buy_limit": buy_limit
				} )

				## scraping price and unit data
				count_keys[ "item" ] = item[ "id" ]
				count_keys[ "alpha" ] = item[ "name" ].replace( " ", "+" )
				count = replace_keys( count_template, placeholders, count_keys )
				count_response = load_html_from_url( count, headers = {'User-Agent':'Magic Browser'} )
				price = load_dict_from_text( count_response, PRICE_KEY_REGEX, PRICE_VAL_REGEX )
				units = load_dict_from_text( count_response, UNITS_KEY_REGEX, UNITS_VAL_REGEX )

				if not price:
					continue

				for el in price:
					date = datetime.strptime( el, "%Y/%m/%d" ).strftime( "%Y-%m-%d" )
					
					if day and day != date:
						continue
					
					item_daily_db.insert_dict( {
						"itemid": item[ "id" ],
						"day": date,
						"price": price[ el ],
						"units": units[ el ] if el in units else None,
					} )			
					
				print( "successfully loaded item " + str( item[ "id" ] ) + " ..." )

				sleep( REQUEST_TIMER )
	

			catalog_keys[ "page" ] = catalog_keys[ "page" ] + 1
 
	return True


## i am un multi-coring this for now, will need to look back into making this multithreaded
def transform( db_name, verbose=True ):
	my_model = DataModelTable( db_name )
	by_item_daily = ItemDailyFactsTable( db_name )

	for item in by_item_daily.select( keys=["itemid"], distinct=True )[ 0 ]:
		
		item = item[ 0 ]
	
		if verbose:
			print( "processing item " + str( item ) + " ..." )		

		daily_info = by_item_daily.select( keys=[ "price", "price_delta_1day" ], where={ "itemid": item }, orderby=[ "day" ] )[ 0 ]
		item_info = by_item_daily.select( keys=[ "MIN( price ) as price_min", "MAX( price ) as price_max", "AVG( price ) as price_average" ], where={ "itemid": item }, groupby = ['itemid'] )

		item_info = dict( zip( item_info[ 1 ], item_info[ 0 ][ 0 ] ) )

		price_info, delta_price_1day = zip( *daily_info )
		plus = [ ( 1 if e > 0  else 0 ) for e in delta_price_1day ]
		minus = [ ( 1 if e < 0 else 0 ) for e in delta_price_1day ]
		price_average = item_info[ 'price_average' ]
		price_crossed_average = sum( [ ( 1 if dp and min( [ p, p + dp ] ) <= price_average and price_average <= max( [ p, p + dp ] ) else 0 ) for p, dp in zip( price_info, delta_price_1day ) ] )
		price_current = price_info[ -1 ]
		price_min_diff = 1 if price_current == item_info[ 'price_min' ] else price_current - item_info[ 'price_min' ]
		price_max_diff = item_info[ 'price_max' ] - price_current

		my_model.insert_dict( {
			"itemid": item,
			"price_current": price_current,
			"price_plus": sum( plus ),
			"price_minus": sum( minus ),
			"price_crossed_average": price_crossed_average,
			"price_min_diff": price_min_diff,
			"price_max_diff": price_max_diff,
			"price_potential": price_max_diff * price_crossed_average / price_min_diff
		} )	
		

	return True 

