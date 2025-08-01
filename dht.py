#!/usr/bin/env python3

from datetime import datetime
import logging

from PIL import Image, ImageDraw

import constants as const
import util

# For these two files to exist, the dht11 kernel module needs to be loaded.
# To enable the module add the following line to the /boot/config.txt
#
# dtoverlay=dht11,gpiopin=4
#
# where the pin is the pin of the dht data line

TEMP_PATH = r"/sys/bus/iio/devices/iio:device0/in_temp_input"
HUMID_PATH = r"/sys/bus/iio/devices/iio:device0/in_humidityrelative_input"


def read_file(filepath):
    try:
        f = open(filepath, "r")
    except (FileNotFoundError, IOError):
        return ""
    else:
        with f:
            return f.read()


def get_dht_data(config):
    temp = 0.0
    humid = 0.0

    if config["test_mode"]:
        return {
            "success": True,
            "temp": 22.5,
            "humid": 65.1,
            "timestamp": datetime.now().isoformat(),
        }

    try:
        temp = int(read_file(TEMP_PATH)) / 1000
    except ValueError:
        logging.error("temp could not be read")
        return {"success": False}

    try:
        humid = int(read_file(HUMID_PATH)) / 1000
    except ValueError:
        logging.error("humid could not be read")
        return {"success": False}

    return {
        "success": True,
        "temp": temp,
        "humid": humid,
        "timestamp": datetime.now().isoformat(),
    }


# creates the dht 'module' that can be pasted to the main image
def create_module(config):
    module = Image.new("1", (260, const.MODULE_H), 1)
    draw = ImageDraw.Draw(module)

    dht_data = get_dht_data(config)

    if dht_data["success"]:
        draw.text(
            xy=(38, 80),
            text=" {}°\n {}%".format(dht_data["temp"], dht_data["humid"]),
            font=util.load_font(50),
        )
    else:
        draw.text((10, 100), "Could not gather dht data!", font=util.load_font(20))

    return module
