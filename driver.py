#!/usr/bin/python
from etl import extract, transform
from sys import argv, exit

if len( argv ) <> 3:
    print( "Incorrect Number of Arguments, Exitting ..." )
    exit( 0 )

filename = argv[ 1 ]
config = argv[ 2 ]
extract( filename, config )
transform( filename )
