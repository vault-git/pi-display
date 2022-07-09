#!/usr/bin/env python3

import sys
import cairosvg
import util
import constants as const
import weather_data as weather
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw

def draw_ui(draw_context):
    dist = 20
    half_height = const.SCREEN_H / 2
    half_width = const.SCREEN_W / 2
    draw_context.line([(half_width, dist), (half_width, half_height)], fill=1, width=2)
    draw_context.line([(dist, half_height), (const.SCREEN_W - dist, half_height)], fill=1, width=2)

def get_and_draw_time(draw_context, xy = (0, 0)):
    current_time = datetime.now()
    draw_context.text((xy[0], xy[1]), current_time.strftime("%H:%M"), font=const.FONT_56, fill=1)
    draw_context.text((xy[0] + 7, xy[1] + 60), current_time.strftime("%d.%m.%y"), font=const.FONT_32, fill=1)

def get_and_draw_dht_data(draw_context, xy = (0, 0)):
    temp = 275 # comes from the sensor
    humid = 455 # comes from the sensor
    draw_context.text((xy[0], xy[1]),
                      "{0}°C\n{1}%".format(temp / 10, humid / 10),
                      font=const.FONT_40,
                      fill=1)

def main():
    img = Image.new('1', (const.SCREEN_W, const.SCREEN_H), 0)
    draw = ImageDraw.Draw(img)

    draw_ui(draw)
    get_and_draw_time(draw, (120, 60))
    get_and_draw_dht_data(draw, (530, 65))
    img.paste(weather.create_weather_image(), box=(0, 250))

    img.show()

if __name__ == '__main__':
    main()
