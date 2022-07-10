#!/usr/bin/env python3

import cairosvg
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def load_icon(icon_path, scale):
    out = BytesIO()
    cairosvg.svg2png(url=icon_path, write_to=out, scale=scale)
    return Image.open(out)

def load_font(size):
    return ImageFont.truetype("data/fonts/RobotoMono-Regular.ttf", size)
