"""
Ryan Markus Poggers
"""

import turtle
import world.turtle.world as world

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.shapesize(0.9)
        self.penup()
        self.speed(0)

class Goal(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.shapesize(0.9)
        self.color("green")
        self.pu()
        self.speed(0)

levels = [""]

level_1 = [
"XXXXXXXXXGXXXXXXXXXXXXXXX",
"X XXXXXXX XXXXXXXX  XXXXX",
"X       X        X XXXXXX",
"X  X XXXXXXXXXXX       XX",
"X XXXXXXX     XX XXXXX XX",
"X X       XXX    XX    XX",
"X X XXXXXX   XXXXXX XX XX",
"X X    XXX X        XX XX",
"X   XX X    XXXXXXXXXX XX",
"G XXXX XXXX    X  XXXX  G",
"XXX       XXX  XX XXXXXXX",
"X X XXXXX  XXX    XXX XXX",
"X  XX   X XXXXXXX XXX XXX",
"XX XX X X  XXPXX      XXX",
"XX XX XXXX       XXXXXXXX",
"XX         XXXXX XXXXXXXX",
"XXXXXX XXXXXXXXX XX    XX",
"XX      XXXX   X XX X XXX",
"XX XXX       X   XXXX XXX",
"X  XXX XXXXXXXXX XXXX XXX",
"X XXXX XXXXXXXXX   X  XXX",
"X   XXXXX   XXXXXX   XXXX",
"XXX    XX X   XXXX XXXXXX",
"XXXXXX     XX X         X",
"XXXXXXXXXXXXXGXXXXXXXXXXX",
]

levels.append(level_1)

walls = []
goals = []
open_space = []
player = []

import world.turtle.world as world

def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            char = level[y][x]
            screen_x = -240 + (x * 20)
            screen_y = 240 - (y * 20)

            if char == "X":
                pen.goto(screen_x,screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))

            if char == "P":
                world.turtle_robot.goto(screen_x,screen_y)
                world.x = screen_x
                world.y = screen_y
                player.append((screen_x, screen_y))
            
            if char == "G":
                goal.goto(screen_x, screen_y)
                goal.stamp()
                goals.append((screen_x, screen_y))
            
            if char == " ":
                open_space.append((screen_x, screen_y))
    # print(goals)

    pen.hideturtle()
    goal.hideturtle()
                

pen = Pen()
goal = Goal()

# setup_maze(levels[1])
def is_position_blocked(command):
    """
    This function creates mock position for where the robot is going
    Then will check if the mock position is where any obstacle is
    if there is a obstacle at the position then the variable blocked will be true
    if not the blocked will stay false
    and then the function will return blocked"""
    blocked = False
    new_x = world.x
    new_y = world.y
    if world.robot_direction == "":    
        if command[0] == "forward":
            new_y = new_y + int(command[1])
        elif command[0] == "back":
            new_y = new_y - int(command[1])
    elif world.robot_direction == "left":
        if command[0] == "forward":
            new_x = new_x - int(command[1])
        elif command[0] == "back":
            new_x = new_x + int(command[1])
        
    elif world.robot_direction == "right":
        if command[0] == "forward":
            new_x = new_x + int(command[1])
        elif command[0] == "back":
            new_x = new_x - int(command[1])

    elif world.robot_direction == "backwards":
        if command[0] == "forward":
            new_y = new_y - int(command[1])
        elif command[0] == "back":
            new_y = new_y + int(command[1])
    for i in walls:
        if i[0]-9 <= new_x <= i[0]+9 and i[-1]-9 <= new_y <= i[-1]+9:
            blocked = True

    return blocked


def is_path_blocked(command):
    """
    this function creates the length of the path the robot is going to take
    then in a for loop will check if there is obstacles in
    each step the robot will take by using the is position blocked function
    and blocked will change to true if there is a position
    """
    length = int(command[-1])
    blocked = False
    for i in range(length):
        new_command = [command[0], i]
        if is_position_blocked(command=new_command) == True:
            blocked = True
    return blocked


def escaped():
    for i in goals:
        if i[0] == world.x and i[-1] == world.y:
            pen.clear()
            goal.clear()
            goal.write(arg="""Congratulations!
You escaped""", move=False, font=('Arial', 40, 'normal'), align='left')
            print("Congratulations! You escaped")
        
