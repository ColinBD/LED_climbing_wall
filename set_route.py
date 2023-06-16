import time, sqlite3
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


# Configure the count of pixels:
PIXEL_COUNT = 32

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
allowed_strings = ["l11","l10","l9","k9","k10","k11","k12","j11","j10","j9","i9","i10","i11","i12",
"h11","h10","h9","g9","g10","g11","g12","f11","f10","f9","e9","e10","e11","e12","d11","d10","d9","c9",
"c10","c11","c12","b11","a12","a11","b10","a10","b9","a9","a8","a7","a6","a5","b5","b6","b7","b8","c8",
"c7","c6","c5","d5","d6","d7","d8","e8","f8","f7","e7","f6","e6","e5","f5","g5","g6","g7","g8","h8",
"h7","h6","h5","i5","i6","i7","i8","j8","j7","j6","j5","k5","k6","k7","k8","l8","l7","l6","l5","l4",
"l3","l2","l1","k1","k2","k3","k4","j4","j3","j2","j1","i1","i2","i3","i4","h4","h3","h2","h1","g1",
"g2","g3","g4","f4","f3","f2","f1","e1","e2","e3","e4","d4","d3","d2","d1","c1","c2","c3","c4","b4","b3","b2","b1","a1","a2","a3","a4"]

# maps climbing wall LED identifier to position in LED string
# short mapper below is just for testing
mapper = {"a1": 0, "a2": 1, "a3": 2, "a4": 3, "a5": 4, "a6": 5, "a7": 6, "a8": 7}

# mapper = {"l11": 0, "l10": 1, "l9": 2, "k9": 3, "k10": 4, "k11": 5, "k12": 6, "j11": 7, "j10": 8,
# "j9": 9, "i9": 10, "i10": 11, "i11": 12, "i12": 13, "h11": 14, "h10": 15, "h9": 16, "g9": 17,
# "g10": 18, "g11": 19, "g12": 20, "f11": 21, "f10": 22, "f9": 23, "e9": 24, "e10": 25, "e11": 26,
# "e12": 27, "d11": 28, "d10": 29, "d9": 30, "c9": 31, "c10": 32, "c11": 33, "c12": 34, "b11": 35,
# "a12": 36, "a11": 37, "b10": 38, "a10": 39, "b9": 40, "a9": 41, "a8": 42, "a7": 43, "a6": 44,
# "a5": 45, "b5": 46, "b6": 47, "b7": 48, "b8": 49, "c8": 50, "c7": 51, "c6": 52, "c5": 53, "d5": 54,
# "d6": 55, "d7": 56, "d8": 57, "e8": 58, "f8": 59, "f7": 60, "e7": 61, "f6": 62, "e6": 63, "e5": 64,
# "f5": 65, "g5": 66, "g6": 67, "g7": 68, "g8": 69, "h8": 70, "h7": 71, "h6": 72, "h5": 73, "i5": 74,
# "i6": 75, "i7": 76, "i8": 77, "j8": 78, "j7": 79, "j6": 80, "j5": 81, "k5": 82, "k6": 83, "k7": 84,
# "k8": 85, "l8": 86, "l7": 87, "l6": 88, "l5": 89, "l4": 90, "l3": 91, "l2": 92, "l1": 93, "k1": 94,
# "k2": 95, "k3": 96, "k4": 97, "j4": 98, "j3": 99, "j2": 100, "j1": 101, "i1": 102, "i2": 103,
# "i3": 104, "i4": 105, "h4": 106, "h3": 107, "h2": 108, "h1": 109, "g1": 110, "g2": 111, "g3": 112,
# "g4": 113, "f4": 114, "f3": 115, "f2": 116, "f1": 117, "e1": 118, "e2": 119, "e3": 120, "e4": 121,
# "d4": 122, "d3": 123, "d2": 124, "d1": 125, "c1": 126, "c2": 127, "c3": 128, "c4": 129, "b4": 130,
# "b3": 131, "b2": 132, "b1": 133, "a1": 134, "a2": 135, "a3": 136, "a4": 137}

class Led:
  def __init__(self, position, colour):
    self.position = position
    self.colour = colour

def set(light, color):
    #transform the wall LED identifier (e.g. a6) into the string identifier (e.g. 18)
    string_pos = mapper[light]
    if color == 'red':
        pixels.set_pixel(string_pos, Adafruit_WS2801.RGB_to_color(0,0,255))
    elif color == 'green':
        pixels.set_pixel(string_pos, Adafruit_WS2801.RGB_to_color(0,255,0))
    elif color == 'blue':
        pixels.set_pixel(string_pos, Adafruit_WS2801.RGB_to_color(255,0,0))
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
        print('the save to db routine')
        #only save routes with >= 2 holds lit (e.g. a dyno route could be two holds)
        if len(lights_list) > 1:
            grade = raw_input('What is the v grade of the route? (just enter the number)')
            conn = sqlite3.connect("routesDB.db")
            cursor = conn.cursor()
            string = prep_string()
            print('\nthis is lights string: ' + string)
            cursor.execute('''INSERT INTO routes(route, grade, complete_count, fail_count)
                      VALUES(?,?,?,?)''', (string,grade,0,0))
            conn.commit()

def prep_string():
        i=0
        my_string = ''
        for i in lights_list:
            my_string = my_string + i + ';' 
        # while i < (len(lights_list) - 1):
        #         #get the content from lights list and add it to the string var with a comma
        #         my_string = my_string + lights_list[i] + ';'
        #         print(my_string)
        #         i = i + 1
        print(my_string)
        raw_input('consider my_string then press ENTER to continue')
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
            print("I don't understand that command, so I can't set that an LED, save to the database or quit the application. Please try again.")