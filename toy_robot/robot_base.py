import math

class BaseRobot():
    """
    An instance of this class is a robot that can be 
    controlled via commands and sends messages to the console.
    It needs to be put in a world to move around.
    """
    def robot_say_message(self, message:str, start:str = "", end:str = "\n"):
        """
        Robot Sends message to console.

        Args:
            message (str): The text the robot sends to the console.
            start (str, optional): print something before message. 
            Defaults to empty string.
            end (str, optional): string appended after the last value. 
            Defaults to newline.
        """
        if self.messages_enabled:
            print(f"{start}{message}" , end = end) 
    
    
    def robot_get_name(self):
        """
        Sets robots name to a given input.
        """
        self.robot_say_message("What do you want to name your robot? ", end="")
        self.name = input()


    def __init__(self) -> None:
        """
        Constructor that sets the default values for the robot
        when a new instance of it is created.

        Args:
            name (str, optional): Robot's name. Defaults to "".
            position (tuple, optional): Starting position. Defaults to (0,0).
            rotation (int, optional): Starting direction. Defaults to 0.
        """
        # self.bounds:tuple = ((-100, 100), (-200, 200))
        # self.position:tuple = (0,0)
        # self.rotation:int = 0
        self.name:str = ''
        self.messages_enabled:bool = True
