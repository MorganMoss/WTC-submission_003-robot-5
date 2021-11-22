import sys
from toy_robot.robot_toy import ToyRobot, CommandHandler, Commands

from world.text.world import World

if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'turtle':
        from world.turtle.world import TurtleWorld as World
    elif sys.argv[1].lower() == 'text':
        # from world.text.world import World
        ...


def robot_start() -> None:
    """This is the entry point for starting my robot"""

    commands = Commands()
    command_handler = CommandHandler(commands.command_dict)

    toy_robot = ToyRobot()
    toy_robot.start()
    
    world = World()
    world.add_robot(toy_robot.robot)
    world.generate_obstacles()
    
    commands.exec_command(world, toy_robot.robot, ["OBSTACLES"], '')

    while True:
        try:
            toy_robot.cmd(world, commands, command_handler)
        except SystemExit:
            break

if __name__ == "__main__":
    robot_start()
