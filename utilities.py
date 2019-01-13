from json import loads
from urllib2 import urlopen
from time import sleep
from re import findall, MULTILINE

def load_json_from_url( url, attempts=3, timeout=10 ):  

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
		return load_json_from_url( url, attempts, timeout + 1 )

	if not fp:
		print( "was unable to open url, trying again ..." )
		return load_json_from_url( url, attempts, timeout + 1 )

	try:
		json = loads( fp.read() )
		if json:
			return json
	except:
		print( "was unable to load downloaded json, trying again ..." )
		sleep( timeout )	
	
	return load_json_from_url( url, attempts, timeout + 1 )

def load_dict_from_url( regex_key, regex_val, url, attempts=3, timeout=10 ):

	if not attempts:
		print( "was unable to load url: " + url )

	attempts = attempts - 1
	fp = None

	try:
		fp = urlopen( url )
	except Exception as e:
		print( "was unable to open url, trying again ..." )
		sleep( timeout )
		return load_dict_from_url( regex_key, regex_val, url, attempts, timeout + 1 )
	
	text = fp.read()
	
	if not text:
		print( "received no text from response, trying again ..." )
		sleep( timeout )
		return load_dict_from_url( regex_key, regex_val, url, attempts, timeout + 1 )

	try:
		keys = findall( regex_key, text, flags=MULTILINE )
		if len( keys ) and len( keys[ 0 ] ) > 1:
			keys = [ e for t in keys for e in t if e ]
		vals = findall( regex_val, text, flags=MULTILINE )
		if len( vals ) and len( vals[ 0 ] ) > 1:
			vals = [ e for t in vals for e in t if e ]
		ret_dict = dict( zip( keys, vals ) )
		if ret_dict:
			return ret_dict

	except Exception as e:
		print( "error creating dictionary from given regexes, exitting ..." )


def replace_keys( string, placeholders, keys ):
	for key in keys:
		string = string.replace( str( placeholders[ key ] ), str( keys[ key ] ) )
	return string


def column_names( db, table ):
	cursor = db.cursor()
	cursor = cursor.execute( "SELECT * FROM " + table )
	return [ e[ 0 ] for e in cursor.description ]


def query_to_array( db, query ):
	return [ a for a, in db.cursor().execute( query ).fetchall() ]


def split_array( array, parts ):
	offset = int( len( array ) / parts )
	results = [ None ] * parts
	for idx in range( parts ):
		start, end = idx * offset, ( ( idx + 1 ) * offset ) if idx + 1 < parts else len( array )
		results[ idx ] = array[ start : end ]
	return results


def split_dict( d, parts ):
	keys_split = split_array( d.keys(), parts )
	split = []
	for keys in keys_split:
		split.append( { key: d[ key ] for key in keys } )
	return split
