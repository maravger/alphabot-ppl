from simple_grid_nav import *

DIAGRAM1 = GridWithWeights(10, 10)
DIAGRAM1.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
DIAGRAM1.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6), 
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6), 
                                       (5, 7), (5, 8), (6, 2), (6, 3), 
                                       (6, 4), (6, 5), (6, 6), (6, 7), 
                                       (7, 3), (7, 4), (7, 5)]}
# (Column, Row)
DIAGRAM1_S = (1,4)
DIAGRAM1_G = (7,8)

DIAGRAM2 = GridWithWeights(10,10)
DIAGRAM2_S = (5,0)
DIAGRAM2_G = (5,9)

RIGHT = 4
LEFT = 2
DOWN = 3
UP = 1

def change_orientation(no, co)
    diff = no - co
    if (diff == 1 or diff == 3):
       # rotate left 

def main():
    # Solve A* and visualise path
    came_from, cost_so_far = a_star_search(DIAGRAM2, DIAGRAM2_S, DIAGRAM2_G)
    draw_grid(DIAGRAM2, width=3, point_to=came_from, start=DIAGRAM2_S, goal=DIAGRAM2_G)
    print()
    draw_grid(DIAGRAM2, width=3, number=cost_so_far, start=DIAGRAM2_S, goal=DIAGRAM2_G)
    print()
    draw_grid(DIAGRAM2, width=3, path=reconstruct_path(came_from, start = DIAGRAM2_S, goal = DIAGRAM2_G))
    path = reconstruct_path(came_from, start = DIAGRAM2_S, goal = DIAGRAM2_G)
    print(path)

    # Start following path
    cp = path.pop(0) # Get starting position
    while path: # While path_list not empty
        #print(path)
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
         
        cp = np

if __name__ == "__main__":
    main()
