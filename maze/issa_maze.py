import random

'''
Pranav 
⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠉⠉⠉⠛⠻⣿⣿⠿⠛⠛⠙⠛⠻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⢀⣀⣀⡀⠀⠈⢄⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠏⠀⠀⠀⠔⠉⠁⠀⠀⠈⠉⠓⢼⡤⠔⠒⠀⠐⠒⠢⠌⠿⢿⣿⣿⣿
⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⢀⠤⣒⠶⠤⠭⠭⢝⡢⣄⢤⣄⣒⡶⠶⣶⣢⡝⢿⣿
⡿⠋⠁⠀⠀⠀⠀⣀⠲⠮⢕⣽⠖⢩⠉⠙⣷⣶⣮⡍⢉⣴⠆⣭⢉⠑⣶⣮⣅⢻
⠀⠀⠀⠀⠀⠀⠀⠉⠒⠒⠻⣿⣄⠤⠘⢃⣿⣿⡿⠫⣿⣿⣄⠤⠘⢃⣿⣿⠿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠤⠭⣥⣀⣉⡩⡥⠴⠃⠀⠈⠉⠁⠈⠉⠁⣴⣾⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠔⠊⠀⠀⠀⠓⠲⡤⠤⠖⠐⢿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿
⠀⠀⠀⠀⠀⠀⠀⢸⣿⡻⢷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣘⣿⣿
⠀⠀⠀⠀⠀⠠⡀⠀⠙⢿⣷⣽⣽⣛⣟⣻⠷⠶⢶⣦⣤⣤⣤⣤⣶⠾⠟⣯⣿⣿
⠀⠀⠀⠀⠀⠀⠉⠂⠀⠀⠀⠈⠉⠙⠛⠻⠿⠿⠿⠿⠶⠶⠶⠶⠾⣿⣟⣿⣿⣿
⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿
⣿⣿⣶⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣟⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
'''

maze = [
    'X00X000000',
    'X0X000X0X0',
    'X0X0XX000X',
    '0000X00XX0',
    'X0X0X00X0X',
    '00X00X0X00',
    'XXX000X00X',
    'X00X00XX0X',
    '000X0000X0',
    '0X00XX0XX0',
    '00X00X00X0',
    'X0000XX000',
    'XX0X0000X0',
    'X00XX0XXX0',
    '0000000000',
    'X00XX00X0X',
    '00000X0X00',
    '0X0X0X0X0X',
    '0X00000000',
    '000X00X00X',
]

obstacles_lst = list()
open_spaces = []


def get_walls():
    '''
    Gets bottom left coordinate of each cell wall
    '''
    current_coords = [-100, 180]

    for row in maze:
        for block in list(row):
            current_x, current_y = current_coords[0], current_coords[1]
            if block == 'X':
                obstacles_lst.append((current_x, current_y))
            else:
                current_space = open_space_coords((current_x, current_y))
                open_spaces.append(tuple(current_space))
            current_coords[0] += 20
        current_coords[1] -= 20
        current_coords[0] = -100
    
    random_space = random.choice(open_spaces)
    
    return list(random_space)

# l = [(x,y) for x in range(0,6) for y in range(0,6)]


def open_space_coords(current_coords):
    x = current_coords[0]
    y = current_coords[1]
    x += 10
    y += 10
    return [x, y]


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


#Morgan added this
get_walls()
generate_obstacles = lambda : obstacles_lst
