from toy_robot import ToyRobot
from world.text.world import World

class Commands():      
    """
    This class inherits implements
    commands for robots and worlds.
    """


    def __init__(self) -> None:
        """
        Contructor for Commands, initializes a dictionary 
        containing all the commands above,
        with descriptions and arguments
        It also creates an empty history list 
        """
        self.history:list = list()
        """
        Rules for command_dict commands:
            * The key is the command word (in caps!).
            * The item is a dictionary:
                * requires "description" with a relevant explanation.
                * requires "command" that equals the relevant method in CommandRobot.
                * requires "history" for if it will be stored in robot history.
                * optional "args" if it needs any arguments, a list of types.
                    * if an str type is needed:
                        * have it at the end.
                        * have no optional arguments.
                        * have only one str argument.
                * optional "opt" if it has any optional arguments.
                    * if an str type is needed:
                        * have it at the end.
                        * have only one str argument.
        """
        self.command_dict:dict = {
        "OFF"       : { "description": "Shut down robot",
                        "command": "command_off" ,
                        "history": False},

        "HELP"      : { "description": "provide information about commands", 
                        "command": "command_help", 
                        "history": False},

        "FORWARD"   : { "description": "Move robot foward by [number] steps", 
                        "command": "command_forward", 
                        "args": [int],
                        "history": True},

        "BACK"      : { "description": "Move robot back by [number] steps", 
                        "command": "command_back", 
                        "args": [int],
                        "history": True},

        "RIGHT"     : { "description": "Rotate robot right", 
                        "command": "command_turn_right", 
                        "optional": [float],
                        "history": True},    

        "LEFT"      : { "description": "Rotate robot left", 
                        "command": "command_turn_left", 
                        "optional": [float],
                        "history": True},

        "SPRINT"    : { "description": "Move robot foward by [number] steps, "+
                        "then [number]-1 steps, and so on, until it hits 0.", 
                        "command": "command_sprint", 
                        "args": [int],
                        "history": True},   

        "HISTORY"   : { "description": "Shows history of movement commands.",
                        "command": "command_show_history",
                        "history": False},

        "REPLAY"    : { "description": "Replays previous movement commands.\n"+
                        "\t  It has optional arguments:"+
                        "\n\t\tSilent - Hides output from replayed commands"+
                        "\n\t\tReversed - Reverses the order to be last to first"+
                        "\n\t\t<int> - Starts from previous <int> commands"+
                        "\n\t\t<int>-<int> - Starts from previous <int> "+
                        "commands and ends at <int> previous commands", 
                        "command": "command_replay", 
                        "optional": [str],
                        "tags": ["silent", "reversed"],
                        "history": False},   

        "OBSTACLES" : { "description": "Shows a list of obstacles in current world.",
                        "command": "command_get_obstacles",
                        "history": False}      
        }


    def command_forward(self, steps:int):
        """
        Moves robot forward and displays appropriate messages.

        Args:
            steps (int): The distance the robot moves. Ignores negatives
        """
        self.world.move_robot(self.robot, abs(steps))
        self.world.get_position(self.robot)
        

    def command_back(self, steps:int):
        """
        Moves robot back and displays appropriate messages.

        Args:
            steps (int): The distance the robot moves. Ignores positives
        """
        self.world.move_robot(self.robot, -abs(steps))
        self.world.get_position(self.robot)


    def command_turn_right(self, degrees:float = 90):
        """
        Rotates robot 90° to the right
        and displays appropriate messages.

        Args:
            degrees (float): The amount the robot turns in degrees. 
            Defaults to 90.
        """
        self.world.rotate_robot(self.robot,abs(degrees))
        self.world.get_position(self.robot)


    def command_turn_left(self, degrees:float = 90):
        """
        Rotates robot 90° to the left
        and displays appropriate messages.

        Args:
            degrees (float): The amount the robot turns in degrees. 
            Defaults to -90.
        """
        self.world.rotate_robot(self.robot, -abs(degrees))
        self.world.get_position(self.robot)
        

    def command_sprint(self, steps:int):
        """
        Recursively moves the robot forward.

        Args:
            steps (int): The ditance the robot moves.
        """

        if  steps != 0:
            if self.world.move_robot(self.robot, steps):
                self.command_sprint(steps + (-1 if steps > 0 else 1))
        else:
            self.world.get_position(self.robot)


    def command_get_obstacles(self) -> None:
        """
        Prints a messages detailing all the objects in the current world.        
        """
        if len(self.world.get_obstacles()) > 0:
            self.robot.robot_say_message("There are some obstacles:")
            self.robot.robot_say_message(str(self.world.obstacles))


    def command_off(self):
        """
        Exits and displays appropriate message.
        """
        self.robot.robot_say_message(
            "Shutting down..",
            f"{self.robot.name}: "
        )
        raise SystemExit
        

    def command_help(self):
        """
        Robot displays a detailed list of all the commands available.
        """
        self.robot.robot_say_message("I can understand these commands:")
        for key, value in self.command_dict.items():
            spaces = "  " if key == "OFF" else " " if key == "HELP" else "\t"
            self.robot.robot_say_message(f"{key}{spaces}- {value['description']}")
        
    
    def replay_get_range(self, rng:str) -> range:
        """
        Error checks and converts the input into a range

        Args:
            rng (str): The user inputted string depicting range

        Returns:
            range: The range that is used to traverse a part of history.
        """
        command_arguments = rng.strip().split('-')

        history = list(
            filter(lambda command: command[0:2] == [self.world, self.robot], self.history))

        h_size = len(history)

        if  not all(map(lambda arg : arg.isdigit(), command_arguments)):
            self.robot.robot_say_message(
                # f"'{'-'.join(command_arguments)}' is not of type 'int'.",
                f"Sorry, I did not understand '{self.command_str}'.",
                f"{self.robot.name}: "
            )
            return False
        if  len(command_arguments) > 2:
            self.robot.robot_say_message(
                f"'{command_arguments}' has too many parts.",
                f"{self.robot.name}: "
            )            
            return False
        
        if len(command_arguments) == 2:
            start = h_size - int(command_arguments[0])
            stop = h_size - int(command_arguments[1])
        else:
            start = h_size - int(command_arguments[0])
            stop = h_size
        
        if  0 > start or start > stop or stop > h_size:
            self.robot.robot_say_message(
                f"'{command_arguments[0]}' and '{command_arguments[1]}'"+
                " need to be between {h_size} and 0,"+
                " and '{command_arguments[0]}'"+
                " needs to be the larger of the two.",
                f"{self.robot.name}: "
            )
            return False
    
        return range(start, stop)


    def command_replay(self, *args):
        """
        Replays all previous movement and rotation commands in a range.

        Args:
            tags(tuples[str,bool]): to set to silent and/or reversed
            
            range(str): a user input argument depicting
            the range to traverse history from.
        """
        options = {
            'silent'    : False,
            'reversed'  : False,
            'range'     : range(0, len(self.history))
        }

        history = list(
            filter(lambda command: command[0:2] == [self.world, self.robot], self.history))
        
        if len(args) > 0:
            if isinstance(args[0], str):
                rng = self.replay_get_range(args[0])
                if not rng:
                    return
                options['range'] = rng
                args = args[1:]

        if len(args)>0:
            options.update(args)

        if  options['silent']:
            self.robot.messages_enabled = False

        if  options['reversed']:
            history.reverse()
        
        for index in options['range']:
            command = history[index]
            self.exec_command(command[0], command[1], command[2:], '')
            self.history.pop()

        if  options['reversed']:
            history.reverse()
        self.robot.messages_enabled = True

        self.robot.robot_say_message(
            ''.join([
                "replayed",
                f" {len(list(options['range']))}",
                " commands",
                " in reverse" if options['reversed'] else '',
                " silently" if options['silent'] else '',
                '.'
            ]),
            f" > {self.robot.name} "
        )
        self.world.get_position(self.robot)


    def command_show_history(self):
        """
        Prints the history of current robot in current world.
        """
        if len(self.history) == 0:
            self.robot.robot_say_message(
                "No Commands in history.", f"{self.robot.name}: "
            )
        else:
            self.robot.robot_say_message(
                "Commands in history:", f"{self.robot.name}: "
            )
            for index ,command in enumerate(self.history):
                if command [0:2] == [self.world,self.robot] :
                    self.robot.robot_say_message(
                        f" {len(self.history) - index} > {' '.join(map(str,command[2:]))}"
                    )


    def add_to_history(self, command:list):
        """
        Adds the given command to history

        Args:
            command (list): the command to add to history
        """
        if  self.command_dict[command[0].upper()]["history"]:
            self.history.append([self.world, self.robot] + command)


    def exec_command(
        self, world:World, robot:ToyRobot, command:list, command_str:str
    ):
        """
        Executes a specific command available to the robot.

        Args:
            world (World): The world the current robot is in
            robot (ToyRobot): The robot that will do the command
            command (list): A command name, then args, then tags
            command_str (str): The raw input
        """
        self.world = world
        self.robot = robot
        self.command_str = command_str

        self.add_to_history(command)
        
        getattr(
            self,
            self.command_dict[command[0].upper()]["command"]
        )(*command[1:])

