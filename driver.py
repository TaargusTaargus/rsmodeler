#!/usr/bin/python
import argparse
from constants import ALPHABET_DEFAULT, DAY_DEFAULT, MAX_PAGE_DEFAULT, MEMBERS_DEFAULT, REQUEST_TIMER_DEFAULT, VERBOSE_DEFAULT
import datetime
from etl import extract, transform
from sys import argv, exit

def main():
    parser = argparse.ArgumentParser( description='''Runescape API extract, load, and transform shell tool.''' )

    # Add command-line options
    parser.add_argument( "database_name", help="Specify the name of an output database (ex: tmp.db)." )
    parser.add_argument( "-d", "--day",  help="Request a particular day of history in SQL format (ex: '2023-01-01') -- defaults to as many days as possible." )
    parser.add_argument( "-a", "--alpha", help="Request a particular set of letters to be searched as a string (ex: 'abcz') -- defaults to entire alphabet." )
    parser.add_argument( "-p", "--pages", help="Request a limit on pages returned from API (ex: 1) -- defaults to as many as are available." )
    parser.add_argument( "-m", "--members", action="store_true", help="Flag to request to return only members items -- defaults to FALSE." )
    parser.add_argument( "-v", "--verbose", action="store_true", help="Flag to request verbose output -- defaults to FALSE." )

    # Parse the command-line arguments
    args = parser.parse_args()
    
    extract( 
    	args.database_name
        , alphabet = args.alpha if args.alpha else ALPHABET_DEFAULT
    	, day = args.day if args.day else DAY_DEFAULT
    	, max_page = int( args.pages ) if args.pages else MAX_PAGE_DEFAULT
    	, members = args.members if args.members else MEMBERS_DEFAULT
    	, verbose = args.verbose if args.verbose else VERBOSE_DEFAULT
    )
    transform( args.database_name )

if __name__ == "__main__":
    main()



