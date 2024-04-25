from PIL import Image, ImageDraw

from datetime import datetime
import constants
import util
import dht
import weather_data
import crypto_price

def create_image(config):
    img = Image.new('1', (constants.SCREEN_W, constants.SCREEN_H))

    img.paste(dht.create_module(config), (0,0))
    img.paste(crypto_price.create_module(config), (320,0))
    img.paste(weather_data.create_module(config), (0,240))

    # draws timestamp in the bottom right
    ImageDraw.Draw(img).text((675, 465), datetime.now().strftime("%H:%M %d.%m.%y"), font=util.load_font(14))

    return img
