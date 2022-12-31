from sqlite3 import connect

class TableAdapter:

  def __init__( self, db_name, table_name ):
    self.db = connect( db_name )
    self.db_name = db_name
    self.cursor = self.db.cursor()
    self.table_name = table_name


  def insert_dict( self, dict ):
    placeholders = ', '.join( [ '?' ] * len( dict ) )
    columns = ', '.join( dict.keys() )
    sql = "REPLACE INTO %s ( %s ) VALUES ( %s )" % ( self.table_name, columns, placeholders )
    self.cursor.execute( sql, dict.values() )
    self.db.commit()


  def select( self, keys=[ "*" ], where=None, orderby=None, distinct=False ):
    distinct_clause = ""
    if distinct:
      distinct_clause = " DISTINCT "   

    where_clause = ""
    if where:
      where_clause = " WHERE " + " AND ".join( [ key + "=" + str( where[ key ] ) + "" for key in where ] )

    orderby_clause = ""
    if orderby:
      orderby_clause = " ORDER BY " + ", ".join( orderby )
    return ( self.cursor.execute( 
               "SELECT " + distinct_clause + ", ".join( keys ) 
		+ " FROM " + self.table_name
                + where_clause + orderby_clause
           ).fetchall(),
             [ e[ 0 ] for e in self.cursor.description ]
           )

class ItemDailyTable( TableAdapter ):
  NAME ="ITEM_DAILY"

  def __init__( self, db_name ):
    TableAdapter.__init__( self, db_name, self.NAME )
    self.cursor.execute( '''
      CREATE TABLE IF NOT EXISTS ''' + self.NAME + '''
      (
        itemid int,
  	name text,
        timestamp int,
	day text,
	units int,
	price int,
	price_delta_1day int,
	units_delta_1day int
      )
    ''' )

class ItemSummaryTable( TableAdapter ):

  NAME = "ITEM_SUMMARY"

  def __init__( self, db_name ):
    TableAdapter.__init__( self, db_name, self.NAME )
    self.cursor.execute( '''
      CREATE TABLE IF NOT EXISTS ''' + self.NAME + '''
      ( 
        itemid int,
        name text,
        members bit,
        price_average float,
	units_average float,
	price_min int,
	price_max int,
	units_min int,
	units_max int,
	price_avg_abs_delta1day float,
	units_avg_abs_delta1day float,
	units_daily_buy_limit int
      )
    ''' )
    self.db.commit()

class MyModelTable( TableAdapter ):

  NAME = "MODEL"

  def __init__( self, db_name ):
    TableAdapter.__init__( self, db_name, self.NAME )
    self.cursor.execute( '''
      CREATE TABLE IF NOT EXISTS ''' + self.NAME + '''
      ( 
        itemid int,
        name text,
	price_current int,
        price_plus int,
	price_minus int,
	price_crossed_average int,
	price_min_diff int,
	price_max_diff int,
	price_potential float
      )
    ''' )
    self.db.commit()


