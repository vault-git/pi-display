from PIL import Image, ImageDraw

from datetime import datetime
import constants
import util
import dht
import weather_data
import crypto_price

MODULE_0_POS = (0, 0)
MODULE_1_POS = (400, 0)
MODULE_2_POS = (0, 240)
MODULE_3_POS = (400, 240)

def create_image():
    img = Image.new('1', (constants.SCREEN_W, constants.SCREEN_H))

    # all modules (except for weather) have the same size (400, 240)
    img.paste(dht.create_module(), MODULE_0_POS)
    img.paste(crypto_price.create_module(), MODULE_1_POS)
    img.paste(weather_data.create_module(), MODULE_2_POS)

    # draws timestamp in the bottom right
    ImageDraw.Draw(img).text((700, 465), datetime.now().strftime("%H:%M %d.%m.%y"), font=util.load_font(12))

    # for changing and testing image creation
    # img.save("test.png")

    return img

if __name__ == '__main__':
    create_image()
