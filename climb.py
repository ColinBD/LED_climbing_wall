#!/usr/bin/python
# -*- coding: ascii -*-
import os, sys, time, sqlite3
from random import randint

# route mapper for raspberry pi - WORKOUT BY NUMBER OF ROUTES   (we'll have another file for workout by time)

#set led pixel library
from AndyPiPixelLights import AndyPiPixelLights # Import the AndyPi Python module (you need to set the number of pixels in here)
LEDs=AndyPiPixelLights() # Set the name of our module 
NUMBER_OF_PIXELS=138 # Set the number of pixels i.e. number of leds we have
ledpixels = [0] * NUMBER_OF_PIXELS # set up the pixel array

#set up required variable
current_route_num = 1
route_set = []


# ---- DECLARE FUNCTIONS ----

# ensure low grade is not higher than high grade
def grade_check():
        if int(high_grade) < int(low_grade):
                print ("high/low grade mismatch... you'll have to start again!... exiting program...")
                time.sleep(2)
                exit()
        return

# create a user info function
def user_update():
        print("you are on route " + str(current_route_num) + " of " + str(num_routes))
        return


# ---- GET WORKOUT DETAILS FROM USER ----

num_routes = raw_input("how many routes do you want to do this workout?")
low_grade = raw_input("what is the LOWEST 'v' grade you want to do this workout? [just enter a number]")
high_grade = raw_input("what is the HIGHEST 'v' grade you want to do this workout? [just enter a number]")

# check that the high grade is not lower than the low grade - if it is ask them to choose again
grade_check()

print("\nthanks for that, we are generating your workout...\n")


# ---- GET ROUTES FROM DATABASE ----

# connect to the database
conn = sqlite3.connect('routesDB.db')
cursor = conn.cursor()
sql = "SELECT aroute FROM routes WHERE grade BETWEEN " + low_grade + " AND " + high_grade
i=0
for row in cursor.execute(sql):
        #print row
        route_set.append(row)
        i = i+1
conn.close()
print('the number of routes matching your criteria is: ' + str(len(route_set)))

# if no routes match the users criteria quit
if len(route_set) == 0:
        print("There are no routes that match your request... you'll have to start again... quitting")
        time.sleep(3)
        exit()

# print the routes
#i=0
#while i < len(route_set):
#       print(route_set[i])
#       i = i + 1

# ---- DECLARE THE DICTIONARY ----

# declare the dictionary to map between board code and LED number
mapper = {"l11": 0, "l10": 1, "l9": 2, "k9": 3, "k10": 4, "k11": 5, "k12": 6, "j11": 7, "j10": 8, "j9": 9, "i9": 10, "i10": 11, "i11": 12, "i12": 13, "h11": 14, $


# ---- THE LOOPY BIT / REPEAT FOR EACH ROUTE
        # loop from 1 through to the users desired number of routes are complete
while current_route_num <= int(num_routes):
        # get a route from the route_set data 
                # generate a random number within the bounds of the number of routes matching our criteria
        dice_roll = randint(0,len(route_set)-1)
                # pick a random route from the set using the random number
        currentRouteMidway = route_set[(dice_roll)]
        # clean up the selected route data
        currentRoute = currentRouteMidway[0]
                # split at ',' and store the parts in a list
        currentRouteList = [x.strip() for x in currentRoute.split(',')]


        # create an output array the same size as theRoute array - in this case it is filled with zeros for now
                # i.e. same number of moves
        theConvertedRoute = [0] * len(currentRouteList)

		# convert board info into LED pixel integer info
        i = 0
        while i < len(currentRouteList):
                theConvertedRoute[i] = mapper[(currentRouteList[i])]
                print "board code: " + currentRouteList[i] + " = LED number: " + str(theConvertedRoute[i])
                i += 1

        # PIXEL LIGHTS STUFF HERE
        try:
                LEDs.cls(ledpixels) # clears all the pixels to black
                time.sleep(0.1)
                #loop through and set the pixels
                i = 0
                while i < len(theConvertedRoute):
                        LEDs.setpixelcolor(ledpixels, theConvertedRoute[i], LEDs.Color(0,0,255)) # set the 1st (0th)  pixel to red
                        i = i+1
                LEDs.writestrip(ledpixels) # writes the pixels (must be called after setpixelcolor to update    
        except  KeyboardInterrupt: # clears all pixels in the case of Ctrl-C exit
                LEDs.cls(ledpixels)
                sys.exit(0)
        # give the user some feedback
        user_update()
        # pause the program here and wait for the user to press a key before continuing
        raw_input("Press the ENTER key to continue...")
        current_route_num = current_route_num + 1

# once we are out of the while loop the user has been through all the routes so we can display a thanks and goodbye message
print('that is all the routes done... goodbye')
LEDs.cls(ledpixels)
time.sleep(3)

