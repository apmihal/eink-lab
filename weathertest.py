#!/usr/bin/python3
import sys
import os
# import python_weather
import signal
# import asyncio
import tkinter as tk
import requests
import json
from PIL import Image, ImageDraw, ImageFont, ImageTk

libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()

epd_height = 250
epd_width = 122

# async def get_weather():
    
#     async with python_weather.Client(unit=python_weather.IMPERIAL) as client:

#         weather = await client.get('stl')
        
#         print(weather)
#         # Fetch weather forecast for upcoming days.
#         for daily in weather:
#             print(daily)

#             # Each daily forecast has their own hourly forecasts.
#             for hourly in daily:
#                 print(f' --> {hourly!s}')

#         return weather

def main():

    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    response = requests.get(
        'https://wttr.in/stl', 
        params={"format": "j1"})

    weather = response.json()

    image = Image.new('1', (epd_height, epd_width), 255)
    draw = ImageDraw.Draw(image)
    temp_mid = ImageFont.truetype('/usr/share/fonts/truetype/agenia/Agenia-Bold.ttf', 55)
    temp_big = ImageFont.truetype('/usr/share/fonts/truetype/agenia/Agenia-Bold.ttf', 100)
    text_font = ImageFont.truetype('/usr/share/fonts/truetype/hack/Hack-Regular.ttf', 20)

    # weather = asyncio.run(get_weather())

    # draw.text((248, 28), str(weather["current_condition"][0]["temp_F"]) + "°", font=temp_font, fill=0, anchor="rt")
    draw.text((245, 5), weather["weather"][0]["maxtempF"], font=temp_mid, fill=0, anchor="rt")
    draw.text((245, 117), weather["weather"][0]["mintempF"], font=temp_mid, fill=0, anchor="rb")
    draw.text((95, 15), weather["current_condition"][0]["temp_F"], font=temp_big, fill=0, anchor="mt")
    draw.text((245, 61), "HI|LO", font=text_font, fill=0, anchor="rm")
    draw.text((95, 107), "NOW", font=text_font, fill=0, anchor="mb")

    image = image.rotate(180)
    # image.show()

    epd.display(epd.getbuffer(image))
    epd.sleep()

# def SignalHandler_SIGINT(SignalNumber, Frame):
#     epd.init()
#     epd.Clear(0xFF)
#     print("Screen cleared. Sleeping.")
#     epd.sleep()
#     print('Exiting')
#     sys.exit()

# # regsiter signal with handler
# signal.signal(signal.SIGINT,SignalHandler_SIGINT)


if __name__ == '__main__':
    main()