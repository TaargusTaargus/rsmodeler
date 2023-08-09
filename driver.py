#!/usr/bin/python
import argparse
import datetime
from etl import extract, transform
from sys import argv, exit

def main():
    parser = argparse.ArgumentParser( description='''Runescape API extract, load, and transform shell tool.''' )

    # Add command-line options
    parser.add_argument( "database_name", help="Specify the name of an output database." )
    parser.add_argument( "-d", "--day",  help="Request a particular day of history." )

    # Parse the command-line arguments
    args = parser.parse_args()

    extract( args.database_name, day = args.day )
    transform( args.database_name )

if __name__ == "__main__":
    main()



