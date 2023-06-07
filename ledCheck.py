import time, sys
from AndyPiPixelLights import AndyPiPixelLights
LEDs = AndyPiPixelLights() #set the name of the module
NUMBER_OF_PIXELS = 138 # Set the number of LEDs in our string
ledpixels = [0] * NUMBER_OF_PIXELS # set up the LED array
theLight = 2

theLight = raw_input("choose an LED number")
while True:
        print ("now displaying LED: " + theLight)
        #clear the leds so nothing is lit
        LEDs.cls(ledpixels) # clears all LEDs to off
        #light the chosen led
        LEDs.setpixelcolor(ledpixels, int(theLight), LEDs.Colo$
        LEDs.writestrip(ledpixels)
        #time.sleep(2)
        #set up for next user input
        theLight = raw_input("choose an LED number")