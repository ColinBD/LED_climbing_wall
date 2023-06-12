import time
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


# Configure the count of pixels:
PIXEL_COUNT = 32

# Helpers
red = 'red'
blue = 'blue'
green = 'green'
off = 'off'

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

def set(light, color):
    if color == 'red':
        pixels.set_pixel(light, Adafruit_WS2801.RGB_to_color(0,0,255))
    elif color == 'green':
        pixels.set_pixel(light, Adafruit_WS2801.RGB_to_color(0,255,0))
    elif color == 'blue':
        pixels.set_pixel(light, Adafruit_WS2801.RGB_to_color(255,0,0))
    elif color == 'off':
        pixels.set_pixel(light, Adafruit_WS2801.RGB_to_color(0,0,0))

def brightness_decrease(pixels, wait=0.01, step=1):
    for j in range(int(256 // step)):
        for i in range(pixels.count()):
            r, g, b = pixels.get_pixel_rgb(i)
            r = int(max(0, r - step))
            g = int(max(0, g - step))
            b = int(max(0, b - step))
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( r, g, b ))
        pixels.show()
        if wait > 0:
            time.sleep(wait)

def blink_color(pixels, blink_times=5, wait=0.5, color=(255,0,0)):
    for i in range(blink_times):
        # blink two times, then wait
        pixels.clear()
        for j in range(2):
            for k in range(pixels.count()):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.08)
            pixels.clear()
            pixels.show()
            time.sleep(0.08)
        time.sleep(wait)

def appear_from_back(pixels, color=(255, 0, 0)):
    pos = 0
    for i in range(pixels.count()):
        for j in reversed(range(i, pixels.count())):
            pixels.clear()
            # first set all pixels at the begin
            for k in range(i):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            # set then the pixel at position j
            pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.02)

if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!
    #time.sleep(0.05)

    #for i in range(3):
     #   blink_color(pixels, blink_times = 1, color=(255, 0, 0))
      #  blink_color(pixels, blink_times = 1, color=(0, 255, 0))
       # blink_color(pixels, blink_times = 1, color=(0, 0, 255))

    #pixels.set_pixel(12, Adafruit_WS2801.RGB_to_color(255,0,0))
    #pixels.set_pixel(14, Adafruit_WS2801.RGB_to_color(0,255,0))
    #pixels.set_pixel(16, Adafruit_WS2801.RGB_to_color(0,0,255))
    #but I would prefer to write like: set(4, red)

    while True:
        s = raw_input('Which LED would you like to set? Enter pixel number, then comma, then color (choices of red, green, blue, off. E.g. "6,red". ')
        current_pix = s.split(',')
        if len(current_pix) == 2:
            print('Okay, you want to set LED ' + str(current_pix[0]) + ' to ' + str(current_pix[1]))
            col = current_pix[1]
        if col == 'red' or col == 'green' or col == 'blue' or col == 'off':
            set(int(current_pix[0]), current_pix[1])
            pixels.show()
        else:
            print('I do not understand that colour, so I cannot set that pixel.')


    #set(1, red)
    #set(2, red)
    #set(5, blue)
    #set(12, green)
    #set(12, off)
    #pixels.show()
    #time.sleep(2)
    #brightness_decrease(pixels)
    #pixels.clear()
    #pixels.show()