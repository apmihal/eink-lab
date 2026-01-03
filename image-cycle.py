#!/usr/bin/env python3
import sys
import os
import random
import signal
import time
from PIL import Image, ImageDraw, ImageFont

# Importing functions from another script
from displayimage import display, pasteOnCanvas, validateAndConvert
from clearscreen import clearScreen

libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()

def main():
    
    isRandom = True

    counter = 0

    # Create dictionary for filename: image object
    images = {}

    # Grabs list of files in ./images
    files = os.listdir('./images')

    # Runs once to pick out the valid images and put them in images dictionary
    for file in files:

        # Concatenates ./images path to filename, sends to validator
        # allowSmall = false (must be exactly 250x122)
        # kill = false (don't kill program over invalid file)
        valid, image = validateAndConvert('./images/' + file, False, False)

        if valid:
            images[file] = image

    print(images)

    # Main loop. Displays images on screen and prints filenames with a timestamp.
    # Has a counter that resets once it's looped through dictionary.
    while True:
        currentTime = getTime()

        if isRandom:
            imageNum = random.randrange(0, len(images))

        else:
            imageNum = counter   

        # Dictionaries are now ordered in python.
        # Using list() instantiates a list of keys indexed at counter
        print('Displaying: ' + list(images)[imageNum] + ' at ' + currentTime)   

        # One step further by creating list of values indexed at counter
        display(list(images.values())[imageNum])

        #Spec sheet says waiting at least 3 minutes between refreshes is ideal
        time.sleep(180)

        # Counter increment/reset logic
        if counter + 1 == len(images):
            counter = 0
        else:
            counter += 1
         
def getTime():
    # Returns current time in a string
    return time.strftime("%H:%M:%S", time.localtime())

# Create a Signal Handler for Signals.SIGINT:  CTRL + C 
def SignalHandler_SIGINT(SignalNumber, Frame):
    clearScreen()
    print('Exiting')
    sys.exit()

# regsiter signal with handler
signal.signal(signal.SIGINT,SignalHandler_SIGINT)

if __name__ == '__main__':
    main()
