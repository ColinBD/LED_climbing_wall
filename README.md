# LED climbing wall

Use LEDs to create custom routes up a climbing wall. This code runs on a Raspberry Pi 3 connected to a chain of WS2801 LEDs. Three scripts are included: 
- climb.py is used to generate a workout by picking routes at random from the database. 
- addRoutes.py lets you create routes and stores them into the database
- addSymetricalRoutes.py is for people who have a symetrical 'systems board' climbing wall. For each route created, a secondary symetrical route is generated and stored into the database. 

As of 2023 these scripts no longer work. They will soon be replaced by the following scripts:
- led_test.py
- set_route.py - lets you turn pixels on/off, set their color, add a climbing grade and save the route to a database.
- circuit.py - you choose a grade range, the number of climbs you want to do, whether you want to do symetrical versions, and then the routes will be presented with a key press moving to the next route.

## Demonstration

You can see the system in action in this YouTube demo:

[![LED climbing wall demonstration](https://img.youtube.com/vi/_OsM3mQc0_Y/0.jpg)](https://www.youtube.com/watch?v=_OsM3mQc0_Y)

## Prerequisites

- Raspberry Pi 3
- WS2801 LEDs chained together (which you should fit into holes below each hold on the climbing wall - not necessary for initial testing)

## Pi Setup

You need to configure the Pi's SPI bus. Open a terminal and type:

    sudo raspi-config

Then select “Advanced Option” > “SPI”. Enable it and exit.

Update and install neccessary packages:

    sudo apt-get update
    sudo apt-get install python-pip -y
    sudo pip install adafruit-ws2801

## Connecting the LEDS
You need to connect the LEDs to the GPIO pins on your Pi. Ensure your Pi is switched off when making these connections.

Note: Your Pi may not be able to supply enough current so you might need to connect the 5V wire on your LEDs to an alternative  power supply if the supply from GPIO pin 2 proves insufficient.

| **GPIO pin**  | **LED connection** |
|---------------|--------------------|
| Pin 2 (5V)    | 5V                 |
| Pin 6 (GND)   | GND                |
| Pin 19 (MOSI) | SI / DI            |
| Pin 23 (SCKL) | CK / CI            |

![image](./img/GPIO_pins.jpg)

## Test the LEDs

With the lights connected and the Pi setup and powered on, you can now test the lights by opening a terminal and running:

    python led_check.py

You should see each pixel ligh in turn, and this will cycle through red, green then blue.

## Add an SQLite database

This will store the routes

- [An SQLight database](http://raspberrywebserver.com/sql-databases/set-up-an-sqlite-database-on-a-raspberry-pi.html)

Next, you should download this repo onto your Pi and try running climb.py.

## Configuring for your climbing wall environment

The scripts were written for my climbing wall which has 16 rows of holds, with an alternating number of holds on each column; 12 or 11, giving 138 LEDs in total. Unless you wish to build a wall which matches this configuration you will want to modify the code to match your wall. 

In such cases you will need to:

- Delete all the entries from the SQLite database. 
- Label each hold on your climbing wall (I recommend labelling each row and each column, holds are then identified through this paring e.g. the hold on row A, column 2 is A2)
- Modify the 'allowed_strings' and 'mapper' variables to link each LED to the corresponding hold on your climbing wall. This should be done in the 'climb.py', 'addRoutes.py' and 'addSymetricalRoutes.py' files. 

## Author

**Colin Bone Dodds**   email: colinbonedodds@gmail.com   github: https://github.com/ColinBD

## License

This project is licensed under the MIT License

