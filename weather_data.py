#!/usr/bin/env python3

import requests
import util
import logging
import constants as const
from datetime import datetime
from PIL import Image, ImageDraw, ImageOps

TODAY = 0
TOMORROW = 1
DAY_AFTER_TOMORROW = 2

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast?latitude=49.23&longitude=12.67&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset&timezone=Europe%2FBerlin"

# tries to get the weather data from the open-meteo API
def get_weather_data():
    try:
        result = requests.get(WEATHER_API_URL)
        result.raise_for_status() # raises exception when http status code is error

        return result.json()

    except requests.ConnectionError:
        logging.error("error connecting to weather API")
    except requests.HTTPError:
        logging.error("weather API returned error code")

def get_icon_for_code(code):
    icon_scale = 3

    # should be replaced with 'match' when python 3.10 is available
    if code == 0:
        return util.load_icon('data/image/sun.svg', icon_scale)
    if code == 1 or code == 2 or code == 3:
        return util.load_icon('data/image/cloud.svg', icon_scale)
    if code == 51 or code == 53 or code == 55:
        return util.load_icon('data/image/cloud-drizzle.svg', icon_scale)
    if code == 61 or code == 63 or code == 65:
        return util.load_icon('data/image/cloud-rain.svg', icon_scale)
    if code == 71 or code == 73 or code == 75:
        return util.load_icon('data/image/cloud-snow.svg', icon_scale)
    if code == 95 or code == 96 or code == 99:
        return util.load_icon('data/image/cloud-lightning.svg', icon_scale)

    return util.load_icon('data/image/wi-na.svg', icon_scale)

def parse_weather_data(data, day):
    daily = data['daily']

    # ['2022-07-08', 3.0, '2022-07-08T05:11', '2022-07-08T21:17', 9.7, 20.4]
    return [daily['time'][day],
            daily['weathercode'][day],
            daily['sunrise'][day],
            daily['sunset'][day],
            daily['temperature_2m_min'][day],
            daily['temperature_2m_max'][day]]

def create_weather_image_day(daily_data):
    img = Image.new('1', (230, 200), 1)
    draw = ImageDraw.Draw(img)

    today_icon = get_icon_for_code(daily_data[1])
    img.paste(today_icon, box=(15, 15), mask=today_icon)

    sunrise_icon = util.load_icon('data/image/sunrise.svg', 1)
    img.paste(sunrise_icon, box=(150, 10), mask=sunrise_icon)
    sunrise_time = datetime.fromisoformat(daily_data[2]).strftime('%H:%M')
    draw.text((145, 50), sunrise_time, font=const.FONT_16)

    sunset_icon = util.load_icon('data/image/sunset.svg', 1)
    img.paste(sunset_icon, box=(150, 80), mask=sunset_icon)
    sunset_time = datetime.fromisoformat(daily_data[3]).strftime('%H:%M')
    draw.text((145, 120), sunset_time, font=const.FONT_16)

    draw.text((5, 150), '{0}°C {1}°C'.format(str(daily_data[4]), str(daily_data[5])), font=const.FONT_26)

    img = img.convert('L')
    img = ImageOps.invert(img)
    img = img.convert('1')

    return img

def create_weather_image():
    weather_data = get_weather_data()

    today_img = create_weather_image_day(parse_weather_data(weather_data, TODAY))
    tomorrow_img = create_weather_image_day(parse_weather_data(weather_data, TOMORROW))
    day_after_tomorrow_img = create_weather_image_day(parse_weather_data(weather_data, DAY_AFTER_TOMORROW))

    img = Image.new('1', (800, 240), 0)

    img.paste(today_img, box=(20, 20))
    img.paste(tomorrow_img, box=(tomorrow_img.width + 50, 20))
    img.paste(day_after_tomorrow_img, box=(2 * day_after_tomorrow_img.width + 100, 20))

    # draw seperating lines between days
    # draw = ImageDraw.Draw(img)
    # dist = 10 # distance from border
    # draw.line([(220, dist), (220, 200 - dist)], fill=1, width=1)
    # draw.line([(450, dist), (450, 200 - dist)], fill=1, width=1)

    return img
