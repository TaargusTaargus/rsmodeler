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
        delta_1day int,
        plus int,
        minus int,
        crossed_average bit 
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
        plus int,
        minus int,
        crossed_average int
      )
    ''' )
    self.db.commit()

