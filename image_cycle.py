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
   
    # This will be determined by an argument, but is hardcoded for now.
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
        
        # Populates images dictionary with valid images and their filenames
        if valid:
            images[file] = image

    # Fills recents up with 2 random numbers because the logic for checking if it's populated each time
    # and populating it if it hasn't been is too complicated. They're still random! Just not recent.
    # Shh our little secret 🤫 
    rand1 = random.randrange(0, len(images))
    rand2 = random.randrange(0, len(images))

    while rand1 == rand2:
        rand2 = random.randrange(0, len(images))

    recents = [rand1, rand2]

    print(images)

    # Main loop. Displays images on screen and prints filenames with a timestamp.
    # Has a counter that resets once it's looped through dictionary.
    while True:
        currentTime = getTime()
        
        # If random=True generate a random number until you find one that hasn't been used recently.
        if isRandom:
            imageNum = random.randrange(0, len(images))

            while imageNum in recents:
                imageNum = random.randrange(0, len(images))
            
            # Remove oldest recent, and add the newest imageNum value
            recents.pop(0)
            recents.append(imageNum)
        
        # If random=False just index along with the counter
        else:
            imageNum = counter

        # Dictionaries are now ordered in python.
        # Using list() instantiates a list of keys indexed at counter
        print('Displaying: ' + list(images)[imageNum] + ' at ' + currentTime)   

        # One step further by creating list of values indexed at counter
        display(list(images.values())[imageNum])

        # Spec sheet says waiting at least 3 minutes between refreshes is ideal
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
