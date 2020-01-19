import time
import Adafruit_DHT
from influxdb import InfluxDBClient

clientweb = InfluxDBClient(host='67.205.147.13', port=8086, username='admin', password='Imadog22')
clientweb.switch_database('sensordb')

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

try:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    humidity = round(humidity, 1)
    temperature = round((temperature*(9/5)+32), 1)
except:
    print("Could not retrieve data")

datapoints = [
    {
        "measurement": "temperature",
        "tags": {
            "device": "DHT22",
            "location": "calibration"
        },
        "fields": {
            "value": float(temperature)
        }
    },
    {
        "measurement": "humidity",
        "tags": {
            "device": "DHT22",
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

