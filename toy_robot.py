from command_handling.input_exceptions import InputError

class ToyRobot():
    """
    This class uses the Command Handler and Command classes
    to be able to execute commands on itself via user input.
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

        
    def start(self) -> None:
        """ 
        Gets the robot to ask for a name and say hello.
        """
        self.robot_get_name()
        self.robot_say_message(
            "Hello kiddo!", 
            f"{self.name}: "
        )   


    def cmd(self, world, commands, command_handler) -> None:
        """
        Receives and executes a user input command 
        for this robot in a specific world.

        Args:
            world (World): The world in which you want to place a robot.
            commands (Commands): The commands object you want to call commands from.
            command_handler (CommandHandler): The input validator you wish to use.
        """
        self.robot_say_message(
            "What must I do next? ",
            f"{self.name}: ",
            ''
        )
        try:
            # main tests fail unless I take the command string 
            # to exec_command for one single error message >:(
            command, command_str = command_handler.get_command()
            commands.exec_command(world, self, command, command_str)
        except InputError as e:
                self.robot_say_message(str(e), f"{self.name}: ")
                

    def __init__(self) -> None:
        """
        Constructor for ToyRobot.
        """
        self.name:str = ''
        self.messages_enabled:bool = True

        

