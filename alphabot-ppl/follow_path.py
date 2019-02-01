from grid_nav import *
import os
import subprocess
from self_locator import *
from micro_controller import *
import yaml
import math
import signal
import sys

CONFIG = yaml.load(open("../config.yaml"))

# Example Diagram with obstacles
# DIAGRAM1_S = (1,4)
# DIAGRAM1_G = (7,8)
# DIAGRAM1 = GridWithWeights(10, 10)
# DIAGRAM1.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
# DIAGRAM1.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
#                                        (4, 3), (4, 4), (4, 5), (4, 6), 
#                                        (4, 7), (4, 8), (5, 1), (5, 2),
#                                        (5, 3), (5, 4), (5, 5), (5, 6), 
#                                        (5, 7), (5, 8), (6, 2), (6, 3), 
#                                        (6, 4), (6, 5), (6, 6), (6, 7), 
#                                        (7, 3), (7, 4), (7, 5)]}

# (Column, Row)
GRID_COLUMNS = CONFIG["grid"]["columns"]
GRID_ROWS = CONFIG["grid"]["columns"]

# BEACON_COLORS = [0, 1, 2, 3, 4]
BEACON_COLUMNS = CONFIG["grid"]["beacons_columns"]
BEACON_ROWS = CONFIG["grid"]["beacons_rows"]
CELL_SIZE = CONFIG["grid"]["cell_size"]

DIAGRAM2 = GridWithWeights(GRID_COLUMNS, GRID_ROWS)
DIAGRAM2_S = CONFIG["grid"]["start"] # Start
DIAGRAM2_G = CONFIG["grid"]["goal"] # Goal
ORIENT_REF_ROW = CONFIG["grid"]["orientation_reference_row"] # Red Beacon

S1 = str(CONFIG["camera"]["vertical_servo_pin"])

# Rotate AlphaBot according to its new desired orientation
def change_orientation(mc, co, no):
    print("Orientation should be: " + str(no) + "deg, but is: " + str(co) + "deg.")
    deg_diff = co - no
    # Rotational movements below 10deg are imprecise
    if (math.fabs(deg_diff) > 10):
        print("Fix: Rotating " + str(int(deg_diff)) + "deg...\n")
        print("---------- Micro Controller Logs -------------")
        mc.move_and_control([0, 0, 0, 0, 0, deg_diff])
        print("----------------------------------------------\n")
    else:
        print("Error too small. Ignoring...")
    
# Move AlphaBot one tile forward
def move_forward(mc, distance):
    print("Moving forward for " + str(round(distance, 2)) + "m...\n")
    pos_arry = [0, 0, 0, distance, 0, 0]
    print("---------- Micro Controller Logs -------------")
    r = mc.move_and_control(pos_arry)
    print("----------------------------------------------\n")
    return r

# Return estimated AlphaBot's position in grid (column, row, orientation)
def self_localize(self_locator):
    print("Self Localising...")
    b_distance, b_angle, b_color = self_locator.dna_from_beacons()
    x, y, column, row = detect_position_in_grid(b_distance, b_color)
    # angle from the first beacon is enough
    orientation = detect_orientation(x, y, b_distance[0], b_angle[0], b_color[0]) 
    # print x, y, column, row, orientation
    return x, y, column, row, orientation

