

from numpy import char


obstacles_list = []

exit_coord = []

def get_obstacles():

    """
    Generates a list of obstacles using from a predefined list containing characters
    :param command:
    :return: obstacles_list
    """


    #list is used in a loop to determine how many obstacles are in each row and column
    # The length of the list signifies the number of columns
    # The length of each item in the list signifies the number of rows

    global obstacles_list,exit_coord
    obstacles_list = []
    exit_coord = []

    walls = [
"XEXXXXXXXXXXXXXXXXXXXXXXX",
"X XXXXXXXXXXXXXXXXXXXXX X",
"X                       X",
"X                       X",
"XXXXXXXXXXXXXXXXXXXXXXX X",
"XXXXXXXXXXXXXXXXXXXXXXX X",
"X                     X X",
"X                     X X",
"X XXXXXXXXXXXXXXXXXXX X X",
"X XXXXXXXXXXXXXXXXXXX X X",
"X X                 X X X",
"X X                 X X X",
"X X XXXXXXXXXXXXXXX X X X",
"X X XXXXXXXXXXXXXXX X X X",
"X X X             X X X X",
"X X X             X X X X",
"X X X XXXXXXXXXXX X X X X",
"X X X XXXXXXXXXXX X X X X",
"X X X X         X X X X X",
"X X X X         X X X X X",
"X X X X XXXXXXX X X X X X",
"X X X X XXXXXXX X X X X X",
"X X X X X     X X X X X X",
"X X X X X     X X X X X X",
"X X X X X X P X X X X X X",
"X X X X X X   X X X X X X",
"X X X X X X   X X X X X X",
"X X X X X X   X X X X X X",
"X X X X X XXXXX X X X X X",
"X X X X X XXXXX X X X X X",
"X X X X X       X X X X X",
"X X X X X       X X X X X",
"X X X X XXXXXXXXX X X X X",
"X X X X XXXXXXXXX X X X X",
"X X X X           X X X X",
"X X X X           X X X X",
"X X X XXXXXXXXXXXXX X X X",
"X X X XXXXXXXXXXXXX X X X",
"X X X               X X X",
"X X X               X X X",
"X X XXXXXXXXXXXXXXXXX X X",
"X X XXXXXXXXXXXXXXXXX X X",
"X X                   X X",
"X X                   X X",
"X XXXXXXXXXXXXXXXXXXXXX X",
"X XXXXXXXXXXXXXXXXXXXXX X",
"X                       X",
"X                       X",
"X XXXXXXXXXXXXXXXXXXXXX X",
"XXXXXXXXXXXXXXXXXXXXXXXXX",
]

    for row in range(len(walls)): #How many rows we have OR the number of items in a list
            for col in range(len(walls[row])): # The number of columns OR the number of elements each items in a list contains
                    # calculate the screen x ,y coordinates

                    screen_x = (-99 + (col *8))
                    screen_y = (195- (row *8))

                    character = walls[row][col]

                    # Check if it is a X (representing the obsticles)
                    if character =="X":
                            obstacles_list.append((screen_x,screen_y))

                    if character =="E":
                            exit_coord.append((screen_x,screen_y))
                                           

    return (obstacles_list,exit_coord)
        


def is_position_blocked(x,y):
    """
    Checks if the position entered is blocked by an obsticles and returns True is blocked
    :param command: x,y
    :return: True
    """

    for i in obstacles_list:
        
        if x in range(i[0],i[0]+4) and y in range(i[1],i[1]+4):
            return True


def is_path_blocked(x1,y1, x2, y2):
    """
    Checks if the path of the position entered contains an obsticles and returns True 
    if an obstacle is on the same path
    :param command: x1,y1, x2, y2
    :return: True
    """
    
    for i in range(0,len(obstacles_list)):

        obs_x =obstacles_list[i][0]
        obs_y = obstacles_list[i][1]

        obs = (obs_x, obs_y)

        # x1 == x2
        if (x1 == obs_x == x2) and (min(y1,y2) <= obs_y <= max(y1,y2)):
            return True
        
        # y1 == y2
        elif (y1 == obs_y == y2) and (min(x1,x2) <= obs_x <= max(x1,x2)):
            return True

