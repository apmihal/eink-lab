#!/usr/bin/env python3

# Usage: ./imagetesting.py 'image.bmp'
# As long as the image is within the screen's dimensions it will be displayed
# The image will be converted to monochrome if it isn't already.

import sys
import os
from PIL import Image, ImageDraw, ImageFont

libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()

def main():
    if len(sys.argv) == 1:
        print('Specify an image file.')

    elif len(sys.argv) == 2:
        file = sys.argv[1]

        # try:
        #     image = Image.open(file)
        # except:
        #     print("Can't open file")
        #     sys.exit()

        # if image.format != 'BMP':
        #     reject(image, 'Needs to be BMP')
        
        # elif image.height > 122 or image.width > 250:
        #     reject(image, 'Dimensions too big')
        
        # elif image.mode != '1':
        #     image = image.convert('1')
        #     print('mode converted')
        
        # # If the image isn't exactly 250x122 this pastes it on a canvas that is
        # elif image.height < 122 or image.width < 250:
        #     image = pasteOnCanvas(image)

        valid, image = validateAndConvert(file, True, True)

        if valid:
            printMetadata(image)
            display(image)

        else:
            print('not sure how we got here')
            sys.exit()

    else:
        print('Too many arguments.')

def pasteOnCanvas(image):
    canvas = Image.new('1', (epd.height, epd.width), 255)
    canvas.paste(image, (0, 0))
    return canvas        

def reject(image, message):
    print("Error: " + message)
    printMetadata(image)
    sys.exit()   
        
def printMetadata(image):
    print('height: ' + str(image.height))
    print('width: ' + str(image.width))
    print('mode: ' + image.mode)
    #Needs str() because if the image had to be pasted it returns None
    print('format: ' + str(image.format))
   
def display(image):
    epd.init()
    epd.Clear(0xFF)

    image = image.rotate(180)
    epd.display(epd.getbuffer(image))
    epd.sleep()
    print('sleeping')

def validateAndConvert(filename, allowSmall, kill):
# usage validateAndConvert(str, bool, bool)
# allowSmall allows images that are less than screen rez to display
# kill kills the program if a file is bad
    try:
        image = Image.open(filename)

    except:
        print("Can't open file")
        if kill:
            sys.exit()

        else:
            return False, None

    if image.format != 'BMP':
        print("Needs to be BMP")

        if kill:
            sys.exit()

        else:
            return False, None
        
    elif image.height > 122 or image.width > 250:
        print("Image too big")

        if kill:
            sys.exit()

        else:
            return False, None

    elif image.mode != '1':
        try:
            image = image.convert('1')

        except:
            print("Can't convert to monochrome")

            if kill:
                sys.exit()

            else:
                return False, None

    elif image.height < 122 or image.width < 250:
        if allowSmall:
            image = pasteOnCanvas(image)

        else:
            print("Image too small")

            if kill:
                sys.exit()
            else:
                return False, None

    return True, image

if __name__ == '__main__':
    main()
