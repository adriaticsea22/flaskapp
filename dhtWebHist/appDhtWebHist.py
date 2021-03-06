#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  appDHT_v1.py
#
#  Created by MJRoBot.org
#  10Jan18

'''
	RPi WEb Server for DHT captured data with Graph plot
'''

import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import dates
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import io
import datetime

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('../sensorsData.db')
curs=conn.cursor()

# Retrieve LAST data from database
def getLastData():
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1] * 1.8 + 32
		hum = row[2]
	for row in curs.execute("SELECT * FROM circuit_data ORDER BY timestamp DESC LIMIT 1"):
		light = row[1]
	#conn.close()
	return time, temp, hum, light


def getHistData (numSamples):
	curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	for row in reversed(data):
		dates.append(row[0])
		temps.append(row[1] * 1.8 + 32)
		hums.append(row[2])
	return dates, temps, hums

def getHistDataCircuit (numSamplesCircuit):
	curs.execute("SELECT * FROM circuit_data ORDER BY timestamp DESC LIMIT "+str(numSamplesCircuit))
	data = curs.fetchall()
	dates2 = []
	lights = []
	for row in reversed(data):
		dates2.append(row[0])
		lights.append(row[1])
	return dates2, lights

def maxRowsTable():
	for row in curs.execute("select COUNT(temp) from  DHT_data"):
		maxNumberRows=row[0]
	return maxNumberRows

def maxRowsTableCircuit():
	for row in curs.execute("select COUNT(light) from  circuit_data"):
		maxNumberRowsCircuit=row[0]
	return maxNumberRowsCircuit

#initialize global variables
global numSamples, numSamplesCircuit
numSamples = maxRowsTable()
numSamplesCircuit = maxRowsTableCircuit()
if (numSamples > 101):
	numSamples = 100
if (numSamplesCircuit > 101):
	numSamplesCircuit = 100


# main route
@app.route("/")
def index():

	time, temp, hum, light = getLastData()
	templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum,
	  'light'		: light,
      'numSamples'	: numSamples,
	  'numSamplesCircuit' : numSamplesCircuit
	}
	return render_template('index.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
	global numSamples, numSamplesCircuit
	numSamples = int(request.form['numSamples'])
	numSamplesCircuit = numSamples
	numMaxSamples = maxRowsTable()
	numMaxSamplesCircuit = maxRowsTableCircuit()
	if (numSamples > numMaxSamples):
		numSamples = (numMaxSamples-1)
	if (numSamplesCircuit > numMaxSamplesCircuit):
		numSamplesCircuit = (numMaxSamplesCircuit -1)

	time, temp, hum, light = getLastData()

	templateData = {
	'time'		: time,
	'temp'		: temp,
	'hum'			: hum,
	'light'		: light,
	'numSamples'	: numSamples,
	'numSamplesCircuit' : numSamplesCircuit
	}
	return render_template('index.html', **templateData)


@app.route('/plot/temp')
def plot_temp():
	times, temps, hums = getHistData(numSamples)
	ys = temps
	timec = []
	for thing in times:
		timec.append(datetime.datetime.strptime(thing, "%Y-%m-%d %H:%M:%S"))

	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [°F]")
	axis.set_xlabel("Time of day")
	axis.grid(True)

	xs = timec
	plt.setp(axis.xaxis.get_majorticklabels(), rotation=90)
#	plt.gcf().subplots_adjust(bottom=0.25)
	axis.plot(xs, ys)
#	axis.set_xticklabels(rotation=45)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/hum')
def plot_hum():
	times, temps, hums = getHistData(numSamples)
	ys = hums
	timec = []
	for thing in times:
		timec.append(datetime.datetime.strptime(thing, "%Y-%m-%d %H:%M:%S"))
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity [%]")
	axis.set_xlabel("Time of day")
	axis.grid(True)
	xs = timec
	plt.setp(axis.xaxis.get_majorticklabels(), rotation=90)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/light')
def plot_light():

	times, lights = getHistDataCircuit(numSamplesCircuit)
	ys = lights
	timec = []
	for thing in times:
		timec.append(datetime.datetime.strptime(thing, "%Y-%m-%d %H:%M:%S"))
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Light level")
	axis.set_xlabel("Time of day")
	axis.grid(True)
	xs = timec
	plt.setp(axis.xaxis.get_majorticklabels(), rotation=90)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)
