# -*- coding: ascii -*-
import os, sys, sqlite3, time

# this script will allow a user to create a route and add it to the database

#set led pixel library
from AndyPiPixelLights import AndyPiPixelLights # Import the AndyPi Python module (you need to set the number of pixels in here)
LEDs=AndyPiPixelLights() # Set the name of our module 
NUMBER_OF_PIXELS=138 # Set the number of pixels i.e. number of leds we have
ledpixels = [0] * NUMBER_OF_PIXELS # set up the pixel array

# the var below will be used to break us out of a while loop
switching = True

# create a lights list which we can store our lights in
lights_list = []

# create an allowed strings list
allowed_strings = ["l11","l10","l9","k9","k10","k11","k12","j11","j10","j9","i9","i10","i11","i12",
"h11","h10","h9","g9","g10","g11","g12","f11","f10","f9","e9","e10","e11","e12","d11","d10","d9","c9",
"c10","c11","c12","b11","a12","a11","b10","a10","b9","a9","a8","a7","a6","a5","b5","b6","b7","b8","c8",
"c7","c6","c5","d5","d6","d7","d8","e8","f8","f7","e7","f6","e6","e5","f5","g5","g6","g7","g8","h8",
"h7","h6","h5","i5","i6","i7","i8","j8","j7","j6","j5","k5","k6","k7","k8","l8","l7","l6","l5","l4",
"l3","l2","l1","k1","k2","k3","k4","j4","j3","j2","j1","i1","i2","i3","i4","h4","h3","h2","h1","g1",
"g2","g3","g4","f4","f3","f2","f1","e1","e2","e3","e4","d4","d3","d2","d1","c1","c2","c3","c4","b4","b3","b2","b1","a1","a2","a3","a4"]

# ---- DECLARE THE DICTIONARY ----
# declare the dictionary to map between board code and LED number 
mapper = {"l11": 0, "l10": 1, "l9": 2, "k9": 3, "k10": 4, "k11": 5, "k12": 6, "j11": 7, "j10": 8,
"j9": 9, "i9": 10, "i10": 11, "i11": 12, "i12": 13, "h11": 14, "h10": 15, "h9": 16, "g9": 17,
"g10": 18, "g11": 19, "g12": 20, "f11": 21, "f10": 22, "f9": 23, "e9": 24, "e10": 25, "e11": 26,
"e12": 27, "d11": 28, "d10": 29, "d9": 30, "c9": 31, "c10": 32, "c11": 33, "c12": 34, "b11": 35,
"a12": 36, "a11": 37, "b10": 38, "a10": 39, "b9": 40, "a9": 41, "a8": 42, "a7": 43, "a6": 44,
"a5": 45, "b5": 46, "b6": 47, "b7": 48, "b8": 49, "c8": 50, "c7": 51, "c6": 52, "c5": 53, "d5": 54,
"d6": 55, "d7": 56, "d8": 57, "e8": 58, "f8": 59, "f7": 60, "e7": 61, "f6": 62, "e6": 63, "e5": 64,
"f5": 65, "g5": 66, "g6": 67, "g7": 68, "g8": 69, "h8": 70, "h7": 71, "h6": 72, "h5": 73, "i5": 74,
"i6": 75, "i7": 76, "i8": 77, "j8": 78, "j7": 79, "j6": 80, "j5": 81, "k5": 82, "k6": 83, "k7": 84,
"k8": 85, "l8": 86, "l7": 87, "l6": 88, "l5": 89, "l4": 90, "l3": 91, "l2": 92, "l1": 93, "k1": 94,
"k2": 95, "k3": 96, "k4": 97, "j4": 98, "j3": 99, "j2": 100, "j1": 101, "i1": 102, "i2": 103,
"i3": 104, "i4": 105, "h4": 106, "h3": 107, "h2": 108, "h1": 109, "g1": 110, "g2": 111, "g3": 112,
"g4": 113, "f4": 114, "f3": 115, "f2": 116, "f1": 117, "e1": 118, "e2": 119, "e3": 120, "e4": 121,
"d4": 122, "d3": 123, "d2": 124, "d1": 125, "c1": 126, "c2": 127, "c3": 128, "c4": 129, "b4": 130,
"b3": 131, "b2": 132, "b1": 133, "a1": 134, "a2": 135, "a3": 136, "a4": 137}

# -- FUNCTIONS --
def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")

def save_to_db():
        author = raw_input('Who is the routes author?')
        grade = raw_input('What is the v grade of the route? (just enter the number)')
        conn = sqlite3.connect("routesDB.db")
        cursor = conn.cursor()
        string = prep_string()
        print('\nthis is lights string: ' + string)
        cursor.execute('''INSERT INTO routes(aroute, grade, author)
                  VALUES(?,?,?)''', (string,grade,author))
        conn.commit()

def prep_string():
        i=0
        my_string = ''
        while i < (len(lights_list) - 1):
                #get the content from lights list and add it to the string var with a comma
                my_string = my_string + lights_list[i] + ','
                print(my_string)
                i = i + 1
        my_string = my_string + lights_list[i]
        print(my_string)
        return my_string

# -- THE LOOP --

# the normal state is to be in a loop allowing the user to toggle LEDs on and off switch an LED
while switching == True:
        # get an LED from the user
        current_led = raw_input("which LED would you like to switch?")
        # check that they entered a valid LED
        if current_led in allowed_strings:
                #print('your entry was accepted')
                # is the LED in the lights list?
                if current_led in lights_list:
                        # it is already there so remove it to turn the light off
                        lights_list.remove(current_led)
                else: lights_list.append(current_led) # it's not there so add it
                        # if the LED is found then it gets removed, if it is not found it gets appended (i.e. this allows them to be toggled on and off)
        else: print('entry is not recognised')
        print(lights_list)

        # CLEAR AND SET THE LEDS HERE
        try:
                print('WE ARE INTO THE LOOP')
                LEDs.cls(ledpixels) # clears all the pixels to black
                time.sleep(0.1)
                #loop through and set the pixels
                i = 0
                while i < len(lights_list):
                        LEDs.setpixelcolor(ledpixels, mapper[lights_list[i]], LEDs.Color(0,0,255)) # set the 1st (0th)  pixel to red
                        i = i+1
                LEDs.writestrip(ledpixels) # writes the pixels (must be called after setpixelcolor to update    
        except  KeyboardInterrupt: # clears all pixels in the case of Ctrl-C exit
                LEDs.cls(ledpixels)
                sys.exit(0)

        if yes_or_no('would you like to switch another LED?') == False:
                # user does not want to switch another LED so we can exit the switching loop
                switching = False


# user then has the choice of 1) switch another LED, 2) save the route to db 3) quit
while True:
        choice = raw_input('Would you like to: 1) save the route to the database? 2) quit the program?')
        if choice in ['1','2']: # check that the user entered either 1 or 2
                break # if it's an appropriate input we can break out of the loop
        else: print('\nUhhh... please try again \n')

# process their choice
if choice == '1':
        print('\nsaving the route to the database...\n')
        # call the save to db routine
        save_to_db()
        print('the route: ' + str(lights_list) + ' was saved to the database')
else:
        print('\nyou have chosen to quit...quitting now\n')
        LEDs.cls(ledpixels)
        quit()