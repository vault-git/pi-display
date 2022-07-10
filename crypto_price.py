#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageOps
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import constants as const
import util

COINMARKETCAP_API = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

PARAMETERS = {
    'start':'1',
    'limit':'2',
    'convert':'EUR'
}

HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'insert-api-key-here!!!',
}

def get_crypto_price():
    session = Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(COINMARKETCAP_API, params=PARAMETERS)
        data = json.loads(response.text)

        prices = {}

        for coin in data['data']:
            if coin['name'] == 'Bitcoin':
                prices['Bitcoin'] = (coin['quote']['EUR']['price'],
                                     coin['quote']['EUR']['percent_change_24h'],
                                     coin['quote']['EUR']['percent_change_7d'],
                                     coin['quote']['EUR']['percent_change_90d'])
            if coin['name'] == 'Ethereum':
                prices['Ethereum'] = (coin['quote']['EUR']['price'],
                                     coin['quote']['EUR']['percent_change_24h'],
                                     coin['quote']['EUR']['percent_change_7d'],
                                     coin['quote']['EUR']['percent_change_90d'])

        return prices

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return ''

# creates the crypto_price 'module' that can be pasted to the main image
def create_module():
    module = Image.new('1', const.MODULE_SIZE, 1)
    draw = ImageDraw.Draw(module)

    btc_icon = util.load_icon('data/image/bitcoin-icon.svg', 0.5)
    eth_icon = util.load_icon('data/image/ethereum-icon.svg', 0.5)

    crypto_data = get_crypto_price()

    module.paste(btc_icon, box=(20, 30), mask=btc_icon)
    draw.text((95, 40), '{:6d}€'.format(int(crypto_data['Bitcoin'][0])), font=util.load_font(30))
    draw.text((270, 20), '{:.2f}%'.format(crypto_data['Bitcoin'][1]), font=util.load_font(20))
    draw.text((270, 50), '{:.2f}%'.format(crypto_data['Bitcoin'][2]), font=util.load_font(20))
    draw.text((270, 80), '{:.2f}%'.format(crypto_data['Bitcoin'][3]), font=util.load_font(20))

    module.paste(eth_icon, box=(20, 140), mask=eth_icon)
    draw.text((95, 150), '{:6d}€'.format(int(crypto_data['Ethereum'][0])), font=util.load_font(30))
    draw.text((270, 130), '{:.2f}%'.format(crypto_data['Ethereum'][1]), font=util.load_font(20))
    draw.text((270, 160), '{:.2f}%'.format(crypto_data['Ethereum'][2]), font=util.load_font(20))
    draw.text((270, 190), '{:.2f}%'.format(crypto_data['Ethereum'][3]), font=util.load_font(20))

    # add a border to the image
    module = ImageOps.expand(module, border=2)

    return module
