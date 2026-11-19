#!/usr/bin/python3
import sys
import os
import signal
import tkinter as tk
import requests
import json
from time import sleep
from PIL import Image, ImageDraw, ImageFont, ImageTk

# passing 'dev' as arg at runtime renders as png instead of on screen
dev = False

if len(sys.argv) > 1:
    if sys.argv[1] == "dev":
        dev = True

if not dev:
    libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'

    if os.path.exists(libdir):
        sys.path.append(libdir)

    from waveshare_epd import epd2in13_V4

    epd = epd2in13_V4.EPD()

epd_height = 250
epd_width = 122

temp_mid = ImageFont.truetype('/usr/share/fonts/truetype/agenia/Agenia-Bold.ttf', 55)
temp_big = ImageFont.truetype('/usr/share/fonts/truetype/agenia/Agenia-Bold.ttf', 90)
text_font = ImageFont.truetype('/usr/share/fonts/truetype/hack/Hack-Regular.ttf', 20)

def main():

    # not sure why it wouldn't let update be a global variable, but dev is fine
    update = True

    while update:
        if not dev:
            epd.init()
            epd.Clear(0xFF)

        response = requests.get(
            'https://wttr.in/stl', 
            params={"format": "j1"})

        weather = response.json()

        image = Image.new('1', (epd_height, epd_width), 255)
        draw = ImageDraw.Draw(image)

        # current temp
        draw.text(
            (75, 5), 
            weather["current_condition"][0]["temp_F"] + "°", 
            font=temp_big, 
            fill=0, 
            anchor="mt")

        # max temp
        draw.text(
            (245, 5), 
            weather["weather"][0]["maxtempF"] + "°", 
            font=temp_mid, 
            fill=0, 
            anchor="rt")

        # min temp
        draw.text(
            (245, 117), 
            weather["weather"][0]["mintempF"] + "°", 
            font=temp_mid, 
            fill=0, 
            anchor="rb")

        # "HI | LO"
        draw.text(
            (235, 61), 
            "HI|LO", 
            font=text_font, 
            fill=0, 
            anchor="rm")

        # "NOW"
        draw.text(
            (107, 68), 
            "NOW", 
            font=text_font, 
            fill=0, 
            anchor="lb")

        # weather description
        draw.text(
            (87, 95), 
            weather["current_condition"][0]["weatherDesc"][0]["value"], 
            font=text_font, 
            fill=0, 
            anchor="lm")
    
        # finds the highest percent chance of rain for the day
        biggest_chance = 0

        for hour in range(0, len(weather["weather"][0]["hourly"])):
            chance = weather["weather"][0]["hourly"][hour]["chanceofrain"]
            
            if int(chance) > biggest_chance:
                biggest_chance = int(chance)

        # "RA\nIN"
        draw.text(
            (5, 74), 
            "RA\nIN", 
            font=text_font, 
            fill=0)

        # rain chance percent
        draw.text(
            (35, 95), 
            str(biggest_chance) + "%", 
            font=text_font, 
            fill=0, 
            anchor="lm")

        if dev:
            image.show()
            update = False
        else:
            image = image.rotate(180)
            epd.display(epd.getbuffer(image))
            epd.sleep()
            sleep(1830)    

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