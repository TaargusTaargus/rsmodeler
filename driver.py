#!/usr/bin/python
import argparse
from constants import ALPHABET_DEFAULT, DAY_DEFAULT, OPTIONS_DEFAULT, END_PAGE_DEFAULT, MEMBERS_DEFAULT, REQUEST_TIMER_DEFAULT, RESOLVE_MATERIALS_DEFAULT, START_PAGE_DEFAULT, VERBOSE_DEFAULT
import datetime
from etl import RSModelerETL
from sys import argv, exit

def main():
    parser = argparse.ArgumentParser( description='''Runescape API extract, load, and transform shell tool.''' )

    # Add command-line options
    parser.add_argument( "database_name", help="Specify the name of an output database (ex: tmp.db)." )
    parser.add_argument( "-d", "--day",  help="Request a particular day of history in SQL format (ex: '2023-01-01') -- defaults to as many days as possible." )
    parser.add_argument( "-a", "--alpha", help="Request a particular set of letters to be searched as a string (ex: 'abcz') -- defaults to entire alphabet." )
    parser.add_argument( "-e", "--end", type=int, help="Specify the ending page to extract items from (ex: 1) -- defaults to as many as are available." )
    parser.add_argument( "-m", "--members", action="store_true", help="Flag to request to return only members items -- defaults to FALSE." )
    parser.add_argument( "-s", "--start", type=int, help="Specify the starting page to extract items from (ex: 3) -- defaults to 1." )   
    parser.add_argument( "-v", "--verbose", type=int, help="Flag to request verbose output (0 = basic output, 1 = basic debugging, 2 = advanced debugging -- defaults to 0." )
    parser.add_argument( "-r", "--materials", action="store_true", help="Flag to request that required materials are resolved on top of catalogued items -- defaults to FALSE." )
    parser.add_argument( "-t", "--timer", type=int, help="Specify the request timer on call to OSRS API, API will reject calls that are too fast in succession -- defaults to 3 seconds" )

    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Create options dictionary
    options = OPTIONS_DEFAULT
    for arg_name, arg_value in vars( args ).items():
    	if arg_value:
    		options[ arg_name ] = arg_value

    # Create an ETL object
    etl = RSModelerETL( args.database_name, options )
    etl.execute()

if __name__ == "__main__":
    main()



