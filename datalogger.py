from Adafruit_IO import Client
aio = Client('adriangamador', '936cda57b84f404ab7b883364fba3b6e')
import board
import busio
import adafruit_tsl2591
import adafruit_bme280
import adafruit_veml6075

i2c = busio.I2C(board.SCL, board.SDA)
veml = adafruit_veml6075.VEML6075(i2c, integration_time=800)
lux = adafruit_tsl2591.TSL2591(i2c)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

def uv_read():
    UV_index = veml.uv_index
    UV_A = veml.uva
    UV_B = veml.uvb
    return UV_index, UV_A, UV_B

def lux_read():
    light_level = lux.lux
    visible_light = lux.visible
    infrared = lux.infrared
    return light_level, visible_light, infrared

def bme_read():
    temperature = bme280.temperature * 1.8 + 32
    humidity = bme280.humidity
    pressure = bme.pressure
    return temperature, humidity, pressure


def log_data():
    UV_index, UV_A, UV_B = uv_read()
    light_level, visible_light, infrared = lux_read()
    temperature, humidity, pressure = bme_read()
    aio.send('uv-index', UV_index)
    aio.send('uv-a', UV_A)
    aio.send('uv-b', UV_B)
    aio.send('lux', visible_light)
    aio.send('indoor-temperature', temperature)
    aio.send('indoor-humidity', humidity)
    aio.send('indoor-pressure', pressure)
    print('success')

log_data()
