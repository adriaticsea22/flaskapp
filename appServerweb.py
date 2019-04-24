#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  appServer.py


'''
	RPi Web Server for captured sensor data
'''

from flask import Flask, render_template, request
app = Flask(__name__)


# main route 
@app.route("/")
def index():
	
	return render_template('indexweb.html')


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)

