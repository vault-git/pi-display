#!/usr/bin/env python3

import waveshare.epd7in5_V2 as epd7in5

import logging

def draw_to_display_and_sleep(image):
    try:
        # init the display
        epd = epd7in5.EPD()
        epd.init()
        # epd.Clear()

        # draw the image to the display
        epd.display(epd.getbuffer(image))

        # go to deep sleep mode
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd7in5.epdconfig.module_exit()
        exit()
