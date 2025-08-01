#!/usr/bin/env python3

import logging
from datetime import datetime, timedelta

import requests
from PIL import Image, ImageDraw

import constants as const
import util

DAILY_IMG_W = 300
DAILY_IMG_H = 300
TODAYS_IMG_W = 500
DAY_HOUR_DISTANCE = 124

WEATHER_API_URL = "https://api.open-meteo.com/v1/dwd-icon"

TEMP = "temperature_2m"
TEMP_MIN = "temperature_2m_min"
TEMP_MAX = "temperature_2m_max"
WIND_SPEED = "wind_speed_10m"
WMO_CODE = "weather_code"
RAIN_PROB = "precipitation_probability"
RAIN_AMOUNT = "rain"
UV_INDEX = "uv_index"


def get_parameters(location):
    return {
        "latitude": location[0],
        "longitude": location[1],
        "current": "is_day,temperature_2m,wind_speed_10m,weather_code,relative_humidity_2m",
        "hourly": "temperature_2m,weather_code,precipitation_probability,rain,uv_index",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "Europe/Berlin",
        "forecast_days": "4",
    }


# tries to get the weather data from the open-meteo API
def get_weather_data(location):
    try:
        result = requests.get(WEATHER_API_URL, get_parameters(location))
        result.raise_for_status()  # raises exception when http status code is error

        logging.debug(result.json())

        return result.json()

    except requests.ConnectionError:
        logging.error("error connecting to weather API")
    except requests.HTTPError:
        logging.error("weather API returned error code")


def wmo_code_to_icon(code, is_day):
    code = str(code)

    if code in ("0"):  # Clear sky
        return "󰖨" if is_day else ""
    if code in ("1", "2", "3"):  # Mainly clear, partly cloudy, and overcast
        return "" if is_day else ""
    if code in ("45", "48"):  # Fog and depositing rime fog
        return ""
    if code in ("51", "53", "55"):  # Drizzle: Light, moderate, and dense intensity
        return ""
    if code in ("56", "57"):  # Freezing Drizzle: Light and dense intensity
        return "󰙿"
    if code in ("61", "63", "65"):  # Rain: Slight, moderate and heavy intensity
        return ""
    if code in ("66", "67"):  # Freezing Rain: Light and heavy intensity
        return "󰙿"
    if code in ("71", "73", "75"):  # Snow fall: Slight, moderate, and heavy intensity
        return ""
    if code in ("77"):  # Snow grains
        return ""
    if code in ("80", "81", "82"):  # Rain showers: Slight, moderate, and violent
        return ""
    if code in ("85", "86"):  # Snow showers slight and heavy
        return ""
    if code in ("95"):  # Thunderstorm: Slight or moderate
        return "" if is_day else ""
    if code in ("96", "99"):  # Thunderstorm with slight and heavy hail
        return "" if is_day else ""

    return ""


def create_current_weather_image(weather_data):
    img = Image.new("1", (DAILY_IMG_W, const.MODULE_H), 1)
    draw = ImageDraw.Draw(img)

    draw.text(
        xy=(20, 20),
        text="{:.0f}°".format(weather_data["current"][TEMP]),
        font=util.load_font(74),
    )
    draw.text(
        xy=(110, -55),
        text=wmo_code_to_icon(
            weather_data["current"][WMO_CODE], weather_data["current"]["is_day"]
        ),
        font=util.load_font(320),
    )
    draw.text(
        xy=(30, 170),
        text=" {:.0f} km/h\n {} %".format(
            weather_data["current"][WIND_SPEED],
            weather_data["current"]["relative_humidity_2m"],
        ),
        font=util.load_font(42),
    )

    return img


def todays_weather_hour(weather_data, dt):
    img = Image.new("1", (TODAYS_IMG_W, const.MODULE_H), 1)
    draw = ImageDraw.Draw(img)

    draw.text(
        xy=(20, 20),
        text="{}".format(dt.strftime("%H:%M")),
        font=util.load_font(24),
    )

    index = weather_data["hourly"]["time"].index(dt.isoformat(timespec="minutes"))

    def is_day(dt):
        return dt.hour >= 6 and dt.hour <= 20

    draw.text(
        xy=(0, -5),
        text=wmo_code_to_icon(weather_data["hourly"][WMO_CODE][index], is_day(dt)),
        font=util.load_font(220),
    )

    draw.text(
        xy=(10, 160),
        text=" {:.0f}°\n {}%\n{}mm".format(
            weather_data["hourly"][TEMP][index],
            weather_data["hourly"][RAIN_PROB][index],
            weather_data["hourly"][RAIN_AMOUNT][index],
        ),
        font=util.load_font(28),
    )

    return img


def create_todays_weather_image(weather_data):
    dt = datetime.now()

    if dt.minute != 0:
        dt = dt.replace(hour=dt.hour + 1, minute=0)

    img = Image.new("1", (TODAYS_IMG_W, const.MODULE_H), 1)
    x = 0

    for hours in [0, 2, 2, 2]:
        dt = dt + timedelta(hours=hours)
        hour_data_img = todays_weather_hour(weather_data, dt)
        img.paste(im=hour_data_img, box=(x, 0))

        x += DAY_HOUR_DISTANCE

    return img


def parse_daily_weather(data, day):
    daily = data["daily"]

    # ['2022-07-08', 3, 20.4, 11.4]
    return [
        daily["time"][day],
        daily["weather_code"][day],
        daily["temperature_2m_min"][day],
        daily["temperature_2m_max"][day],
    ]


def create_daily_image(data):
    img = Image.new("1", (DAILY_IMG_W, const.MODULE_H), 1)
    draw = ImageDraw.Draw(img)

    draw.text(
        (0, 10),
        datetime.strptime(data[0], "%Y-%m-%d").strftime("%A").center(16),
        font=util.load_font(20),
    )

    draw.text(
        xy=(10, -40),
        text=wmo_code_to_icon(data[1], True),
        font=util.load_font(280),
    )

    draw.text(
        (0, 170),
        "{:.0f}° / {:.0f}°".format(data[2], data[3]).center(11),
        font=util.load_font(30),
    )

    return img


def create_module(config):
    location = config["location"]

    if config["test_mode"] and len(config["location"]) == 0:
        location = (48.1549958, 11.4594364)  # munich

    weather_data = get_weather_data(location)

    current_img = create_current_weather_image(weather_data)
    today_img = create_todays_weather_image(weather_data)
    day2_img = create_daily_image(parse_daily_weather(weather_data, 1))
    day3_img = create_daily_image(parse_daily_weather(weather_data, 2))
    day4_img = create_daily_image(parse_daily_weather(weather_data, 3))

    module = Image.new("1", (const.SCREEN_W, const.SCREEN_H), 1)

    module.paste(im=current_img, box=(0, 0))
    module.paste(im=today_img, box=(300, 0))
    module.paste(im=day2_img, box=(250, 250))
    module.paste(im=day3_img, box=(440, 250))
    module.paste(im=day4_img, box=(630, 250))

    return module
