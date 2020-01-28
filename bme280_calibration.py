import time
import board
import busio
import adafruit_bme280
from influxdb import InfluxDBClient
import RPi.GPIO as GPIO

clientweb = InfluxDBClient(host='67.205.147.13', port=8086, username='admin', password='Imadog22')
clientweb.switch_database('sensordb')

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.HIGH)

try:
    i2c = busio.I2C(board.SCL, board.SDA)
    bme = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    humidity = bme.humidity
    humidity = round(humidity, 1)
    temperature = bme.temperature
    temperature = round((temperature*(9/5)+32), 1)
except:
    print("Could not retrieve data")

datapoints = [
    {
        "measurement": "temperature",
        "tags": {
            "device": "BME280",
            "location": "calibration"
        },
        "fields": {
            "value": float(temperature)
        }
    },
    {
        "measurement": "humidity",
        "tags": {
            "device": "BME280",
            "location": "calibration"
        },
        "fields": {
            "value": float(humidity)
        }
    }
    ]
try:
    clientweb.write_points(datapoints)
    print('success')
except:
    print("Couldn't write to influxdb")
    pass

