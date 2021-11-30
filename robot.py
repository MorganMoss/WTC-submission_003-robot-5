import sys
import importlib
import os

from command_handling.command_handling import CommandHandler
from command_handling.commands import Commands
from toy_robot import ToyRobot

if "--list" in sys.argv:
    mazes = os.listdir("./maze")
    mazes = filter(lambda word : "maze" in word, mazes)
    mazes = map(lambda word : word.replace(".py", ''), mazes)
    print(*mazes, sep="\n")
    raise SystemExit

if "--help" in sys.argv:
    print(
""" Add the following arguments to change how this program works:
    --help    : Shows how to add arguments to robot.py
    --list    : Lists the Mazes inside the maze directory you can use
    <Integer> : To adjust the size of obstacles
    *maze*    : A word containing 'maze' - Trys to import custom maze with this filename
    turtle    : Program now uses turtle graphics instead of text"""
    )
    raise SystemExit

sys.argv = list(map(lambda w : w.lower(), sys.argv))
if 'turtle' in sys.argv:
    from world.turtle.world import TurtleWorld as World
else:
    from world.text.world import World

for arg in sys.argv:
    if "maze" in arg:
        try:
            Maze = getattr(importlib.import_module("."+arg, "maze"), "Maze")
            break
        except:
            ...
    from maze.empty_maze import Maze

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

    world.add_robot(toy_robot, (0,0))

    #Command Handling
    commands = Commands()
    commands.exec_command(world, toy_robot, ["OBSTACLES"], '')
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
