from sqlite3 import connect

class TableAdapter:

  def __init__( self, db, table_name ):
    self.db = db
    self.cursor = self.db.cursor()
    self.table_name = table_name


  def insert_dict( self, dict ):
    placeholders = ', '.join( [ '?' ] * len( dict ) )
    columns = ', '.join( dict.keys() )
    sql = "REPLACE INTO %s ( %s ) VALUES ( %s )" % ( self.table_name, columns, placeholders )
    self.cursor.execute( sql, dict.values() )
    self.db.commit()


  def select( self, keys=[ "*" ], where=None, orderby=None, groupby=None, distinct=False ):
    distinct_clause = ""
    if distinct:
      distinct_clause = " DISTINCT "   

    select_clause = ""
    if keys:
    	select_clause = ", ".join( keys )
    else:
    	return None

    where_clause = ""
    if where:
      where_clause = " WHERE " + " AND ".join( [ key + "=" + str( where[ key ] ) + "" for key in where ] )

    orderby_clause = ""
    if orderby:
      orderby_clause = " ORDER BY " + ", ".join( orderby )
      
    groupby_clause = ""
    if groupby:
      groupby_clause = ", ".join( groupby )
      select_clause = groupby_clause + ", " + select_clause
      groupby_clause = " GROUP BY " + groupby_clause
      
    return ( self.cursor.execute( 
               "SELECT " + distinct_clause 
                + select_clause
		+ " FROM " + self.table_name
                + where_clause 
                + groupby_clause 
                + orderby_clause
           ).fetchall(),
             [ e[ 0 ] for e in self.cursor.description ]
           )

class ItemDailyFactsTable( TableAdapter ):

  NAME ="ITEM_DAILY_FACTS"

  def __init__( self, db ):
    TableAdapter.__init__( self, db, self.NAME )
    self.cursor.execute( '''
      CREATE TABLE IF NOT EXISTS ''' + self.NAME + '''
      (
	itemid int,
        day date,
        units int,
        price int,
        PRIMARY KEY( itemid, day )
      )
    ''' )


class ItemMasterTable( TableAdapter ):

  NAME = "ITEM_MASTER"

  def __init__( self, db):
    TableAdapter.__init__( self, db, self.NAME )
    self.cursor.execute( '''
      CREATE TABLE IF NOT EXISTS ''' + self.NAME + '''
      ( 
        itemid int,
        name text,
        description text,
        members bit,
	units_daily_buy_limit int,
	PRIMARY KEY( itemid )
      )
    ''' )
    self.db.commit()

class DataModelTable( TableAdapter ):

  NAME = "DATA_MODEL"

  def __init__( self, db ):
    TableAdapter.__init__( self, db, self.NAME )
    self.cursor.execute( '''
      CREATE TABLE IF NOT EXISTS ''' + self.NAME + '''
      ( 
        itemid int,
	price_potential float,
	volatility int,
	score float,
	score_rank int,
	PRIMARY KEY( itemid )
      )
    ''' )
    self.db.commit()


