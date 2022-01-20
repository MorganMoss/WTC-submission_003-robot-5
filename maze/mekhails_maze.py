scale = 40

maze_coords = []


def is_position_blocked(x,y):
    """
    checks to see if any position
    on any axis has an obstacle.

    Args:
        x (int): 
        x coordinate of the robot.

        y (int): 
        y coordinate of the robot.

    Returns:
        bool: 
        True if the robots x and y axis is in between the obstacles
        coordinates.
        else False.
    """

    global maze_coords,scale

    for coord in maze_coords:

        obj_min_x = coord[0]
        obj_max_x = coord[0] + scale

        obj_min_y = coord[1] - scale
        obj_max_y = coord[1]

        if obj_min_x <= x <= obj_max_x and obj_min_y <= y <= obj_max_y:
            return True

    return False


def is_path_blocked(x1,y1,x2,y2):
    """
    Checking to see if the obstacle is in between
    the robots old and new destination.

    Args:
        x1 (int): 
        old x coordinate of robot.

        y1 (int): 
        old y coordinate of robot.

        x2 (int): 
        new x coordinate of robot.

        y2 (int): 
        new y coordinate of robot.

    Returns:
        Bool: 
        True if the object is in range of the 
        robots old and new coordinates.
        else False.
    """

    global maze_coords,scale
    x = 0
    y = 1

    for obj in maze_coords:

        max_x = obj[x] + scale
        min_y = obj[y] - scale

    #checking to see if the coordinates of the obstacle is in range
    #of the robots old and new y coordinates.
        if x1 == x2:
            if y1 <= min_y <= obj[y] <= y2 and obj[x] <= x1 <= max_x:
                return True

    #inversing the top
            if y1 >= obj[y] >= min_y >= y2 and obj[x] <= x1 <= max_x:
                return True

    #checking to see if the coordinates of the obstacle is in range
    #of the robots old and new x coordinates.
        if y1 == y2:
            if x1 <= obj[x] <= max_x <= x2 and min_y <= y1 <= obj[y]:
                return True

    #inversing the top
            if x1 >= max_x >= obj[x] >= x2 and min_y <= y1 <= obj[y]:
                return True

    return False


def draw_maze(min_x,min_y):
    global maze_coords,scale

    maze = [
    "XXXX XX XXXXX",
    "XX   X   XX  ",
    "XX XXX XXXX X",
    "XX  XX   XX X",
    "     XX X   X",
    "XX XXX    XXX",
    "XX X XXX    X",
    "XX X     XXXX",
    "XX    X      ",
    "XX XX XXXXXXX",
    "XX XX      XX",
    "XX XX XXX XXX",
    "XX XXXXXX XXX",
]
    maze.reverse()

    counter = 0
    x = min_x
    y = min_y
    
    for walls in maze:

        x = min_x
        y += scale

        for index in walls:

            if index == "X":
                maze_coords.append((x,min_y + counter))
                x += scale

            else:
                x += scale

        counter += scale

    maze_coords.reverse()
    return maze_coords


def clear_obj_coords():
    """
    Clearing the global varaible.
    in the obstacles moduel.
    """
    global maze_coords
    maze_coords = []

