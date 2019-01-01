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

class ByItemRawTable( TableAdapter ):
  NAME ="BY_ITEM_RAW"

  def __init__( self, db_name ):
    TableAdapter.__init__( self, db_name, self.NAME )
    self.cursor.execute( '''
      CREATE TABLE IF NOT EXISTS ''' + self.NAME + '''
      (
        itemid int,
  	name text,
        timestamp int,
	units int,
	price int
      )
    ''' )

class ByItemTable( TableAdapter ):

  NAME = "BY_ITEM"

  def __init__( self, db_name ):
    TableAdapter.__init__( self, db_name, self.NAME )
    self.cursor.execute( '''
      CREATE TABLE IF NOT EXISTS ''' + self.NAME + '''
      (
        itemid int,
        name text,
        timestamp long,
        price int,
	units int,
        price_delta_1day int,
	units_delta_1day int,
        price_plus bit,
        price_minus bit,
        price_crossed_average bit 
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
        price_average float,
	price_min int,
	price_max int,
	units_min int,
	units_max int,
        price_plus int,
        price_minus int,
	price_avg_abs_delta1day float,
	units_avg_abs_delta1day float,
        price_crossed_average int,
	units_buy_limit int
      )
    ''' )
    self.db.commit()

