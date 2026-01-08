#!/usr/bin/python3
import sys
import os
from PIL import Image, ImageDraw, ImageFont

# Add the library path
libdir = '/home/andrewm/eink/e-Paper/RaspberryPi_JetsonNano/python/lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

def main():
    # Initialize display
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)
    
    # Create a new image (250x122 pixels for 2.13" V4)
    # Note: width and height are swapped due to display orientation
    image = Image.new('1', (epd.height, epd.width), 255)  # 255 = white background
    draw = ImageDraw.Draw(image)
    
    # Load a font
    font = ImageFont.truetype('/usr/share/fonts/truetype/JetBrainsMono/JetBrainsMonoNL-Regular.ttf', 20)
    
    # Draw text

    draw.text((0, 0), "Testing monospace font\nI hope it works!", font=font, fill=0)  # 0 = black text
    
    # Rotate 180 degrees if needed
    image = image.rotate(180)
    
    # Display the image
    epd.display(epd.getbuffer(image))
    
    # Sleep mode to save power
    epd.sleep()
    print("Done! Display should show 'Hello World!'")

if __name__ == '__main__':
    main()
