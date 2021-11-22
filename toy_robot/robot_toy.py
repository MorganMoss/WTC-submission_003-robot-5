from command_handling import CommandHandler,Commands,InputError
from toy_robot.robot_base import BaseRobot
from world.text.world import World


class ToyRobot():
    """
    This class uses the Command Handler and Command classes
    to be able to execute commands on a robot via user input.
    """


    def cmd(self, world:World, commands:Commands, command_handler:CommandHandler) -> None:
        """
        Receives and executes a user input command 
        for this robot in a specific world.

        Args:
            world (World): The world in which you want to place a robot.
            commands (Commands): The commands object you want to call commands from.
            command_handler (CommandHandler): The input validator you wish to use.
        """
        self.robot.robot_say_message(
            "What must I do next? ",
            f"{self.robot.name}: ",
            ''
        )
        try:
            # main tests fail unless I take the command string 
            # to exec_command for one single error message >:(
            command, command_str = command_handler.get_command()
            commands.exec_command(world, self.robot, command, command_str)
        except InputError as e:
                self.robot.robot_say_message(str(e), f"{self.robot.name}: ")
                

    def start(self) -> None:
        """ 
        Gets the robot to ask for a name and say hello.
        """
        self.robot.robot_get_name()
        self.robot.robot_say_message(
            "Hello kiddo!", 
            f"{self.robot.name}: "
        )   


    def __init__(self) -> None:
        """
        Constructor for ToyRobot. Creates a Base Robot to use.
        """
        self.robot = BaseRobot()

        

