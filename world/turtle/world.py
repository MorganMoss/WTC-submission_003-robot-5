import turtle
from world.text.world import World
from toy_robot import ToyRobot


class TurtleWorld(World):
    """
    Builds a 2D visual for the text based world.

    Inheritance:
        World : The text based world
    """
    

    def __init__(
        self, maze:type,
        bounds_x:tuple=(-100,100),
        bounds_y:tuple=(-200,200),
        cell_size:int = 4) -> None:
        """
        Constructor for TurtleWorld. Initializes the inherited TextWorld,
        and then sets up turtle graphics for startup.

        Args:
            bounds_x (tuple, optional): 
             Horizontal boundary. Defaults to (-100,100).
            bounds_y (tuple, optional): 
             Vertical boundary. Defaults to (-200,200).
            cell_size (int): the size of the obstacles in this world
        """
        super().__init__(
            maze, bounds_x, bounds_y, cell_size
        )
    
        turtle.hideturtle()

        self.scale = 8
        if self.cell_size > 10:
            self.scale = 16

        self.screen = turtle.getscreen()
        self.screen.screensize(
            (self.bounds_x[1]-self.bounds_x[0])*self.scale/self.cell_size+1,
            (self.bounds_y[1]-self.bounds_y[0])*self.scale/self.cell_size+self.cell_size*2
        )

        self.screen.xscale=self.scale/self.cell_size
        self.screen.yscale=self.scale/self.cell_size
        
        self.screen.bgcolor("black")

        turtle.pencolor("red")
        turtle.fillcolor("orange")
        turtle.speed(0)
        self.screen.tracer(0)
        self.draw_box(*self.bounds_x,*self.bounds_y)
        self.draw_obstacles()
        self.robot_turtles = dict()
        self.screen.tracer(1)


    def __str__(self) -> str:
        """The str method for this class

        Returns:
            str: Gives info about the obstacles
        """
        return "(Shown in turtle)"

    def add_robot(
        self, robot: ToyRobot, 
        start_pos: tuple = (0,0), direction: float = 0) -> None:
        """
        Add a robot to the world.

        Args:
            robot (ToyRobot): The robot to add
            start_pos (tuple, optional): Position it starts at. Defaults to (0,0).
            direction (float, optional): Direction it faces. Defaults to 0.
        """
        super().add_robot(robot, start_pos=start_pos, direction=direction)
        self.robot_turtles[robot] = turtle.Turtle(visible=False, shape='turtle')
        self.robot_turtles[robot].penup()
        self.robot_turtles[robot].color("light blue")
        self.robot_turtles[robot].shapesize(self.cell_size/20*(self.scale-1)/self.cell_size)
        self.robot_turtles[robot].goto(*start_pos)
        self.robot_turtles[robot].lt(90)
        self.robot_turtles[robot].pendown()
        self.robot_turtles[robot].showturtle()
        robot.messages_enabled = False
        self.rotate_robot(robot, direction)
        robot.messages_enabled = True

        def move_foward():
            self.move_robot(robot, self.cell_size*2)
        def move_back():
            self.move_robot(robot, -self.cell_size*2)
        def turn_right():
            self.rotate_robot(robot, 90)
        def turn_left():
            self.rotate_robot(robot, -90)

        self.screen.onkey(move_foward, "Up")
        self.screen.onkey(move_back, "Down")
        self.screen.onkey(turn_right, "Right")
        self.screen.onkey(turn_left, "Left")

        
    def draw_box(
        self, x_low:int, x_high:int,
              y_low:int, y_high:int,
              fill:bool = False) -> None:
        """
        Draws a box in the turtle window.

        Args:
            x_low (int): left side x co-ordinate of box.
            x_high (int): right side x co-ordinate of box.
            y_low (int): top side y co-ordinate of box.
            y_high (int): bottom side y co-ordinate of box.
        """
        turtle.penup()
        turtle.goto(x_low,y_low)
        if fill:
            turtle.begin_fill()
        else:
            turtle.pendown()
        turtle.goto(x_low, y_high)
        turtle.goto(x_high, y_high)
        turtle.goto(x_high, y_low)
        turtle.goto(x_low, y_low)
        turtle.end_fill()


    def draw_obstacles(self) -> None:
        """
        Draws the obstacles that are contained in this world
        """
        turtle.pencolor("orange")
        turtle.penup()
        turtle.shape("square")
        turtle.turtlesize(self.cell_size/20*(self.scale-1)/self.cell_size)

        for obstacle in self.obstacles:
            x1, y1 = obstacle[0]
            x2, y2 = obstacle[1]
            x = (x1 + x2)//2
            y = (y1 + y2)//2
            turtle.goto(x,y)
            turtle.stamp()

    
    def generate_obstacles(self) -> None:
        """
        Sets up the obstacles for this world.
        """
        super().generate_obstacles()
        self.draw_obstacles()


    def rotate_robot(self, robot: ToyRobot, angle: float) -> None:
        """
        Rotates robot, now with visuals.

        Args:
            robot (ToyRobot): The robot to be rotated.
            angle (float): The degrees by which it rotates.
        """
        super().rotate_robot(robot, angle)
        if angle > 0:
            self.robot_turtles[robot].rt(angle)
        else:
           self.robot_turtles[robot].lt(-angle) 


    def move_robot(self, robot: ToyRobot, steps: int) -> bool:
        """
        Moves the robot, now with visuals.

        Args:
            robot (ToyRobot): The robot to be moved
            steps (int): The distance it moves

        Returns:
            bool: True if move was successful
        """
        b = super().move_robot(robot, steps)
        self.robot_turtles[robot].goto(self.robot_pos[robot.name])
        return b


    def mazerun(self, robot: ToyRobot, goal_pos: tuple):
        """
        Solves the maze by mapping it out. This is faster.

        Args:
            robot (ToyRobot): The robot to be moved around
            goal_pos (tuple): The edge to land on
        """
        if not super().mazerun(robot, goal_pos):
            for pos in self.path:
                self.robot_turtles[robot].goto(pos)
                
    
    def enable_keys(self) -> None:
        """
        Allows movement with arrowkeys
        """
        self.screen.listen()