# Detect AlphaBot's orientation (degrees) relevant to a reference point in grid
def detect_orientation(ax, ay, distance, theta_beac, color):
    rx = ORIENT_REF_ROW * CELL_SIZE + CELL_SIZE / 2
    ry = ay
    bx = BEACON_ROWS[color] * CELL_SIZE + CELL_SIZE / 2
    by = BEACON_COLUMNS[color] * CELL_SIZE + CELL_SIZE / 2 

    # beacon - alphabot distance
    bad = round(distance)
    print("Beacon - AlphaBot distance: " + str(bad) + "cm.")
    # beacon - ref distance
    brd = round(math.sqrt((bx - rx) ** 2 + (by - ry) ** 2))
    print("Beacon - Reference Point distance: " + str(brd) + "cm.")
    # alphabot - ref distance
    ard = round(math.sqrt((ax - rx) ** 2 + (ay - ry) ** 2))
    print("AlphaBot - Reference Point distance: " + str(ard) + "cm.")

    # Cosine Rule
    a = round(math.degrees(math.acos((bad ** 2 + ard ** 2 - brd ** 2) / (2 * bad * ard))), 2)
    print("Cosine Rule Angle: " + str(a) + "deg.")
    
    # theta_or < 0 if the reference point is on the right of the alphabot, > 0 otherwise 
    # if ((by < ry) and (theta_beac > 0)):
    #     theta_or = theta_beac + a
    # elif ((by < ry) and (theta_beac < 0)):
    #     theta_or = theta_beac + a 
    # elif ((by > ry) and (theta_beac > 0)):
    #     theta_or = theta_beac - a
    # elif ((by > ry) and (theta_beac < 0)):
    #     theta_or = theta_beac - a
    theta_or = theta_beac - ((by-ry)/math.fabs(by-ry)) * a
    print("Orientation Angle: " + str(theta_or) + "deg.")

    return theta_or

# Detect AlphaBot's position in grid (columns, rows)
def detect_position_in_grid(distance, color):
    r0 = distance[0]
    print("R0 = " + str(r0))
    r1 = distance[1]
    print("R1 = " + str(r1))
    x0 = BEACON_ROWS[color[0]] * CELL_SIZE + CELL_SIZE / 2 # because it sits in the cell centre
    print("x0 = " + str(x0))
    y0 = BEACON_COLUMNS[color[0]] * CELL_SIZE + CELL_SIZE / 2
    print("y0 = " + str(y0))
    x1 = BEACON_ROWS[color[1]] * CELL_SIZE + CELL_SIZE / 2
    print("x1 = " + str(x1))  
    y1 = BEACON_COLUMNS[color[1]] * CELL_SIZE + CELL_SIZE / 2
    print("y1 = " + str(y1))
    
    # Circle - Circle Intersection calculation
    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r0 ** 2 - a ** 2)
    x2 = x0 + a * (x1 - x0) / d   
    y2 = y0 + a * (y1 - y0) / d   
    x3a = round(x2 + h * (y1 - y0) / d, 2)     
    print("IP1 x = " + str(x3a))
    x3b = round(x2 - h * (y1 - y0) / d, 2)
    print("IP2 x = " + str(x3b))
    y3a = round(y2 - h * (x1 - x0) / d, 2)
    print("IP1 y = " + str(y3a))
    y3b = round(y2 + h * (x1 - x0) / d, 2)
    print("IP2 y = " + str(y3b))

    if ((x3a > GRID_ROWS*CELL_SIZE) or (y3a > GRID_COLUMNS*CELL_SIZE)):   
        if ((x3b <= GRID_ROWS*CELL_SIZE) or (y3b <= GRID_COLUMNS*CELL_SIZE)):  
            x3 = x3b 
            y3 = y3b
        else:
            print("Invalid Intersection Point found!")
            
    elif ((x3a < GRID_ROWS*CELL_SIZE) and (y3a < GRID_COLUMNS*CELL_SIZE)):   
        x3 = x3a
        y3 = y3a
    else:
        print("Invalid Intersection Point found")

    print("IP x = " + str(x3))
    print("IP y = " + str(y3))
    row = x3 // CELL_SIZE
    column = y3 // CELL_SIZE
    
    return x3, y3, column, row

# A dp path planning algorithm (either dijkstra or a*)
def plan_the_path(start, goal):
    came_from, cost_so_far = a_star_search(DIAGRAM2, start, goal)
    draw_grid(DIAGRAM2, width=3, point_to=came_from, start=start, goal=goal)
    print("")
    draw_grid(DIAGRAM2, width=3, number=cost_so_far, start=start, goal=goal)
    print("")
    draw_grid(DIAGRAM2, width=3, path=reconstruct_path(came_from, start = start, goal = goal))
    path = reconstruct_path(came_from, start = start, goal = goal)
    print(path)

    return path

def signal_handler(sig, frame):
    print(' was pressed! Fixing camera position and terminating...\n')
    with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', S1, '-w', '1600'], 
            stdout=devnull, stderr=subprocess.STDOUT)
    sys.exit(0)

