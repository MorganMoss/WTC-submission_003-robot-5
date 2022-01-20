import random

obstacles_lst = list()


def get_num_obstacles():
    '''
    Gets a random number of obstacles.
    '''
    num_obstacles = random.randint(1,10)

    return num_obstacles

# l = [(x,y) for x in range(0,6) for y in range(0,6)]


def is_position_blocked(x,y):
    '''
    Returns true if the position is in an obstacle.
    '''
    for obstacle in obstacles_lst:
        obs_block = [(x_, y_) for x_ in range(obstacle[0], (obstacle[0]+20)) \
                        for y_ in range(obstacle[1], (obstacle[1]+20))]

        if (x,y) in obs_block:
            return True

    return False
    

def is_path_blocked(x1, y1, x2, y2):
    '''
    Returns true if the robots movement/path is blocked by an obstacle.
    '''
    if x2 < 0 and y2 < 0:
        path = [(x_, y_) for x_ in range(x1, (x2-1), -1) for y_ in range(y1, (y2+1), -1)]
    elif x2 < 0:
        path = [(x_, y_) for x_ in range(x1, (x2-1), -1) for y_ in range(y1, (y2+1))]
    elif y2 < 0:
        path = [(x_, y_) for x_ in range(x1, (x2+1)) for y_ in range(y1, (y2-1), -1)]
    else:
        path = [(x_, y_) for x_ in range(x1, (x2+1)) for y_ in range(y1, (y2+1))]

    for x,y in path:
        if is_position_blocked(x,y):
            return True
            
    return False


def get_obstacles():
    '''
    Returns a list of obstacles.
    All x,y values within the set area limit.
    '''
    num_obs = get_num_obstacles()
    global obstacles_lst

    obstacles_lst = []

    for _ in range(num_obs):
        x = 0
        y = 0
        while x == 0 and y == 0:
            x = random.randint(-100, 100)
            y = random.randint(-200, 200)

        obstacles_lst.append((x,y))
    return obstacles_lst

def start_obstacles():
    '''
    Initializes obstacle list.
    '''
    global obstacles_lst
    obstacle_lst = get_obstacles()


