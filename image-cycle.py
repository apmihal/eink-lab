#!/usr/bin/env python3

import sys
import os
import random
import time
from PIL import Image, ImageDraw, ImageFont
from displayimage import display, pasteOnCanvas, validateAndConvert

libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()

def main():

    files = os.listdir('./images')
    recents = []

    while True:
        choice = random.randrange(len(files) - 1)

        if files[choice] not in recents:
            if len(recents) < 2:
                recents.append(files[choice])
            else:
                recents.pop(0)
                recents.append(files[choice])

            valid, image = validateAndConvert('./images/' + str(files[choice]), False, False)

            if valid:
                display(image)
                time.sleep(180)
                

            else:
                continue

        else:
            continue



        












if __name__ == '__main__':
    main()