def main():
    os.system('clear')
    signal.signal(signal.SIGINT, signal_handler)
    print("-----------------------------------------------------------------------------------")
    print("--------------------------------- ALPHABOT-PPL ------------------------------------") 
    print("-----------------------------------------------------------------------------------\n")
    print("Initiating...\n")
    sl = SelfLocator(300)
    mc = MicroControler()
    # Solve the dp and visualise path
    try:
        x, y, i, j, co = self_localize(sl)
    except InsufficientLocalizationInfoError:
        print("I have no information regarding where I am. Quiting...\n")
        quit()
    path = plan_the_path((i,j), DIAGRAM2_G)
    # Start following path
    print("Starting to follow path...")
    cp = path.pop(0) # Get starting position
    while path: # While path_list not empty:
        # 1: check if re-calculation of the path is needed
        print ("Thinking that I am in position: (" + str(int(cp[0])) + ", " + str(int(cp[1])) + ")")
        print ("I actually am at: (" + str(int(i)) + ", " + str(int(j)) + "), or (" + 
            str(int(x)) + ", " + str(int(y)) + ") in cm. ")
        if ((i != cp[0]) or (j != cp[1])):
            print "So, I need to plan the path again.\n"
            path = plan_the_path((i,j), DIAGRAM2_G)
            cp = path.pop(0)
            continue
        else:
            print "So, no need for planning the path again.\n"
        np = path.pop(0)
        # 2: check about extra orientation turn
        print "Checking for extra turn (a change in path orientation)..."
        if (np[0] - cp[0] == -1): # => no = RIGHT
            print("Need of extra turn: RIGHT\n")
            exo = 90
        elif (np[0] - cp[0] == 1): # => no = LEFT
            print("Need of extra turn: LEFT\n")
            exo = -90
        else:
            print("No need for extra turn...\n")
            exo = 0
        # 3: change the orientation; use the Pythagorean Theorem for calculating the new required distance 
        # and angle to move to the next tile
        a = x - (np[1] * CELL_SIZE + CELL_SIZE / 2)
        b = y - (np[0] * CELL_SIZE + CELL_SIZE / 2)
        distance = math.sqrt(a ** 2 + b ** 2) / 100 # distance is needed in m.
        no = math.atan(float(a) / b) + exo
        # TODO: remove. (Temporary, just to visually check the soundness of the results)
        raw_input("Press Enter to continue...\n")
        change_orientation(mc, int(co), int(no))
        # 4: move a tile forward and at the same time measure the distance and angle reported by the light 
        # sensors (encoders) during the last step. Use this information to get an estimation on the grid 
        # position if beacon information is not sufficient.
        x_enc, y_enc, theta_enc = move_forward(mc, distance)
        raw_input("Press Enter to continue...\n")
        # 5: acquire estimated position on the grid
        try:
            x, y, i, j, co = self_localize(sl)
        except InsufficientLocalizationInfoError, ValueError:
            # At this stage, the (blind) AlphaBot has no environmental information regarding its position.
            # It now relys solely on the information coming from the encoders. 
            print("Beacon information not sufficient for localizing. Now using encoders' output...")
            print("Last known beacon-based position estimation: Row = "+ str(int(i)) + ", Column = " + 
                    str(int(j)) + ", x = " + str(int(x)) + "cm , y = " + str(int(y)) + 
                    "cm and Orientation = " + str(int(co)) + "deg")
            x += x_enc
            y += y_enc
            co -= theta_enc
            i = y // CELL_SIZE
            j = x // CELL_SIZE
            print("Current encoder-based position estimation: Row = "+ str(int(i)) + ", Column = " + 
                    str(int(j)) + ", x = " + str(int(x)) + "cm , y = " + str(int(y)) + 
                    "cm and orientation = " + str(int(co)) + "deg")
        # Current position in grid is last step's next position
        cp = np
        print("\n---------------------------------")
        print("End of Step")
        print("---------------------------------\n")
    # TODO: Check here if I am really at the target, otherwise rerun
    print("\n\n\n ---------------------- GOAL REACHED (or at least I think so) ----------------------\n\n\n ")

if __name__ == "__main__":
    main()
