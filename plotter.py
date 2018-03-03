from db import ByItemTable, ItemSummaryTable
import matplotlib.pyplot as plt

DB_NAME = "db/item.db"

by_item = ByItemTable( DB_NAME )
item_summary = ItemSummaryTable( DB_NAME )

selection, columns = by_item.select( 
        keys=[ "name", "timestamp", "price" ], 
        where={ "name": "Iron sword" },
        orderby=[ "timestamp" ]
)
time = [ el[ 1 ] for el in selection ]
price = [ el[ 2 ] for el in selection ]

plt.plot( time, price )

plt.xlabel('time (ms)')
plt.ylabel('price')
plt.title( selection[ 0 ][ 0 ] + ' Price Plot' )
plt.grid( True )
plt.savefig( selection[ 0 ][ 0 ] + '.png' )
plt.show()

