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
import Adafruit_DHT
import serial

dbname='sensorsData.db'
sampleFreq = 60 # time in seconds

# get data from DHT sensor
def getDHTdata():

	DHT22Sensor = Adafruit_DHT.DHT22
	DHTpin = 16
	hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)

	if hum is not None and temp is not None and hum < 100:
		if hum < 100:
			hum = round(hum)
			temp = round(temp, 1)
	return temp, hum

def getCircuitdata():
	try:
		ser = serial.Serial('/dev/ttyACM0', 9600)
	except:
		try:
			ser = serial.Serial('/dev/ttyACM1', 9600)
		except:
			try:
				ser = serial.Serial('/dev/ttyACM2', 9600)
			except:
				try:
					ser = serial.Serial('/dev/ttyACM3', 9600)
				except:
					ser = serial.Serial('/dev/ttyACM4', 9600)

	ser.reset_input_buffer()
	lightlevel = float(ser.readline().decode())
	ser.close()
	return lightlevel



# log sensor data on database


temp, hum = getDHTdata()

conn=sqlite3.connect(dbname)
curs=conn.cursor()
curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
try:
	lightlevel = getCircuitdata()
	curs.execute("INSERT INTO circuit_data values(datetime('now'), (?))", (lightlevel,))
	
except:
	pass
conn.commit()
conn.close()
