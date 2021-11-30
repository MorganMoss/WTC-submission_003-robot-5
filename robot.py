import sys
import command_handling
from toy_robot.robot_toy import ToyRobot, CommandHandler, Commands
from world.text.world import World
from maze.empty_maze import Maze

sys.argv = list(map(lambda w : w.lower(), sys.argv))
if 'turtle' in sys.argv:
    from world.turtle.world import TurtleWorld as World

if "maze" in sys.argv:
    from maze.moss_maze import Maze

def robot_start() -> None:
    """This is the entry point for starting my robot"""   
    #Constants
    cell_size = 4
    num = list(filter(lambda arg: arg.isnumeric(), sys.argv))
    if len(num)>0:
        cell_size = int(num[0])
    scale = 1
    bounds_x = (-100*scale, 100*scale)
    bounds_y = (-200*scale, 200*scale)

    #Initializing a World and Robot
    world = World(Maze, bounds_x, bounds_y, cell_size)
    toy_robot = ToyRobot()
    toy_robot.start()
    world.add_robot(toy_robot.robot, (0,0))

    #Command Handling
    commands = Commands()
    commands.exec_command(world, toy_robot.robot, ["OBSTACLES"], '')
    command_handler = CommandHandler(commands.command_dict)
    while True:
        try:
            toy_robot.cmd(
                world, commands, 
                command_handler
            )
        except SystemExit:
            break

if __name__ == "__main__":
    robot_start()
