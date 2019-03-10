#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  queryTableDHT.py
#
#  Developed by Marcelo Rovai, MJRoBot.org @ 9Jan18
#
# Query dada on table "DHT_data"

import sqlite3

conn=sqlite3.connect('sensorsData.db')

curs=conn.cursor()



print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM circuit_data"):
    print (row)



conn.close()
