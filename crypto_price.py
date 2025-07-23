#!/usr/bin/env python3

import json

from PIL import Image, ImageDraw
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import constants as const
import util

COINMARKETCAP_API = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

PARAMETERS = {
    'start':'1',
    'limit':'2',
    'convert':'EUR'
}

def get_crypto_values(api_key):
    session = Session()
    session.headers.update({
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': api_key,
    })

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

    except (ConnectionError, Timeout, TooManyRedirects):
        return {}

# creates the crypto_price 'module' that can be pasted to the main image
def create_module(config):
    module = Image.new('1', (const.MODULE_W + 100, const.MODULE_H), 1)
    draw = ImageDraw.Draw(module)

    btc_icon = util.load_icon('data/image/bitcoin-icon.svg', 0.4)
    eth_icon = util.load_icon('data/image/ethereum-icon.svg', 0.4)

    if config['test_mode']:
        module.paste(btc_icon, box=(100, 17), mask=btc_icon)
        draw.text((140, 20), '{:.0f}€'.format(100000).center(10), font=util.load_font(38))
        draw.text((0, 80), '24h: {:.1f}%  7d: {:.1f}%  90d: {:.1f}%'.format(-10.0, 10.0, 20.5), font=util.load_font(22))
        module.paste(eth_icon, box=(100, 130), mask=eth_icon)
        draw.text((140, 135), '{:.0f}€'.format(3000).center(10), font=util.load_font(38))
        draw.text((0, 190), '24h: {:.1f}%  7d: {:.1f}%  90d: {:.1f}%'.format(15.4, 12.3, -10.2), font=util.load_font(22))

        return module

    crypto_data = get_crypto_values(config['api_key'])

    if 'Bitcoin' in crypto_data :
        bitcoin = crypto_data['Bitcoin']
        module.paste(btc_icon, box=(100, 17), mask=btc_icon)
        draw.text((140, 20), '{:.0f}€'.format(bitcoin[0]).center(10), font=util.load_font(38))

        draw.text((0, 80), '24h: {:.1f}%  7d: {:.1f}%  90d: {:.1f}%'.format(bitcoin[1], bitcoin[2], bitcoin[3]), font=util.load_font(22))

    if 'Ethereum' in crypto_data :
        ethereum = crypto_data['Ethereum']
        module.paste(eth_icon, box=(100, 130), mask=eth_icon)

        draw.text((140, 135), '{:.0f}€'.format(ethereum[0]).center(10), font=util.load_font(38))

        draw.text((0, 190), '24h: {:.1f}%  7d: {:.1f}%  90d: {:.1f}%'.format(ethereum[1], ethereum[2], ethereum[3]), font=util.load_font(22))

    return module
