import sys
import importlib
import os
from command_handling.command_handling import CommandHandler
from command_handling.commands import Commands
from toy_robot import ToyRobot

sys.argv = list(map(lambda w : w.lower(), sys.argv))
if 'turtle' in sys.argv:
    from world.turtle.world import TurtleWorld as World
else:
    from world.text.world import World

for arg in sys.argv:
    if "maze" in arg.lower() in arg.lower():
        try:
            Maze = importlib.import_module("."+arg, "maze")
            break
        except Exception as e:
            print(f"Import Failed! {e}")
            # print(e)
            raise SystemExit
    import maze.empty_maze as Maze

# import maze.moss_maze as Maze

def robot_start() -> None:
    """This is the entry point for starting my robot"""   
    
    #Constants
    cell_size = 4
    # num = list(filter(lambda arg: arg.isnumeric(), sys.argv))
    for arg in sys.argv:
        try:
            num = float(arg)
            break
        except ValueError:
            num = 0

    scale = 1
    if num > 2:
        cell_size = int(num) 
    elif num > 0:
        cell_size = 2
        scale = int(1/num*2)

    x_size =100
    y_size =196
    bounds_x = (-x_size*scale, x_size*scale)
    bounds_y = (-y_size*scale, y_size*scale)
    
    if cell_size != 4:
        Maze.Maze(bounds_x,bounds_y,cell_size)

    #Initializing a World and Robot
    world = World(Maze, bounds_x, bounds_y, cell_size)
    toy_robot = ToyRobot()
    toy_robot.start()
    world.add_robot(toy_robot, (0,0))
    

    for arg in sys.argv:
        if "maze" in arg:
            break
        arg = "obstacles"
    toy_robot.robot_say_message(
        f"Loaded {arg}.",
        f"{toy_robot.name}: ")

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

    if "--list" in sys.argv:
        mazes = os.listdir("./maze")
        mazes = filter(lambda word : "maze" in word and ".py" in word, mazes )
        mazes = map(lambda word : word.replace(".py", ''), mazes)
        print(*mazes, sep="\n")
        raise SystemExit


    if "--help" in sys.argv:
        print(
    """ Add the following arguments to change how this program works:
        --help    : Shows how to add arguments to robot.py
        --list    : Lists the Mazes inside the maze directory you can use
        <Integer> : To adjust the size of obstacles
        <maze>    : A word containing 'maze' - Trys to import custom maze with this filename
        turtle    : Program now uses turtle graphics instead of text"""
        )
        raise SystemExit

    robot_start()
