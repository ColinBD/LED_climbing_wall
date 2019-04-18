# LED climbing wall

Use LEDs to create custom routes up a climbing wall. This code runs on a Raspberry Pi 3 connected to a chain of WS2801 LEDs. Three scripts are included: 
- climb.py is used to generate a workout by picking routes at random from the database. 
- addRoutes.py lets you create routes and stores them into the database
- addSymetricalRoutes.py is for people who have a symetrical 'systems board' climbing wall. For each route created, a secondary symetrical route is generated and stored into the database.  

## Prerequisites

- Raspberry Pi 3
- WS2801 LEDs chained together (which you will eventually fit into holes below each hold on the climbing wall)
- [The AndyPi PixelLights library](https://github.com/andy-pi/pixellights.git)
- [An SQLight database](http://raspberrywebserver.com/sql-databases/set-up-an-sqlite-database-on-a-raspberry-pi.html)

## Getting Started

Follow AndyPi's [guide](https://andypi.co.uk/2014/12/27/raspberry-pi-controlled-ws2801-rgb-leds/) to get your LEDs set up and working on your Pi - some nice twinkly demos are included. 

Next, you should download this repo onto your Pi and try running climb.py.

## Configuring for your climbing wall environment

The scripts were written for my climbing wall which has 16 rows of holds, with an alternating number of holds on each column; 12 or 11, giving 138 LEDs in total. Unless you wish to build a wall which matches this configuration you will want to modify the code to match your wall. 

In such cases you will need to:

- Delete all the entries from the SQLite database. 
- Label each hold on your climbing wall (I recommend labelling each row and each column, holds are then identified through this paring e.g. the hold on row A, column 2 is A2)
- Modify the 'allowed_strings' and 'mapper' variables to link each LED to the corresponding hold on your climbing wall. This should be done in the 'routes.py', 'addRoutes.py' and 'addRoutes2.py' files. 

## Author

Colin Bone Dodds (https://github.com/ColinBD)

## License

This project is licensed under the MIT License

