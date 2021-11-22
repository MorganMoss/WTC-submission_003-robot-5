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
        self, bounds_x:tuple=(-100,100),
              bounds_y:tuple=(-200,200)) -> None:
        """
        Constructor for TurtleWorld. Initializes the inherited TextWorld,
        and then sets up turtle graphics for startup.

        Args:
            bounds_x (tuple, optional): 
             Horizontal boundary. Defaults to (-100,100).
            bounds_y (tuple, optional): 
             Vertical boundary. Defaults to (-200,200).
        """
        super().__init__(bounds_x=bounds_x, bounds_y=bounds_y)
    
        turtle.hideturtle()
        screen = turtle.getscreen()
        screen.xscale=1.5
        screen.yscale=1.5
        screen.bgcolor("black")
        turtle.pencolor("red")
        turtle.fillcolor("orange")
        self.draw_box(*bounds_x,*bounds_y)
        self.robot_turtles = dict()
  

    def add_robot(
        self, robot: BaseRobot, 
        start_pos: tuple = (0,0), direction: float = 0) -> None:
        super().add_robot(robot, start_pos=start_pos, direction=direction)
        self.robot_turtles[robot] = turtle.Turtle()
        self.robot_turtles[robot].shape('turtle')
        self.robot_turtles[robot].color("dark green")
        self.robot_turtles[robot].penup()
        self.robot_turtles[robot].hideturtle()
        self.robot_turtles[robot].goto(*start_pos)
        self.robot_turtles[robot].lt(90)
        self.robot_turtles[robot].pendown()
        self.robot_turtles[robot].showturtle()
        self.rotate_robot(robot, direction)
        
        


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
        turtle.speed(0)
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
        turtle.penup()


    def draw_obstacles(self) -> None:
        """
        Draws the obstacles that are contained in this world
        """
        for obstacle in self.obstacles.obstacles:
            x, y = obstacle.pos
            self.draw_box(x, x+4,y,y+4, fill=True)

    
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