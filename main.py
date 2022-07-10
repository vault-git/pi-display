#!/usr/bin/env python3

import sys
import cairosvg
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageOps
import waveshare.epd7in5_V2 as epd7in5

import util
import constants as const
import dht
import weather_data
import crypto_price

MODULE_0_POS = (0, 0)
MODULE_1_POS = (400, 0)
MODULE_2_POS = (0, 240)
MODULE_3_POS = (400, 240)

def create_time_module():
    current_time = datetime.now()

    module = Image.new('1', const.MODULE_SIZE, 1)
    draw = ImageDraw.Draw(module)

    draw.text((120, 70), current_time.strftime("%H:%M"), font=util.load_font(56))
    draw.text((120 + 8, 70 + 60), current_time.strftime("%d.%m.%y"), font=util.load_font(32))

    module = ImageOps.expand(module, border=2)

    return module

def draw_timestamp(draw, xy):
    current_time = datetime.now()
    draw.text(xy, current_time.strftime("%H:%M %d.%m.%y"), font=util.load_font(12))

def draw_to_display_and_sleep(image):
    try:
        # init the display
        epd = epd7in5.EPD()
        epd.init()
        # epd.Clear()

        # draw the image to the display
        epd.display(epd.getbuffer(image))

        # go to deep sleep mode
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd7in5.epdconfig.module_exit()
        exit()

def main():
    img = Image.new('1', (const.SCREEN_W, const.SCREEN_H), 1)
    draw = ImageDraw.Draw(img)

    # all modules (except for weather) have the same size (400, 240)
    img.paste(dht.create_module(), MODULE_0_POS)
    img.paste(crypto_price.create_module(), MODULE_1_POS)
    img.paste(weather_data.create_module(), MODULE_2_POS)

    draw_timestamp(draw, (700, 465))

    draw_to_display_and_sleep(img)

if __name__ == '__main__':
    main()
