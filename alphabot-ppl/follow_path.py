from grid_nav import *
import os
import subprocess
from self_locator import *
from micro_controller import *

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
GRID_COLUMNS = 5
GRID_ROWS = 5

# BEACON_COLORS = [0, 1, 2, 3, 4]
BEACON_COLUMNS = [2, 4, 0, 4, 0]
BEACON_ROWS = [4, 2, 4, 4, 2]
CELL_SIZE = 50

DIAGRAM2 = GridWithWeights(GRID_COLUMNS, GRID_ROWS)
DIAGRAM2_S = (2,0) # Start
DIAGRAM2_G = (2,3) # Goal
ORIENT_REF_ROW = 4 # Red Beacon

# Encode Moveset
RIGHT = 4
LEFT = 2
DOWN = 3
UP = 1

# Rotate AlphaBot according to its new desired orientation
def change_orientation(mc, co, no):
    diff = no - co
    if (diff == 1 or diff == 3):
        print("Rotating LEFT!")
        pos_arry = [0, 0, 0, 0, 0, 1.65]
    elif (diff == -1 or diff == -3):
        print("Rotating RIGHT!")
        pos_arry = [0, 0, 0, 0, 0, -1.65]
    # Can only happen during first move
    elif (diff == 2 or diff == -2):
        print("Rotating BACKWARDS!")
        pos_arry = [0, 0, 0, 0, 0, 3.3]
    else:
        print("No need for rotation...")
        pos_arry = [0, 0, 0, 0, 0, 0]
    mc.move_and_control(pos_arry)

# Move AlphaBot one tile forward
def move_forward(mc):
    print("Moving FORWARD!")
    pos_arry = [0, 0, 0, 0.5, 0, 0]
    mc.move_and_control(pos_arry)

# Return estimated AlphaBot's position in grid (column, row, orientation)
def self_localize(self_locator):
    print("Self Localising...")
    b_distance, b_angle, b_color = self_locator.dna_from_beacons()
    x, y, column, row = detect_position_in_grid(b_distance, b_color)
    orientation = detect_orientation(x, y, b_distance[0], b_angle[0], b_color[0]) # angle from the first beacon is enough
    print column, row, orientation
    return column, row, orientation

# Detect AlphaBot's orientation (degrees) relevant to a reference point in grid
def detect_orientation(ax, ay, distance, theta_beac, color):
    rx = ORIENT_REF_ROW * CELL_SIZE + CELL_SIZE / 2
    ry = ay
    bx = BEACON_ROWS[color] * CELL_SIZE + CELL_SIZE / 2
    by = BEACON_COLUMNS[color] * CELL_SIZE + CELL_SIZE / 2 

    # beacon - alphabot distance
    bad = round(distance)
    print("Beacon - AlphaBot distance: " + str(bad))
    # beacon - ref distance
    brd = round(math.sqrt((bx - rx) ** 2 + (by - ry) ** 2))
    print("Beacon - Reference Point distance: " + str(brd))
    # alphabot - ref distance
    ard = round(math.sqrt((ax - rx) ** 2 + (ay - ry) ** 2))
    print("AlphaBot - Reference Point distance: " + str(ard))

    # Cosine Rule
    a = round(math.degrees(math.acos((bad ** 2 + ard ** 2 - brd ** 2) / (2 * bad * ard))), 2)
    print("Cosine Rule Angle: " + str(a))
    
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
    print("Orientation Angle: " + str(theta_or))

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

def main():
    sl = SelfLocator(300)
    mc = MicroControler()
    # Solve A* and visualise path
    came_from, cost_so_far = a_star_search(DIAGRAM2, DIAGRAM2_S, DIAGRAM2_G)
    draw_grid(DIAGRAM2, width=3, point_to=came_from, start=DIAGRAM2_S, goal=DIAGRAM2_G)
    print("")
    draw_grid(DIAGRAM2, width=3, number=cost_so_far, start=DIAGRAM2_S, goal=DIAGRAM2_G)
    print("")
    draw_grid(DIAGRAM2, width=3, path=reconstruct_path(came_from, start = DIAGRAM2_S, goal = DIAGRAM2_G))
    path = reconstruct_path(came_from, start = DIAGRAM2_S, goal = DIAGRAM2_G)
    print(path)

    # Start following path
    print("Start following path...")
    cp = path.pop(0) # Get starting position
    co = DOWN # Assume that starting orientation is down
    move = 0
    while path: # While path_list not empty
        move += 1 
	np = path.pop(0) # Get next position
	# Define new orientation
        if (np[0] - cp[0] == 1): # => no = RIGHT
            print("RIGHT")
            no = RIGHT # new orientation
        elif (np[0] - cp[0] == -1): # => no = LEFT
            print("LEFT")
            no = LEFT
        elif (np[1] - cp[1] == 1):
            print("DOWN")
            no = DOWN
        elif (np[1] - cp[1] == -1):
            print("UP")
            no = UP
        else:
            print("Invalid Next Move")
        change_orientation(mc, co, no)
        cp = np
        co = no
        move_forward(mc)
        column, row, orientation = self_localize(sl)
        print("_________________________________")
        print("End of Step")
        print("---------------------------------")
    print("Goal Reached")

if __name__ == "__main__":
    main()
