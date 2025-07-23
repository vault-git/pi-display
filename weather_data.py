#!/usr/bin/env python3

import requests
import datetime
import util
import logging
import constants as const
from datetime import datetime
from PIL import Image, ImageDraw

TODAY = 0
TOMORROW = 1
DAY_AFTER_TOMORROW = 2

DAILY_IMG_W = 200

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def get_parameters(location):
    return {
            'latitude':location[0],
            'longitude':location[1],
            'current':'temperature_2m,wind_speed_10m',
            'daily':'weather_code,temperature_2m_max,temperature_2m_min',
            'timezone':'Europe/Berlin',
            'forecast_days':'3'
            }

# tries to get the weather data from the open-meteo API
def get_weather_data(location):
    try:
        result = requests.get(WEATHER_API_URL, get_parameters(location))
        result.raise_for_status() # raises exception when http status code is error

        return result.json()

    except requests.ConnectionError:
        logging.error("error connecting to weather API")
    except requests.HTTPError:
        logging.error("weather API returned error code")

def get_icon_for_code(code):
    icon_scale = 4
    code = str(code)

    if code in ('0'):
        return util.load_icon('data/image/wi-day-sunny.svg', icon_scale)
    if code in ('1', '2', '3'):
        return util.load_icon('data/image/wi-day-cloudy.svg', icon_scale)
    if code in ('45', '48'):
        return util.load_icon('data/image/wi-fog.svg', icon_scale)
    if code in ('51', '53', '55'):
        return util.load_icon('data/image/wi-sprinkle.svg', icon_scale)
    if code in ('61', '63', '65'):
        return util.load_icon('data/image/wi-rain-mix.svg', icon_scale)
    if code in ('71', '73', '75', '85', '86'):
        return util.load_icon('data/image/wi-snow.svg', icon_scale)
    if code in ('80', '81', '82'):
        return util.load_icon('data/image/wi-showers.svg', icon_scale)
    if code in ('95', '96', '99'):
        return util.load_icon('data/image/wi-storm-showers.svg', icon_scale)

    return util.load_icon('data/image/wi-na.svg', icon_scale)

def parse_current_weather(data):
    return [data['current']['temperature_2m'],
            data['current']['wind_speed_10m']]

def parse_daily_weather(data, day):
    daily = data['daily']

    # ['2022-07-08', 3, 20.4, 11.4]
    return [daily['time'][day],
            daily['weather_code'][day],
            daily['temperature_2m_min'][day],
            daily['temperature_2m_max'][day]]

def create_current_image(data):
    img = Image.new('1', (DAILY_IMG_W, const.MODULE_H), 1)
    draw = ImageDraw.Draw(img)

    draw.text((0, 40), '{:.0f}°'.format(data[0]).center(8), font=util.load_font(48))
    draw.text((0, 140), '{:.0f} km/h'.format(data[1]).center(10), font=util.load_font(38))

    return img

def create_daily_image(data):
    img = Image.new('1', (DAILY_IMG_W, const.MODULE_H), 1)
    draw = ImageDraw.Draw(img)

    draw.text((0, 10), datetime.strptime(data[0], '%Y-%m-%d').strftime('%A').center(16), font=util.load_font(20))

    today_icon = get_icon_for_code(data[1])
    img.paste(today_icon, box=(42, 40), mask=today_icon)

    draw.text((0, 170), '{:.0f}° | {:.0f}°'.format(data[2], data[3]).center(11), font=util.load_font(30))

    return img

def create_module(config):
    location = config['location']

    if config['test_mode']:
        location = (48.1549958,11.4594364) # munich

    weather_data = get_weather_data(location)

    current_img = create_current_image(parse_current_weather(weather_data))
    today_img = create_daily_image(parse_daily_weather(weather_data, TODAY))
    tomorrow_img = create_daily_image(parse_daily_weather(weather_data, TOMORROW))
    day_after_tomorrow_img = create_daily_image(parse_daily_weather(weather_data, DAY_AFTER_TOMORROW))

    module = Image.new('1', (const.SCREEN_W, const.MODULE_H), 1)

    module.paste(today_img, box=(DAILY_IMG_W, 0))
    module.paste(tomorrow_img, box=(2 * DAILY_IMG_W, 0))
    module.paste(day_after_tomorrow_img, box=(3 * DAILY_IMG_W, 0))
    module.paste(current_img, box=(0, 0))

    return module
