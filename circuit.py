import time, sqlite3
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# database setup
db = 'routesDB.db'
table = 'routes'

# Configure the count of pixels:
PIXEL_COUNT = 32

#set up required variable
current_route_num = 0
num_routes_to_climb = 0
route_set = []

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


# ------- functions ----------------

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

def setAll(LEDS):
    pixels.clear()
    pixels.show() 
    for LED in LEDS:
        set(LED.position, LED.colour)
    pixels.show()

def parse_LED_string(string):
    lights_list = []
    string_list = string.split(';')
    for x in string_list:
        led_info = x.split(',')
        if len(led_info) == 2:
            lights_list.append(Led(led_info[0],led_info[1]))
    return lights_list


def read_from_db(num_wanted):
    routes = []
    conn = sqlite3.connect('routesDB.db')
    cursor = conn.cursor()
    sql = "SELECT * FROM " + table + " WHERE grade BETWEEN " + low_grade + " AND " + high_grade + " ORDER BY RANDOM()" + " LIMIT " + num_wanted
    i=0
    for row in cursor.execute(sql):
            #print row
            routes.append(row)
            i = i+1
    conn.close()
    return routes
 
def update_grade(route_id, grade):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # UPDATE routes SET grade = 9 WHERE id = 1;
    sql = "UPDATE " + table + " SET grade = " + grade + " WHERE id = " + route_id + ";"
    cursor.execute(sql)
    conn.commit()
    conn.close()


# ensure low grade is not higher than high grade
def grade_check():
    if int(high_grade) < int(low_grade):
        print ("high/low grade mismatch... you'll have to start again!... exiting program...")
        time.sleep(2)
        exit()
    return


if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    # ---- GET WORKOUT DETAILS FROM USER ----

    num_routes_wanted = raw_input("how many routes do you want to do this workout? ")
    low_grade = raw_input("what is the LOWEST 'v' grade you want to do this workout? [just enter a number] ")
    high_grade = raw_input("what is the HIGHEST 'v' grade you want to do this workout? [just enter a number] ")

    # check high grade not lower than the low grade
    grade_check()

    print("\nthanks for that, we are generating your workout...\n")

    # get the routes from the database
    route_set = read_from_db(num_routes_wanted)
    num_routes_available = len(route_set)

    # if no routes match the users criteria quit
    if len(route_set) == 0:
            raw_input("There are no routes that match your request in the database. You'll have to start again. Press any key to quit")
            exit()

    # when we got >1 routes but <num requested
    if int(num_routes_available) < int(num_routes_wanted):
        print('You asked for ' + str(num_routes_wanted) + ' routes but I could only find ' + str(num_routes_available) + ' routes in the database within that grade span, so I will just give you them!\n')
        num_routes_to_climb = num_routes_available
    else: 
        num_routes_to_climb = num_routes_wanted
    
    # print for debuggin - todo: remove when it's all working well
    for x in route_set:
         print(x)

    while int(current_route_num) < int(num_routes_to_climb):
    # loop through routes_list presenting them one at a time
        # print useful info to console
        route_id = str(route_set[current_route_num][0])
        route = route_set[current_route_num][1]
        grade = str(route_set[current_route_num][2])
        successes = str(route_set[current_route_num][4])
        fails = str(route_set[current_route_num][5])
        print(str(current_route_num+1) + ' of ' + str(num_routes_to_climb) + '. Grade: V'+ grade + ', success count = ' + successes + ', fail count = ' + fails)
        print('id = ' + route_id + '. Route = ' + route)
        # show the leds
        setAll(parse_LED_string(route))
        # The user is invited to press 'e' to edit the route (change the grade), 'f' to mark as failed on the route and load next, or 'space bar' to mark as success and load next. 
        char = raw_input("'e' to change the grade; 'f' to mark as failed; 's' to mark as success; any other key to load next route without marking success.")
        if char == 'e':
            #  change grade then feedback to user
            new_grade = raw_input('What do you want to set this routes grade to?')
            if new_grade == grade:
                 print("That's the same as the old grade!!!")
            else: 
                update_grade(route_id, new_grade)
        elif char == 'f':
            # increment failed column in the database for this route 
            print('mark as route failed routine')
        elif char == 's':
            # increment success column in the database for this route
            print('mark as route success routine')
        # load next route
        current_route_num = current_route_num + 1
    
    # all done message - give the number of successes and fails for this session. Perhaps give the time to complete too.
    print("All done! That's you on the road to being stronger!")
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!