#!/usr/bin/env python3

import sys
import os
from PIL import Image, ImageDraw, ImageFont

libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()

def main():

    files = os.listdir('.')

    for file in files:
        












if __name__ == '__main__':
    main()

