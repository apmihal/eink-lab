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

def main():
    image = Image.new('1', (epd.height, epd.width), 255)  # 255 = white background
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('/usr/share/fonts/truetype/JetBrainsMono/JetBrainsMonoNL-Regular.ttf', 20)

    long_text = "Venezuela Live Updates: U.S. Forces Seize Two Tankers; Rubio Lays Out Plan for American Control"
    draw_multiline_text(draw, long_text, 0, 0, font, 20, 0, 3)

    display(image)

def draw_multiline_text(draw, text, x, y, font, max_chars_per_line=20, fill=0, line_spacing=5):
    """Draw text with line wrapping based on character count"""
    lines = textwrap.wrap(text, width=max_chars_per_line)

    """If I can get the bounding box of the last line, I can see if the message will go out of bounds
    We can learn how many lines are in lines and use that to pick out the bbox
    maybe just put every bbox in a list and then grab the last one
    or an if statement that grabs the last bbox during the loop"""

    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        current_y += line_height + line_spacing
    
    return current_y

if __name__ == '__main__':
    main()