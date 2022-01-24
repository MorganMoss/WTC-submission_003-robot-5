from random import randint

SCALE = 8
HEIGHT, WIDTH = 400//SCALE,200//SCALE
MAZE_CENTRE_Y = range(HEIGHT//2-3,HEIGHT//2+3)
MAZE_CENTRE_X = range(WIDTH//2-3,WIDTH//2+3)

def create_blank_maze():
    '''
    creates a blank maze grid with dimensions of the constants height and width
    :return: (2d list) - maze with '+' as walls and ' ' as spaces
    '''
    return [['+' if i%2==1 or j%2==1 else '_' for j in range(WIDTH)]for i in range(HEIGHT)]


def create_maze():
    '''
    creates a maze with dimensions of the constants height and width
    :return: maze (2d list) - maze with '+' as walls and ' ' as spaces
    '''
    maze = create_blank_maze()
    for i in range(HEIGHT):
        if i<WIDTH-1: 
            maze[HEIGHT-1][i]='_'
        maze[i][WIDTH-1]='_'
        
    for i in range(0,HEIGHT-1,2):
        for j in range(0,WIDTH-1,2):
            if bool(randint(0,1)): maze[i][j+1]='_'
            else: maze[i+1][j]='_'
    return maze


def get_obstacles():
    '''
    converts maze to a list of obstacles
    :return: walls_coords (list) list of [x,y] coordinates of each cell from the walls
    '''
    maze = create_maze()
    walls_coords = []
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if maze[row][col]=='+' and not (row in MAZE_CENTRE_Y and col in MAZE_CENTRE_X):
                x,y = col*SCALE-100+4,row*SCALE-200+4
                walls_coords.append([x,y])
                walls_coords.append([x+4,y])
                walls_coords.append([x+4,y+4])
                walls_coords.append([x,y+4])
    return walls_coords


def is_position_blocked(position, obstacles): 
    '''
    checks if a position falls inside an obstacle
    :param: position (list) [x,y] positional coordinates
    :param: obstacles (list) list of obstacles
    :return: (bool) True if position falls inside an obstacle
    '''
    x,y = position
    for obs in obstacles:
        if x in range(obs[0],obs[0]+5) and y in range(obs[1],obs[1]+5):
            return True
    return False


def is_path_blocked(x1,y1,x2,y2, obstacles):
    '''
    checks if robot can move without hitting an obstacle
    :param: x1 (int) current x positional coordinate of the robot
    :param: y1 (int) current y positional coordinate of the robot
    :param: x2 (int) new x positional coordinate of the robot
    :param: y2 (int) new y positional coordinate of the robot
    :param: obstacles (list) list of obstacles
    :return: True if no obstacle in the way
    '''
    if (x1,y1,x2,y2) == (0,0,0,0):
        return False
    x_dir,y_dir = -1 if x2<x1 else 1,-1 if y2<y1 else 1
    x_ctrl = abs(x2-x1) >= abs(y2-y1)
    m = abs((y2-y1)/(x2-x1)) if x_ctrl else abs((x2-x1)/(y2-y1))
    if is_position_blocked([x2,y2], obstacles): return True
    while [int(round(x1)),int(round(y1))] != [x2,y2]:
        x_temp,y_temp = int(round(x1)),int(round(y1))
        if is_position_blocked([x_temp,y_temp],obstacles):
            return True
        x1 += x_dir*(1 if x_ctrl else m)
        y1 += y_dir*(m if x_ctrl else 1)
    return False

