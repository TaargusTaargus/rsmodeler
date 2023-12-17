from bs4 import BeautifulSoup
from constants import BUY_LIMITS, OPTIONS_DEFAULT, OSRS_API_ROUTES, PRICE_KEY_REGEX, PRICE_VAL_REGEX, UNITS_KEY_REGEX, UNITS_VAL_REGEX
from datetime import datetime
from db import DataModelTable, ItemDailyFactsTable, ItemMasterTable, ItemMaterialsTable
from os.path import sep
from json import load as jload
from sqlite3 import connect
from time import sleep
from utilities import column_names, load_dict_from_text, load_html_from_url, load_json_from_url, query_to_array, replace_keys
import re, requests

class OsrsWikiScraper:

	def get_high_alch_information( self, html_content ):

		
		LOW_ALCH_PATTERN = r'Low alch.*?(\d+,\d+)* coins'
		HIGH_ALCH_PATTERN = r'High alch.*?(\d+,\d+)* coins'
		
		try: 
			high = int( re.findall( LOW_ALCH_PATTERN, html_content )[ 0 ].replace( ",", "" ) )
			low = int( re.findall( HIGH_ALCH_PATTERN, html_content )[ 0 ].replace( ",", "" ) )
			return low, high
		except:
			return None, None


	def get_material_relationships( self, html_content ):

		# Parse the HTML content with Beautiful Soup
		soup = BeautifulSoup( html_content, 'html.parser' )
	    
		# Find the table element(s) on the page
		tables = soup.find_all( 'table' )
	    
		# Loop through the tables (if there are multiple)
		for table in tables:
	    
			caption = table.find( 'caption' )
			    
			## we only care about the Materials table
			if not caption or caption.text.strip() != 'Materials':
				continue
		    
		    
			## since this is the Materials table -- loop through the rows
			materials = []
			for row in table.find_all( 'tr' ):
		       
				## Get all column values
				columns = row.find_all( 'td' )  # Change 'td' to 'th' if you want to include header cells
			    
				if len( columns ) > 2:
					try:
						materials.append( ( columns[ 1 ].text.strip(), int( columns[ 2 ].text.strip().replace( ",", "" ) ) ) )
					except ValueError as e:
						continue
		
			if materials:
				n_produced = materials[ -1 ][ 1 ]
				return [ ( e, n / n_produced ) for e, n in materials[ : -1 ] ]


	def retrieve_item_osrs_wiki( self, item_name ):

		# Define the URL of the website you want to scrape
		url = 'https://oldschool.runescape.wiki/w/' + item_name

		# Send an HTTP GET request to the URL and retrieve the page content
		response = requests.get( url )

		# Check if the request was successful
		if response.status_code == 200:

			# Extract text from the HTML content
			html_content = response.content.decode( "cp1252", "ignore" )
			return html_content
		
		else:
			print( "Failed to retrieve the web page. Status code: " + str(response.status_code) )
			return None


	


