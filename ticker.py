#!/usr/bin/env python3
import sys
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

from displayimage import display

libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()

# Global starting font size
font_size = 64

too_tall = False

# I figured out the ratio of fontsize to max characters per line with fontsize_to_pixelwidth.py
# Is this a stupid way to do things??
fontsize_to_maxperline = {1: 250, 2: 125, 3: 125, 4: 83, 5: 83, 6: 62, 7: 62, 8: 50, 9: 
50, 10: 41, 11: 35, 12: 35, 13: 31, 14: 31, 15: 27, 16: 25, 17: 25, 18: 22, 19: 22, 20: 
20, 21: 19, 22: 19, 23: 17, 24: 17, 25: 16, 26: 15, 27: 15, 28: 14, 29: 14, 30: 13, 31: 
13, 32: 13, 33: 12, 34: 12, 35: 11, 36: 11, 37: 11, 38: 10, 39: 10, 40: 10, 41: 10, 42: 
10, 43: 9, 44: 9, 45: 9, 46: 8, 47: 8, 48: 8, 49: 8, 50: 8, 51: 8, 52: 8, 53: 7, 54: 7, 
55: 7, 56: 7, 57: 7, 58: 7, 59: 7, 60: 6, 61: 6, 62: 6, 63: 6, 64: 6}



def main():
    image = Image.new('1', (epd.height, epd.width), 255)  # 255 = white background
    draw = ImageDraw.Draw(image)

    # The message to be displayed
    long_text = "ICE FUCK OFF"

    final_y = draw_multiline_text(draw, long_text, 0, 0, font_size, 0, 3)

    display(image)

# slaps text on image based on font size, reduces font size if it won't fit
def draw_multiline_text(draw, text, x, y, font_size, fill=0, line_spacing=3):
    """Draw text with line wrapping based on character count"""
    # breaks the text into individual lines based on what will fit per line
    # the max number of characters is pulled from my dictionary that's indexed by font size
    lines = textwrap.wrap(text, fontsize_to_maxperline[font_size])

    # creates the font object based on current font_size value
    font = ImageFont.truetype('/usr/share/fonts/truetype/JetBrainsMono/JetBrainsMonoNL-Regular.ttf', font_size)

    # iterates over the text lines, draws them to image, looks at difference between
    # bottom and top of text box, and uses that to set the position for the next line
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        current_y += line_height + line_spacing

    # if after iterating through the lines, the bottom line is off the screen then: 
    # we gotta get RECURSIVE!!!
    # we call the function that were currently in after decrementing the font_size
    # and we keep going deeper until it fits (wait...)
    # Is this a stupid way to do things?
    # How could it be stupid? It uses recursion.
    if current_y > 122:
        font_size -= 1
        print(str(font_size))
        draw.rectangle([(0, 0), (250,122)], fill=255)
        draw_multiline_text(draw, text, x, y, font_size, fill=0, line_spacing=3)

    return current_y

if __name__ == '__main__':
    main()
