#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  logDHT.py
#
#  Developed by Marcelo Rovai, MJRoBot.org @ 10Jan18
#
#  Capture data from a DHT22 sensor and save it on a database

import time
import sqlite3
from Adafruit_IO import Client


dbname='sensorsData.db'
sampleFreq = 60 # time in seconds

# get data from adafruit.io
indoor_temp = aio.receive('indoor-temperature')
indoor_temp = indoor_temp.value
indoor_humidity = aio.receive('indoor-humidity')
indoor_humidity = indoor_humidity.value
indoor_pressure = aio.receive('indoor-pressure')
indoor_pressure = indoor_pressure.value
lux = aio.receive('lux')
lux = lux.value
outdoor_temp = aio.receive('outdoor-temperature')
outdoor_temp = outdoor_temp.value
uva = aio.receive('uv-a')
uva = uva.value
uvb = aio.receive('uv-b')
uvb = uvb.value
uv_index = aio.receive('uv-index')
uv_index = uv_index.value


conn=sqlite3.connect(dbname)
curs=conn.cursor()

try:
	curs.execute("INSERT INTO lux values(datetime('now'), (?))", (lux,))

except:
	pass

try:
	curs.execute("INSERT INTO veml values(datetime('now'), (?), (?), (?))", (uva, uvb, uv_index,))

except:
	pass

try:
	curs.execute("INSERT INTO bme values(datetime('now'), (?), (?), (?))", (indoor_temp, indoor_humidity, indoor_pressure,))

except:
	pass

try:
	curs.execute("INSERT INTO outdoor values(datetime('now'), (?))", (outdoor_temp,))

except:
	pass


conn.commit()
conn.close()
