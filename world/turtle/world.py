import turtle
from world.text.world import World
from toy_robot.robot_base import BaseRobot


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
        if cell_size > 10:
            self.scale = 16

        self.screen = turtle.getscreen()
        self.screen.screensize(
            (bounds_x[1]-bounds_x[0])*self.scale/cell_size+1,
            (bounds_y[1]-bounds_y[0])*self.scale/cell_size+cell_size*2
        )

        self.screen.xscale=self.scale/cell_size
        self.screen.yscale=self.scale/cell_size
        
        self.screen.bgcolor("black")

        turtle.pencolor("red")
        turtle.fillcolor("orange")
        turtle.speed(0)
        self.draw_box(*bounds_x,*bounds_y)
        self.draw_obstacles()
        self.robot_turtles = dict()


    def add_robot(
        self, robot: BaseRobot, 
        start_pos: tuple = (0,0), direction: float = 0) -> None:
        """
        Add a robot to the world.

        Args:
            robot (BaseRobot): The robot to add
            start_pos (tuple, optional): Position it starts at. Defaults to (0,0).
            direction (float, optional): Direction it faces. Defaults to 0.
        """
        super().add_robot(robot, start_pos=start_pos, direction=direction)
        self.robot_turtles[robot] = turtle.Turtle(visible=False, shape='turtle')
        self.robot_turtles[robot].penup()
        self.robot_turtles[robot].color("dark green")
        self.robot_turtles[robot].shapesize(self.cell_size/20*(self.scale-1)/self.cell_size)
        self.robot_turtles[robot].goto(*start_pos)
        self.robot_turtles[robot].lt(90)
        self.robot_turtles[robot].pendown()
        self.robot_turtles[robot].showturtle()
        robot.messages_enabled = False
        self.rotate_robot(robot, direction)
        robot.messages_enabled = True

        
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

        for obstacle in self.obstacles.obstacles:
            x1, y1 = obstacle.pos
            x2, y2 = obstacle.end_pos
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


    def rotate_robot(self, robot: BaseRobot, angle: float) -> None:
        """
        Rotates robot, now with visuals.

        Args:
            robot (BaseRobot): The robot to be rotated.
            angle (float): The degrees by which it rotates.
        """
        super().rotate_robot(robot, angle)
        self.robot_turtles[robot].rt(angle)


    def move_robot(self, robot: BaseRobot, steps: int) -> bool:
        """
        Moves the robot, now with visuals.

        Args:
            robot (BaseRobot): The robot to be moved
            steps (int): The distance it moves

        Returns:
            bool: True if move was successful
        """
        b = super().move_robot(robot, steps)
        self.robot_turtles[robot].goto(self.robot_pos[robot.name])
        return b