#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageOps
import constants as const
import util

# For these two files to exist, the dht11 kernel module needs to be loaded.
# To enable the module add the following line to the /boot/config.txt
#
# dtoverlay=dht11,gpiopin=4
#
# where the pin is the pin of the dht data line
#
TEMP_PATH = '/sys/bus/iio/devices/iio\:device0/in_temp_input'
HUMID_PATH = '/sys/bus/iio/devices/iio\:device0/in_humidityrelative_input'

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
        temp = int(read_file(TEMP_PATH)) / 10
    except ValueError:
        return { 'success' : False }

    try:
        humid = int(read_file(HUMID_PATH)) / 10
    except ValueError:
        return { 'success' : False }

    return { 'success' : True, 'temp' : temp, 'humid' : humid }

# creates the dht 'module' that can be pasted to the main image
def create_module():
    dht_data = get_dht_data()

    module = Image.new('1', const.MODULE_SIZE, 1)
    draw = ImageDraw.Draw(module)

    if dht_data['success'] == True:
        draw.text((130, 70), "{0}°C\n{1}%".format(dht_data['temp'], dht_data['humid']), font=util.load_font(40))
    else:
        draw.text((20, 20), 'Could not gather dht data!', font=util.load_font(20))

    # add a border to the image
    module = ImageOps.expand(module, border=2)

    return module
