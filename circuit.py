import time, sqlite3
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# database setup
db = 'routesDB.db'
table = 'routes'

# Configure the count of pixels:
PIXEL_COUNT = 138

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


# ------- functions ----------------

def set_light(light, color):
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

def set_all(LEDS):
    pixels.clear()
    pixels.show() 
    for LED in LEDS:
        set_light(LED.position, LED.colour)
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

def update_route(sql):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
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
        set_all(parse_LED_string(route))
        # The user is invited to press 'e' to edit the route (change the grade), 'f' to mark as failed on the route and load next, or 'space bar' to mark as success and load next. 
        char = raw_input("'e' to change the grade; 'f' to mark as failed; 's' to mark as success; any other key to load next route without marking success.")
        if char == 'e':
            #  change grade then feedback to user
            new_grade = raw_input('What do you want to set this routes grade to?')
            if new_grade == grade:
                 print("That's the same as the old grade!!!")
            else: 
                sql = "UPDATE " + table + " SET grade = " + new_grade + " WHERE id = " + route_id + ";"
                update_route(sql)
                print('\nThe grade had been ammended.')
            char = raw_input("'f' to mark as failed; 's' to mark as success; any other key to load next route without marking success.")
        if char == 'f':
            # increment failed column in the database for this route 
            sql = "UPDATE " + table + " SET fail_count = " + str(int(fails) + 1) + " WHERE id = " + route_id + ";"
            update_route(sql)
        elif char == 's':
            # increment success column in the database for this route
            sql = "UPDATE " + table + " SET complete_count = " + str(int(successes) + 1) + " WHERE id = " + route_id + ";"
            update_route(sql)
        # load next route
        current_route_num = current_route_num + 1
    
    # all done message - give the number of successes and fails for this session. Perhaps give the time to complete too.
    print("All done! That's you on the road to being stronger!")
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!