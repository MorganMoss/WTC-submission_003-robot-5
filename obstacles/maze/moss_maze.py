from obstacles.obstacles import *
import random

class Maze():
    
    def __init__(self) -> None:
        """
        Constructor for my Maze
        """
        self.maze = Obstacles()


    def get_maze(self) -> Obstacles():
        return self.maze


    def create_random_maze():
        # use intervals of 4 in either direction,
        # start at a grid pos | pos%4 == 0
        ...

    def get_custom_maze(textfile_path:str):
        file_object  = open("filename", "mode")
