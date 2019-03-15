from Adafruit_IO import Client
aio = Client('adriangamador', '936cda57b84f404ab7b883364fba3b6e')
import board
import busio
import adafruit_tsl2591
import adafruit_bme280
import adafruit_veml6075
import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

i2c = busio.I2C(board.SCL, board.SDA)
veml = adafruit_veml6075.VEML6075(i2c, integration_time=800)
lux = adafruit_tsl2591.TSL2591(i2c)
lux.GAIN_LOW
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

def out_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def out_temp():
    lines = out_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

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
    pressure = bme280.pressure
    return temperature, humidity, pressure


def log_data():
    UV_index, UV_A, UV_B = uv_read()
    light_level, visible_light, infrared = lux_read()
    temperature, humidity, pressure = bme_read()
    out_temp_c, out_temp_f = out_temp()
    aio.send('uv-index', UV_index)
    aio.send('uv-a', UV_A)
    aio.send('uv-b', UV_B)
    aio.send('lux', visible_light)
    aio.send('indoor-temperature', temperature)
    aio.send('indoor-humidity', humidity)
    aio.send('indoor-pressure', pressure)
    aio.send('outdoor-temperature', out_temp_f)
    print('success')

log_data()
