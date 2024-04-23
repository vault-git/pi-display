#!/usr/bin/env python3

from PIL import Image, ImageDraw
import constants as const
from datetime import datetime
import util

# For these two files to exist, the dht11 kernel module needs to be loaded.
# To enable the module add the following line to the /boot/config.txt
#
# dtoverlay=dht11,gpiopin=4
#
# where the pin is the pin of the dht data line

TEMP_PATH = r'/sys/bus/iio/devices/iio:device0/in_temp_input'
HUMID_PATH = r'/sys/bus/iio/devices/iio:device0/in_humidityrelative_input'

def read_file(filepath):
    try:
        f = open(filepath, 'r')
    except (FileNotFoundError, IOError):
        return ''
    else:
        with f:
            return f.read()

def get_dht_data():
    temp = 0.0
    humid = 0.0

    try:
        temp = int(read_file(TEMP_PATH)) / 1000
    except ValueError:
        print('temp could not be read')
        return { 'success' : False }

    try:
        humid = int(read_file(HUMID_PATH)) / 1000
    except ValueError:
        print('humid could not be read')
        return { 'success' : False }

    return { 'success' : True, 'temp' : temp, 'humid' : humid, 'timestamp' : datetime.now().isoformat() }

# creates the dht 'module' that can be pasted to the main image
def create_module():
    dht_data = get_dht_data()

    module = Image.new('1', const.MODULE_SIZE, 1)
    draw = ImageDraw.Draw(module)

    if dht_data['success'] == True:
        draw.text((0, 55), '{}°'.format(dht_data['temp']).center(13), font=util.load_font(50))
        draw.text((0, 80), '{}%'.format(dht_data['humid']).center(13), font=util.load_font(50))
    else:
        draw.text((30, 100), 'Could not gather dht data!', font=util.load_font(20))

    return module
