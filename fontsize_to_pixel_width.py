#!/usr/bin/env python3
import sys
import os
import textwrap
import math
from PIL import Image, ImageDraw, ImageFont

font_path = '/usr/share/fonts/truetype/JetBrainsMono/JetBrainsMonoNL-Regular.ttf'

def main():
    image = Image.new('1', (2000, 2000), 255)  # 255 = white background
    draw = ImageDraw.Draw(image)

    char = 'm'

    max_font_size = 65

    size_to_maxperline = {}

    # Gets width of character by looking at its bounding box
    # math.floor() sees how many times a pixel that wide can fit on the screen
    #print('size : width : max per line')
    for i in range(1, max_font_size):
        font = ImageFont.truetype(font_path, i)
        bbox = draw.textbbox((0, 0), char, font=font)
        size_to_maxperline[i] = math.floor(250 / bbox[2])
        # print(str(i) + ' : ' + str(bbox[2]) + ' : ' + str(math.floor(122 / bbox[2])))

    print(size_to_maxperline)


if __name__ == '__main__':
    main()