class RSModelerETL:

	def __init__( self, db_path, options = OPTIONS_DEFAULT ):
		## setting up database information
		self.db_path = db_path
		self.options = options
		self.tmp_db = connect( ":memory:" )
		
		## setting up table connections in db
		self.data_model_table = DataModelTable( self.tmp_db )
		self.item_daily_fact_table = ItemDailyFactsTable( self.tmp_db )
		self.item_master_table = ItemMasterTable( self.tmp_db )
		self.item_materials_table = ItemMaterialsTable( self.tmp_db )
		
		## state variables
		self.catalog = []
		
		## setting up API routing
		API = OSRS_API_ROUTES
		self.catalog_template = API[ "endpoints" ][ "catalog" ][ "url" ]
		catalog_keys = API[ "endpoints" ][ "catalog" ][ "keys" ]
		self.catalog_keys = dict( zip( catalog_keys, [ None ] * len( catalog_keys ) ) )

		self.detail_template = API[ "endpoints" ][ "detail" ][ "url" ]
		detail_keys = API[ "endpoints" ][ "detail" ][ "keys" ]
		self.detail_keys = dict( zip( detail_keys, [ None ] * len( detail_keys ) ) )

		self.graph_template = API[ "endpoints" ][ "graph" ][ "url" ]
		graph_keys = API[ "endpoints" ][ "graph" ][ "keys" ]
		self.graph_keys = dict( zip( graph_keys, [ None ] * len( graph_keys ) ) )

		self.count_template = API[ "endpoints" ][ "count" ][ "url" ]
		count_keys = API[ "endpoints" ][ "count" ][ "keys" ]
		self.count_keys = dict( zip( count_keys, [ None ] * len( count_keys ) ) )
		
		self.placeholders = API[ 'placeholders' ]


	def __extract_item_details__( self, itemid ):

		## loading and inserting item master data
		item_entry = {}
		
		self.detail_keys[ "item" ] = itemid
		detail = replace_keys( self.detail_template, self.placeholders, self.detail_keys )
		detail_response = load_json_from_url( detail )

		if self.options[ 'verbose' ] > 1:
			print( "detail url: " + detail )

		if not detail_response or ( self.options[ 'members' ] and "true" in detail_response[ "item" ][ "members" ] ): 
			return item_entry

		if self.options[ 'verbose' ]:
			print( "loading item: '" + str( detail_response[ "item" ][ "name" ] ) + "' ( " + str( itemid ) + " ) ..." )

		buy_limit = None
		try:
			buy_limit =  int( BUY_LIMITS[ detail_response[ "item" ][ "name" ] ] ) * 6 if detail_response[ "item" ][ "name" ] in BUY_LIMITS else None
		except:
			buy_limit = None

		item_entry[ "itemid" ] = itemid
		item_entry[ "name" ] = detail_response[ "item" ][ "name" ]
		item_entry[ "description" ] = detail_response[ "item" ][ "description" ]
		item_entry[ "members" ] = "true" in detail_response[ "item" ][ "members" ]
		item_entry[ "units_daily_buy_limit" ] = buy_limit
		return item_entry


	def __extract_item_fact__( self, itemid, name ):
	
		if self.options[ 'verbose' ]:
			print( "extracting fact information for " + name + " ..." )
	
		## scraping price and unit data
		self.count_keys[ "item" ] = itemid
		self.count_keys[ "alpha" ] = name.replace( " ", "+" )
		count = replace_keys( self.count_template, self.placeholders, self.count_keys )
		
		if self.options[ 'verbose' ] > 1:
			print( "count (fact table) url: " + count )
		
		count_response = load_html_from_url( count, headers = {'User-Agent':'Magic Browser'} )
			
		if not count_response:
			return
			
		price = load_dict_from_text( count_response, PRICE_KEY_REGEX, PRICE_VAL_REGEX )
		units = load_dict_from_text( count_response, UNITS_KEY_REGEX, UNITS_VAL_REGEX )

		date_keys = set()
		
		if not price and not units:
			return item_entry
				
		if price:
			date_keys = date_keys | set( price.keys() )
				
		if units:
			date_keys = date_keys | set( units.keys() )

		for el in date_keys:
						
			date = datetime.strptime( el, "%Y/%m/%d" ).strftime( "%Y-%m-%d" )

			if self.options[ 'day' ] and self.options[ 'day' ] != date:
				return item_entry

			self.item_daily_fact_table.insert_dict( {
				"itemid": itemid,
				"day": date,
				"price": price[ el ] if price and el in price else None,
				"units": units[ el ] if units and el in units else None,
			} )
			
		
		
	def __extract_item__( self, itemid ):
				
		## get item data
		item_entry = self.__extract_item_details__( itemid )

		if self.options[ 'fact' ]:
			self.__extract_item_fact__( itemid, item_entry[ 'name' ] )
			
		 ## resolve material relationships if requested
		if self.options[ 'materials' ] or self.options[ 'alch' ]:

			scraper = OsrsWikiScraper()
			
			name = item_entry[ "name" ]
			formatted_item_string = name.replace( " ", "_" ).replace( "'", "%27" )
			content = scraper.retrieve_item_osrs_wiki( formatted_item_string )
			
			if self.options[ 'alch' ]:
				item_entry[ 'low_alch' ], item_entry[ 'high_alch' ] = scraper.get_high_alch_information( content )
			
			if self.options[ 'materials' ]:
		 
		 		if self.options[ 'verbose' ]:
		 			print( 'checking material relationships for ' + name + ' ...' )
		 		
		 		materials = scraper.get_material_relationships( content )
		 		
		 		if materials:
		 		
		 			for material, quantity in materials:
		 			
		 				if material in self.catalog:
		 					self.item_materials_table.insert_dict( {
		 						'parent_itemid': itemid
		 						, 'child_itemid': self.catalog[ material ]
		 						, 'n_required': quantity
		 					} )
				
		## insert into the item master table
		self.item_master_table.insert_dict( item_entry )
		
		if self.options[ 'verbose' ]:
			print( "successfully loaded item " + str( itemid ) + " ..." )

		
	def __extract_item_catalog__( self ):
	
		## extract itemids from current catalog
		items = {}
		
		if self.options[ 'verbose' ]:
			print( "collecting items from osrs catalog..." )
		
		for letter in self.options[ 'alpha' ]:
		
			self.catalog_keys[ "alpha" ] = letter
			if self.options[ "page" ]:
				self.catalog_keys[ "page" ] = self.options[ "page" ]
			else:
				self.catalog_keys[ "page" ] = 1
		
			while not self.options[ "page" ] or self.catalog_keys[ "page" ] <= self.options[ "page" ]:
			
				catalog = replace_keys( self.catalog_template, self.placeholders, self.catalog_keys )
				
				if self.options[ 'verbose' ] > 1:
					print( "catalog url: " + catalog )
				
				catalog = load_json_from_url( catalog )

				if self.options[ 'verbose' ] == 1:
					print( "catalog letter: " + self.catalog_keys[ "alpha" ]  +  ", page: " + str( self.catalog_keys[ "page" ] ) )
				elif self.options[ 'verbose' ] > 1:
					print( "catalog items (letter: '" + self.catalog_keys[ "alpha" ] + "', page: " + str( self.catalog_keys[ "page" ] ) + "):\n- " + "\n- ".join( [ e[ 'name' ] for e in catalog[ "items" ] ] ) )

				if not catalog or not len( catalog[ "items" ] ):
					break
					
				## extend the catalog
				for e in catalog[ "items" ]:
					items[ e[ "name" ] ] = e[ "id" ]
					
				self.catalog_keys[ "page" ] = self.catalog_keys[ "page" ] + 1
				
				sleep( 1 )

		return items



	def __extract__( self ):
		
		## establish catalog ids from query
		self.catalog = self.__extract_item_catalog__()
		
		## extract item details
		for name, itemid in self.catalog.items():
			self.__extract_item__( itemid )
			sleep( self.options[ 'timer' ] )
	 	
		return True


	def __transform__( self ):
		self.data_model_table.cursor.execute( '''
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
		ItemMaterialsTable( dest_conn )
		DataModelTable( dest_conn )

		# Attach the destination database
		dest_conn.execute( "ATTACH DATABASE '" + self.db_path + "' AS dest" )

		# Create a cursor for both databases
		source_cursor = self.tmp_db.cursor()
		dest_cursor = dest_conn.cursor()

		# Copy data from the source table to the destination table
		for table in [ ItemDailyFactsTable.NAME, ItemMasterTable.NAME, ItemMaterialsTable.NAME, DataModelTable.NAME ]:
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
	
		if self.options[ 'verbose' ]:
			print( "beginning extract..." )
			

		try:
			self.__extract__()
		except Exception as e:
			print( "Ran into an issue during transform process." )
			print( e )
			return False

		if self.options[ 'verbose' ]:
			print( "beginning transform..." )
		
		try:
			self.__transform__()
		except Exception as e:
			print( "Ran into an issue during transform process." )
			print( e )
			return False
			
		if self.options[ 'verbose' ]:
			print( "beginning load..." )
			
		try:
			self.__load__()
		except Exception as e:
			print( "Ran into an issue during load process." )
			print( e )
			return False


