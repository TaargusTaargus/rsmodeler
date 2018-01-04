from json import load
from urllib2 import urlopen
from time import sleep

def load_json_from_url( url, attempts=3, timeout=5 ):
	if not attempts:
		print( "was unable to load url: " + url )
		return None

	attempts = attempts - 1
	fp = None

	try:
		fp = urlopen( url )
	except Exception as e:
		print( "was unable to open url, trying again ..." )
		sleep( timeout )
		load_json_from_url( url, attempts )

	if not fp:
		load_json_from_url( url, attempts )

	try:
		return load( fp )
	except:
		print( "was unable to load downloaded json, trying again ..." )
		sleep( timeout )	
		load_json_from_url( url, attempts )


def replace_keys( string, placeholders, keys ):
	for key in keys:
		string = string.replace( str( placeholders[ key ] ), str( keys[ key ] ) )
	return string


def column_names( db, table ):
	cursor = db.cursor()
	return cursor.execute( "SELECT SQL FROM SQLITE_MASTER WHERE TBL_NAME='" + table + "' AND type='table'" ).fetchone() 


def query_to_array( db, query ):
	return [ a for a, in db.cursor().execute( query ).fetchall() ]
