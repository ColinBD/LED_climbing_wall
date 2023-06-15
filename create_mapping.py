import time
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# Configure the count of pixels:
PIXEL_COUNT = 138

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

mapper = {}

if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    # Instructions 
    print('This script will step through each LED in your string and ask you to input the hold you see indicated by the lit LED.\n')
    print('This assumes: 1. each hold on your climbing wall is labelled (e.g. perhaps via a grid system with letters on the X axis and numbers on the Y axis.\n')
    print('2. That you have edited line 9 of this script to reflect the number of LEDs within your light string.\n')
    print('Once you have input an identifier for each hold, a "mapper" dictionary will be printed to screen.\n')
    print('You should copy this text and paste it into set_route.py, replacing the default mapper dictionary code. I.e. place this directly after the "mapper = " text.\n')

    for i in range(0, PIXEL_COUNT):
        pixels.clear()
        pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(0,255,0))
        pixels.show()
        match = raw_input(str(i+1) + ' of ' + str(PIXEL_COUNT) + '. What hold do you see indicated by the lit LED? Type e.g. a3 (or "none" if no hold is indicated) then press the ENTER key\n')
        #store 'match' against the LED string spoition
        mapper[match] = i

    print('You will now see the mapper dictionary code output below. Copy this and replace the mapper dictionary in set_route.py\n')
    print(mapper)