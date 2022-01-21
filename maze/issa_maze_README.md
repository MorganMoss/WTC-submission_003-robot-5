Following code can be used wherever you draw the maze, e.g: world.turtle

in robot.py you can make your starting coordinate variable = issa_maze.get_walls() 
and make sure to call draw_maze()
^All can be done in robot_start()

Ask for help if this doesn't make any sense :)
maze not ready to be solved...

Maze keys:
X = Walls
0 = Empty Spaces // Not walls


def draw_cell():
        turtle.pendown()
        turtle.fillcolor('white')
        turtle.begin_fill()
        for i in range(4):
                turtle.fd(20)
                turtle.lt(90)
        turtle.end_fill()
        turtle.penup()
        turtle.fd(20)


def draw_maze():
    turtle.goto(-100,180)
    turtle.right(90)
    turtle.pensize(1)
    turtle.speed(0)
    size = 5
    turtle.color('white')

    for row in obstacle.maze:   #obstacle in obstacle.maze can be changed to whatever you
                                    reference the import as. 
                                    e.g: from maze import issa_maze as obstacle
        turtle.penup()
        for block in list(row):
            if block == 'X':
                draw_cell()
            else:
                turtle.fd(20)
        turtle.back(200)
        turtle.right(90)
        turtle.fd(20)
        turtle.left(90)

    random_space = random.choice(obstacle.open_spaces) #Again, change obstacle to whatever  
                                                        you have imported the maze as
    
    turtle.hideturtle()

    #rb in this case is the name of your robot/turtle that you control.

    rb.penup()
    rb.goto(random_space)
    rb.pendown()