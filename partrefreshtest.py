#!/usr/bin/python3
import sys
import os 
import time
from time import sleep
from PIL import Image,ImageDraw,ImageFont
import math

libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()

text_font = ImageFont.truetype('/usr/share/fonts/truetype/hack/Hack-Regular.ttf', 20)

def main():
    
    epd.init_fast()
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    time_draw.rectangle((5, 5, 45,45), fill = 0)
    time_image = time_image.rotate(180)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    num = 0

    while (True):
        time_draw.rectangle((120, 80, 220, 105), fill = 255)
        time_draw.text((120, 80), time.strftime('%H:%M:%S'), font = text_font, fill = 0)

        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        sleep(1)
        if (num == 10):
            break

    sleep(5)

    epd.init()
    epd.Clear(0xFF)

    epd.sleep()

if __name__ == "__main__":
    main()
