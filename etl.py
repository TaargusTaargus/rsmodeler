from constants import BUY_LIMITS, OPTIONS_DEFAULT, OSRS_API_ROUTES, PRICE_KEY_REGEX, PRICE_VAL_REGEX, UNITS_KEY_REGEX, UNITS_VAL_REGEX
from datetime import datetime
from db import DataModelTable, ItemDailyFactsTable, ItemMasterTable
from os.path import sep
from json import load as jload
from sqlite3 import connect
from time import sleep
from utilities import column_names, load_dict_from_text, load_html_from_url, load_json_from_url, query_to_array, replace_keys

class RSModelerETL:

	def __init__( self, db_path, options = OPTIONS_DEFAULT ):
		self.db_path = db_path
		self.options = options
		self.tmp_db = connect( ":memory:" )

	def __extract__( self ):

		item_daily_db = ItemDailyFactsTable( self.tmp_db )
		item_summary_db = ItemMasterTable( self.tmp_db )

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
		
		for letter in self.options[ 'ALPHABET' ]:
		
			catalog_keys[ "alpha" ] = letter
			catalog_keys[ "page" ] = self.options[ 'START_PAGE' ]
		
			while self.options[ 'END_PAGE' ] - catalog_keys[ "page" ] + 1:
			
				catalog = replace_keys( catalog_template, placeholders, catalog_keys )
				catalog = load_json_from_url( catalog )

				if self.options[ 'VERBOSE' ] == 1:
					print( "catalog letter: " + catalog_keys[ "alpha" ]  +  ", page: " + str( catalog_keys[ "page" ] ) )
				elif self.options[ 'VERBOSE' ] > 1:
					print( "catalog items (letter: '" + catalog_keys[ "alpha" ] + "', page: " + str(catalog_keys[ "page" ]) + "):\n- " + "\n- ".join( [ e[ 'name' ] for e in catalog[ "items" ] ] ) )

				if not catalog or not len( catalog[ "items" ] ):
					break
					
				for item in catalog[ "items" ]:

					## loading and inserting item master data
					detail_keys[ "item" ] = item[ "id" ]
					detail = replace_keys( detail_template, placeholders, detail_keys )
					detail_response = load_json_from_url( detail )

					if not detail_response:
						continue					

					if self.options[ 'MEMBERS' ] and "true" in detail_response[ "item" ][ "members" ]: 
						continue

					if self.options[ 'VERBOSE' ]:
						print( "loading item: '" + str( item[ "name" ] ) + "' ( " + str( item[ "id" ] ) + " ) ..." )

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
					
					if not count_response:
						continue
						
					price = load_dict_from_text( count_response, PRICE_KEY_REGEX, PRICE_VAL_REGEX )
					units = load_dict_from_text( count_response, UNITS_KEY_REGEX, UNITS_VAL_REGEX )

					date_keys = set()
				
					if not price and not units:
						continue
					
					if price:
						date_keys = date_keys | set( price.keys() )
					
					if units:
						date_keys = date_keys | set( units.keys() )

					for el in date_keys:
						
						date = datetime.strptime( el, "%Y/%m/%d" ).strftime( "%Y-%m-%d" )

						if self.options[ 'DAY' ] and self.options[ 'DAY' ] != date:
							continue

						item_daily_db.insert_dict( {
							"itemid": item[ "id" ],
							"day": date,
							"price": price[ el ] if price and el in price else None,
							"units": units[ el ] if units and el in units else None,
						} )			
					
					if self.options[ 'VERBOSE' ]:
						print( "successfully loaded item " + str( item[ "id" ] ) + " ..." )

					sleep( self.options[ 'REQUEST_TIMER' ] )
		

				catalog_keys[ "page" ] = catalog_keys[ "page" ] + 1
	 
		return True


	def __transform__( self ):
		data_model_table = DataModelTable( self.tmp_db )
		data_model_table.cursor.execute( '''
			-- get some simple statistical features
			WITH CTE_FACTS_AGG AS 
			(
				SELECT
					ITEMID
					, MIN( PRICE ) AS MIN_PRICE
					, MAX( PRICE ) AS MAX_PRICE
					, AVG( PRICE ) AS AVG_PRICE
					, AVG( UNITS ) AS AVG_UNITS
					, MAX( DAY ) AS CURRENT_DAY
				FROM ITEM_DAILY_FACTS
				GROUP BY ITEMID
			)
			-- get an idea of volatility, in this case how many times an item is likely to cross its price average
			-- gauranteed to be at least 1
			/*, CTE_DELTAPRICE AS
			(
				SELECT 
					P1.ITEMID
					, P1.DAY
					, COALESCE( P2.PRICE  - P1.PRICE, 0 ) AS DELTA_PRICE 
				FROM ITEM_DAILY_FACTS P1 
				INNER JOIN ITEM_DAILY_FACTS P2 
					ON P1.ITEMID = P2.ITEMID 
					AND DATE( P1.DAY, '+1 day' ) = P2.DAY
			)*/
			, CTE_CROSSED_AVERAGE AS
			(
				SELECT 
					P1.ITEMID
					, P1.DAY
					, COALESCE( CASE WHEN P1.PRICE - AGG.AVG_PRICE < 0 THEN -1 ELSE 1 END, 0 ) AS CROSSED_AVERAGE
				FROM ITEM_DAILY_FACTS P1 
				INNER JOIN CTE_FACTS_AGG AGG
					ON P1.ITEMID = AGG.ITEMID
			)
			, CTE_VOLATILITY AS
			(
				SELECT
					ITEMID
					, SUM( DELTA_CROSSED_AVERAGE ) AS VOLATILITY
				FROM (
					SELECT 
						CA1.ITEMID
						, CA1.DAY
						, COALESCE( ABS( CA2.CROSSED_AVERAGE  - CA1.CROSSED_AVERAGE ), 0 ) AS DELTA_CROSSED_AVERAGE
					FROM CTE_CROSSED_AVERAGE CA1
					INNER JOIN CTE_CROSSED_AVERAGE CA2 
						ON CA1.ITEMID = CA2.ITEMID 
						AND DATE( CA1.DAY, '+1 day' ) = CA2.DAY
				)
				GROUP BY ITEMID
			)
			, CTE_CURRENT AS (
				SELECT
					f.ITEMID
					, f.PRICE
				FROM ITEM_DAILY_FACTS f
				INNER JOIN CTE_FACTS_AGG a
					ON f.ITEMID = a.ITEMID
					AND f.DAY = a.CURRENT_DAY
			)
			, CTE_SCORE AS (
				SELECT
					c.ITEMID
					, (a.MAX_PRICE - c.PRICE) / CASE WHEN (c.PRICE - a.MIN_PRICE) = 0 THEN 1 ELSE (c.PRICE - a.MIN_PRICE) END AS PRICE_POTENTIAL
					, v.VOLATILITY AS VOLATILITY
					, (a.MAX_PRICE - c.PRICE) / CASE WHEN (c.PRICE - a.MIN_PRICE) = 0 THEN 1 ELSE (c.PRICE - a.MIN_PRICE) END 
						* v.VOLATILITY
						* a.AVG_UNITS AS SCORE
				FROM CTE_CURRENT c 
				INNER JOIN CTE_FACTS_AGG a
					ON c.ITEMID = a.ITEMID
				INNER JOIN CTE_VOLATILITY v
					ON c.ITEMID = v.ITEMID
			)
			INSERT INTO DATA_MODEL
			SELECT 
				*
				, ROW_NUMBER() OVER (ORDER BY SCORE DESC) AS SCORE_RANK
			FROM CTE_SCORE
		''' )
		return True 

	def __load__( self ): 

		# Connect to the source and destination databases
		dest_conn = connect( self.db_path )
		
		# Ensure tables exist
		ItemDailyFactsTable( dest_conn )
		ItemMasterTable( dest_conn )
		DataModelTable( dest_conn )

		# Attach the destination database
		dest_conn.execute( "ATTACH DATABASE '" + self.db_path + "' AS dest" )

		# Create a cursor for both databases
		source_cursor = self.tmp_db.cursor()
		dest_cursor = dest_conn.cursor()

		# Copy data from the source table to the destination table
		for table in [ ItemDailyFactsTable.NAME, ItemMasterTable.NAME, DataModelTable.NAME ]:
			source_cursor.execute( "SELECT * FROM " + table ) 
			data_to_copy = source_cursor.fetchall()
			
			if len( data_to_copy ):
				placeholders = ', '.join( [ '?' ] * len( data_to_copy[ 0 ] ) )
				dest_cursor.executemany( "REPLACE INTO dest." + table + " VALUES (" + placeholders + ")", data_to_copy )

		# Commit changes to the destination database
		dest_conn.commit()

		# Detach the destination database
		dest_conn.execute("DETACH DATABASE dest")

		# Close connections
		self.tmp_db.close()
		dest_conn.close()
		


	def execute( self ):
	
		try:
			self.__extract__()
		except Exception as e:
			print( "Ran into an issue during extract process." )
			print( e )
			return False

		
		try:
			self.__transform__()
		except Exception as e:
			print( "Ran into an issue during transform process." )
			print( e )
			return False
			
		try:
			self.__load__()
		except Exception as e:
			print( "Ran into an issue during load process." )
			print( e )
			return False


