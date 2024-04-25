#!/usr/bin/env python3

import logging
import argparse
import image

def main():
    parser = argparse.ArgumentParser(
            prog='pi-display',
            description='Create an image with weather data')

    parser.add_argument('-t', '--test', action='store_true', dest='test_mode', help='run the script in test mode')
    parser.add_argument('-a', '--api-key', dest='api_key', required=True, help='coinmarketcap api-key')
    parser.add_argument('-lat', '--latitude', dest='latitude', required=True, help='latitude')
    parser.add_argument('-lon', '--longitude', dest='longitude', required=True, help='longitude')

    args = parser.parse_args()

    config = {
        'test_mode':args.test_mode,
        'api_key':args.api_key,
        'location':(args.latitude, args.longitude)
    }

    if args.test_mode:
        # for testing image creation
        logging.info('starting in testmode...')
        image.create_image(config).save("output.png")
    else:
        import display
        display.draw_to_display_and_sleep(image.create_image(config))

if __name__ == '__main__':
    main()
