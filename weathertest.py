#!/usr/bin/python3
import sys
import os
import python_weather
import signal
import asyncio
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk

libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()

async def get_weather():
    
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:

        weather = await client.get('stl')
        
        print(weather)
        # Fetch weather forecast for upcoming days.
        for daily in weather:
            print(daily)

            # Each daily forecast has their own hourly forecasts.
            for hourly in daily:
                print(f' --> {hourly!s}')

        return weather

def main():

    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/agenia/Agenia-Bold.ttf', 122)

    weather = asyncio.run(get_weather())

    draw.text((250, 0), str(weather.temperature) + "°", font=font, fill=0, anchor="rt")

    image = image.rotate(180)

    epd.display(epd.getbuffer(image))
    epd.sleep()

def SignalHandler_SIGINT(SignalNumber, Frame):
    epd.init()
    epd.Clear(0xFF)
    print("Screen cleared. Sleeping.")
    epd.sleep()
    print('Exiting')
    sys.exit()

# regsiter signal with handler
signal.signal(signal.SIGINT,SignalHandler_SIGINT)


if __name__ == '__main__':
    main()