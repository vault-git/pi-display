#!/usr/bin/env python3

import logging
import argparse
import image


def main():
    parser = argparse.ArgumentParser(
        prog="pi-display", description="Create an image with weather data"
    )

    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        dest="test_mode",
        help="Run the script in test mode",
    )
    parser.add_argument(
        "-a",
        "--api-key",
        dest="api_key",
        help="Coinmarketcap API-KEY (unused currently)",
    )
    parser.add_argument(
        "--log", dest="log", default="WARNING", help="Set the log level"
    )
    parser.add_argument(
        "-lat", "--latitude", dest="latitude", help="Latitude for weather forecast"
    )
    parser.add_argument(
        "-lon", "--longitude", dest="longitude", help="Longitude for weather forecast"
    )

    args = parser.parse_args()

    config = {
        "test_mode": args.test_mode,
        "api_key": args.api_key,
        "location": (args.latitude, args.longitude),
    }

    logging.basicConfig(level=args.log.upper(), format="%(levelname)s: %(message)s")

    if args.test_mode:
        # for test image creation
        logging.info("starting in testmode...")
        image.create_image(config).save("output.png")
    else:
        import display

        display.draw_to_display_and_sleep(image.create_image(config))


if __name__ == "__main__":
    main()
