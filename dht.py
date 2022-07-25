#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageOps
from os.path import exists
import constants as const
from datetime import datetime
import json
import util

# For these two files to exist, the dht11 kernel module needs to be loaded.
# To enable the module add the following line to the /boot/config.txt
#
# dtoverlay=dht11,gpiopin=4
#
# where the pin is the pin of the dht data line
#
TEMP_PATH = r'/sys/bus/iio/devices/iio:device0/in_temp_input'
HUMID_PATH = r'/sys/bus/iio/devices/iio:device0/in_humidityrelative_input'

DHT_VALUES_JSON = r'dht_values.json'

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

def get_min_max_json():
    return { 'temp' : { 'min' : 100, 'min_t' : '',
                        'max' : -100, 'max_t' : ''},
             'humid' : { 'min' : 100, 'min_t' : '',
                         'max' : 0, 'max_t' : '' }}

def has_isoformat_date_changed(timestamp1, timestamp2):
    return datetime.fromisoformat(timestamp1).date() != datetime.fromisoformat(timestamp2).date()

def update_and_get_min_max_values(dht_data):
    with open(DHT_VALUES_JSON, 'a+') as f:
        f.seek(0)

        try:
            dhtjson = json.loads(f.read())
        except json.JSONDecodeError:
            dhtjson = json.loads(json.dumps(get_min_max_json()))
        finally:
            temp = dhtjson['temp']
            if (dht_data['temp'] < temp['min'] or
                has_isoformat_date_changed(temp['min_t'], dht_data['timestamp'])):
                temp['min'] = dht_data['temp']
                temp['min_t'] = dht_data['timestamp']

            if (dht_data['temp'] > temp['max'] or
                has_isoformat_date_changed(temp['max_t'], dht_data['timestamp'])):
                temp['max'] = dht_data['temp']
                temp['max_t'] = dht_data['timestamp']

            humid = dhtjson['humid']
            if (dht_data['humid'] < humid['min'] or
                has_isoformat_date_changed(humid['min_t'], dht_data['timestamp'])):
                humid['min'] = dht_data['humid']
                humid['min_t'] = dht_data['timestamp']

            if (dht_data['humid'] > humid['max'] or
                has_isoformat_date_changed(humid['max_t'], dht_data['timestamp'])):
                humid['max'] = dht_data['humid']
                humid['max_t'] = dht_data['timestamp']

            f.truncate(0)
            f.write(json.dumps(dhtjson))

            return dhtjson

def datetime_hours_minutes(timestamp):
    return datetime.fromisoformat(timestamp).strftime('%H:%M')

def draw_min_max_text(draw_context, min_max_values):
    temp = min_max_values['temp']
    draw_context.text((10, 130), "{0}° at {1}"
                      .format(temp['min'], datetime_hours_minutes(temp['min_t'])), font=util.load_font(20))
    draw_context.text((10, 160), "{0}° at {1}"
                      .format(temp['max'], datetime_hours_minutes(temp['max_t'])), font=util.load_font(20))
    humid = min_max_values['humid']
    draw_context.text((220, 130), "{0}% at {1}"
                      .format(humid['min'], datetime_hours_minutes(humid['min_t'])), font=util.load_font(20))
    draw_context.text((220, 160), "{0}% at {1}"
                      .format(humid['max'], datetime_hours_minutes(humid['max_t'])), font=util.load_font(20))


# creates the dht 'module' that can be pasted to the main image
def create_module():
    dht_data = get_dht_data()

    min_max_values = update_and_get_min_max_values(dht_data)

    module = Image.new('1', const.MODULE_SIZE, 1)
    draw = ImageDraw.Draw(module)

    if dht_data['success'] == True:
        draw.text((40, 50), "{0}°  {1}%".format(dht_data['temp'], dht_data['humid']), font=util.load_font(44))
        draw_min_max_text(draw, min_max_values)
    else:
        draw.text((30, 200), 'Could not gather dht data!', font=util.load_font(20))

    # add a border to the image
    module = ImageOps.expand(module, border=2)

    return module
