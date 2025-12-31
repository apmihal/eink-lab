#!/usr/bin/env python3
import sys
import os
from PIL import Image, ImageDraw, ImageFont

libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

def main():
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    # Resolution is (250x122)
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    icon = Image.open('farside-epaper.bmp')
    icon = icon.convert('1')
    # icon = icon.resize((64,64))
    image.paste(icon, (0,0))

    image = image.rotate(180)
    epd.display(epd.getbuffer(image))
    epd.sleep()
    print("sleeping")

    # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
    
    # if len(sys.argv) == 2:
        # message = sys.argv[1].replace('\\n', '\n')
        # draw.text((5,5), message, font=font, fill=0)
        # image = image.rotate(180)
        # epd.display(epd.getbuffer(image))
        # epd.sleep()
        # print("Message displayed! " + sys.argv[1])

   # else:
       # draw.text((5,5), "Got nothin huh?", font=font, fill=0)
       # image = image.rotate(180)
       # epd.display(epd.getbuffer(image))
       # epd.sleep()
       # print("Gotta put a message pal.")

if __name__ == '__main__':
    main()

