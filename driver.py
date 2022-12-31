#!/usr/bin/python
from etl import extract, transform
from sys import argv, exit

if len( argv ) <> 2:
    print( "Incorrect Number of Arguments, Exitting ..." )
    exit( 0 )

filename = argv[ 1 ]
extract( filename )
transform( filename )
