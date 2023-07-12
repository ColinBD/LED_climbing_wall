import time, sqlite3
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


# Configure the count of pixels:
PIXEL_COUNT = 138

# create a lights list which we can store our lights in
lights_list = []

# Helpers
red = 'red'
blue = 'blue'
green = 'green'
off = 'off'

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

#to verify user input matches an avaolable LED
allowed_strings = ["l11","l10","l9","k9","k10","k11","j11","j10","j9","i9","i10","i11",
"h11","h10","h9","g9","g10","g11","f11","f10","f9","e9","e10","e11","d11","d10","d9","c9",
"c10","c11","b11","a11","b10","a10","b9","a9","a8","a7","a6","a5","b5","b6","b7","b8","c8",
"c7","c6","c5","d5","d6","d7","d8","e8","f8","f7","e7","f6","e6","e5","f5","g5","g6","g7","g8","h8",
"h7","h6","h5","i5","i6","i7","i8","j8","j7","j6","j5","k5","k6","k7","k8","l8","l7","l6","l5","l4",
"l3","l2","l1","k1","k2","k3","k4","j4","j3","j2","j1","i1","i2","i3","i4","h4","h3","h2","h1","g1",
"g2","g3","g4","f4","f3","f2","f1","e1","e2","e3","e4","d4","d3","d2","d1","c1","c2","c3","c4","b4",
"b3","b2","b1","a1","a2","a3","a4","b12","d12","f12","h12","j12"]

# maps climbing wall LED identifier to position in LED string
# short mapper below is just for testing
# mapper = {"a1": 0, "a2": 1, "a3": 2, "a4": 3, "a5": 4, "a6": 5, "a7": 6, "a8": 7}

mapper = {"c4": 110, "d8": 95, "d9": 97, "d6": 93, "d7": 94, "d4": 91, "d5": 92, "d2": 89, 
          "d3": 90, "d1": 88, "e11": 75, "e10": 76, "c5": 108, "b12": 125, "c11": 101, "c10": 102, 
          "g7": 53, "g6": 54, "g5": 55, "g4": 56, "g3": 57, "g2": 58, "g1": 59, "b11": 124, "g9": 51, 
          "g8": 52, "j8": 20, "j9": 21, "j4": 16, "j5": 17, "j6": 18, "j7": 19, "j1": 13, "j2": 14, 
          "j3": 15, "b4": 117, "b5": 118, "b6": 119, "b7": 120, "b1": 114, "b2": 115, "b3": 116, 
          "b8": 121, "b9": 122, "e9": 77, "e8": 79, "e5": 82, "e4": 84, "e7": 80, "e6": 81, "e1": 87, 
          "e3": 85, "e2": 86, "h8": 43, "h9": 45, "h2": 37, "h3": 38, "h1": 36, "h6": 41, "h7": 42, 
          "h4": 39, "h5": 40, "k11": 0, "k10": 1, "c9": 103, "c8": 105, "c3": 111, "c2": 112, "c1": 113, 
          "j12": 24, "c6": 107, "j10": 22, "j11": 23, "h12": 48, "h10": 46, "h11": 47, "f12": 73, 
          "f10": 71, "f11": 72, "f1": 60, "f2": 61, "f3": 62, "f4": 63, "f5": 65, "f6": 66, "f7": 67, 
          "f8": 68, "f9": 70, "d10": 98, "d11": 99, "d12": 100, "k3": 10, "k2": 11, "k1": 12, "k7": 5, 
          "k6": 6, "k5": 7, "k4": 9, "c7": 106, "k9": 2, "k8": 4, "i9": 27, "i8": 28, "a11": 126, 
          "a10": 127, "i1": 35, "b10": 123, "i3": 33, "i2": 34, "i5": 31, "i4": 32, "i7": 29, "i6": 30, 
          "a3": 135, "a2": 136, "a1": 137,"a5": 133, "a4": 134, "a7": 131, "a6": 132, "a9": 128, "a8": 130, 
          "i11": 25, "i10": 26, "g11": 49, "g10": 50}

class Led:
  def __init__(self, position, colour):
    self.position = position
    self.colour = colour

def set(light, color):
    #transform the wall LED identifier (e.g. a6) into the string identifier (e.g. 18)
    string_pos = mapper[light]
    if color == 'red':
        pixels.set_pixel(string_pos, Adafruit_WS2801.RGB_to_color(255,0,0))
    elif color == 'green':
        pixels.set_pixel(string_pos, Adafruit_WS2801.RGB_to_color(0,255,0))
    elif color == 'blue':
        pixels.set_pixel(string_pos, Adafruit_WS2801.RGB_to_color(0,0,255))
    elif color == 'off':
        pixels.set_pixel(string_pos, Adafruit_WS2801.RGB_to_color(0,0,0)) 

def setAll(LEDs):
    pixels.clear()
    pixels.show() 
    for LED in lights_list:
        set(LED.position, LED.colour)
    pixels.show()


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

def save_to_db():
        #only save routes with >= 2 holds lit (e.g. a dyno route could be two holds)
        if len(lights_list) > 1:
            grade = raw_input('What is the v grade of the route? (just enter the number)')
            string = prep_string()
            conn = sqlite3.connect("routesDB.db")
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO routes(route, grade, complete_count, fail_count)
                      VALUES(?,?,?,?)''', (string,grade,0,0))
            conn.commit()

def prep_string():
        i=0
        my_string = ''
        for i in lights_list:
            my_string = my_string + i.position + ',' + i.colour + ';' 
        return my_string

if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    while True:
        s = raw_input('To turn an LED on or off enter the LED indentifier, then comma, then color (choices of red, green, blue, off) E.g. "a6,red".\nTo save route to the database press "s" then ENTER.\nTo exit without saving press "e" then ENTER.\n')
        current_pix = s.split(',')
        if len(current_pix) == 2:
            if current_pix[0] in allowed_strings:
                print('Okay, you want to set LED ' + str(current_pix[0]) + ' to ' + str(current_pix[1])) 
                col = current_pix[1]
                if col == 'red' or col == 'green' or col == 'blue':
                    # push this choice into the lights_list
                    lights_list.append(Led(current_pix[0],current_pix[1]))
                    # change this and instead make a setAll function which loops over lights_list and calls set function for each object
                    setAll(lights_list)
                elif col == 'off':
                    for x in lights_list:
                        if x.position == current_pix[0]:
                            lights_list.remove(x)
                    setAll(lights_list)
        elif current_pix[0] == 'e':
            pixels.clear()
            pixels.show()  # Make sure to call show() after changing any pixels!
            #exit the application
            quit()
        elif current_pix[0] == 's': 
            #save the route to the database
            save_to_db()
            pixels.clear()
            pixels.show()  # Make sure to call show() after changing any pixels!
            #then quit
            raw_input('The route was saved to the database. Press the ENTER key to quit the applicaiton.')
            quit()
        else:
            raw_input("I don't understand that command, so I can't set that LED, save to the database or quit the application. Please press ENTER then try again.")