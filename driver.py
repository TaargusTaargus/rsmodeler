#!/usr/bin/python
import argparse
from constants import ALPHABET_DEFAULT, DAY_DEFAULT, END_PAGE_DEFAULT, MEMBERS_DEFAULT, REQUEST_TIMER_DEFAULT, START_PAGE_DEFAULT, VERBOSE_DEFAULT
import datetime
from etl import RSModelerETL
from sys import argv, exit

def main():
    parser = argparse.ArgumentParser( description='''Runescape API extract, load, and transform shell tool.''' )

    # Add command-line options
    parser.add_argument( "database_name", help="Specify the name of an output database (ex: tmp.db)." )
    parser.add_argument( "-d", "--day",  help="Request a particular day of history in SQL format (ex: '2023-01-01') -- defaults to as many days as possible." )
    parser.add_argument( "-a", "--alpha", help="Request a particular set of letters to be searched as a string (ex: 'abcz') -- defaults to entire alphabet." )
    parser.add_argument( "-e", "--end", help="Specify the ending page to extract items from (ex: 1) -- defaults to as many as are available." )
    parser.add_argument( "-m", "--members", action="store_true", help="Flag to request to return only members items -- defaults to FALSE." )
    parser.add_argument( "-s", "--start", help="Specify the starting page to extract items from (ex: 3) -- defaults to 1." )   
    parser.add_argument( "-v", "--verbose", help="Flag to request verbose output (0 = basic output, 1 = basic debugging, 2 = advanced debugging -- defaults to 0." )
    parser.add_argument( "-t", "--timer", help="Specify the request timer on call to OSRS API, API will reject calls that are too fast in succession -- defaults to 3 seconds" )

    # Parse the command-line arguments
    args = parser.parse_args()
   
    # Create options dictionary
    options = {
    	"ALPHABET": args.alpha if args.alpha else ALPHABET_DEFAULT
    	, "DAY": args.day if args.day else DAY_DEFAULT
    	, "END_PAGE": int( args.end ) if args.end else END_PAGE_DEFAULT
    	, "MEMBERS": args.members if args.members else MEMBERS_DEFAULT
    	, "REQUEST_TIMER": args.timer if args.timer else VERBOSE_DEFAULT
    	, "START_PAGE": int( args.start ) if args.start else START_PAGE_DEFAULT  
    	, "VERBOSE": int( args.verbose ) if args.verbose else VERBOSE_DEFAULT
    }

    # Create an ETL object
    etl = RSModelerETL( args.database_name, options )
    etl.execute()

if __name__ == "__main__":
    main()



