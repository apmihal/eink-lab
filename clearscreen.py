#!/usr/bin/env python3
import sys
import os

libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()

def main():
    clearScreen()

def clearScreen():
    epd.init()
    epd.Clear(0xFF)
    print("Screen cleared. Sleeping.")
    epd.sleep()

if __name__ == '__main__':
    main()