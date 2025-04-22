import sqlite3
import csv

con = sqlite3.connect('database.db')
outfile = open('dump.csv', 'w', newline='')
outcsv = csv.writer(outfile)

cursor = con.execute('select * from items')

# dump column titles
outcsv.writerow(x[0] for x in cursor.description)
# dump rows
outcsv.writerows(cursor.fetchall())

outfile.close()