

import cProfile
import re

import arcade
import time
import copy
import random

from board import Board
from board import W
from board import H
from environment import Environment


##### CONSTANTS #####
#WINDOW_WIDTH = 1000
#WINDOW_HEIGHT = int(WINDOW_WIDTH * 0.75)
TITLE = "Cat and Mice"  

####################
##  MyGame Class  ##
####################
class MyGame(arcade.Window):
    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        self.set_mouse_visible(False) 

        arcade.set_background_color(arcade.color.BLACK)  
        self.board = Board() 
        self.environment = Environment()
        self.drawCount = 0
   
   
    def on_draw(self):
        arcade.start_render()
        if self.drawCount == 120:
            random.shuffle(self.environment.population.mice) #shuffle order of mice to prevent too much in-breeding
            self.drawCount = 0
        else:
            self.drawCount = self.drawCount + 1
        self.board.draw()
        self.environment.draw()
        self.environment.setSafeZones(self.environment.getObstacles(), self.environment.getCat())
        
        safeCoords1 = self.environment.mapSafeZone(self.environment.getObstacles()[0], self.environment.getCat()) #debugging
        safeCoords2 = self.environment.mapSafeZone(self.environment.getObstacles()[1], self.environment.getCat()) #debugging
       
        #add blue safe zone dots for testing
        for i in range (0, len(safeCoords1)):
            arcade.draw_circle_filled(safeCoords1[i][0], safeCoords1[i][1], float(int(W/500)), arcade.color.BLUE)
        for i in range (0, len(safeCoords2)):
            arcade.draw_circle_filled(safeCoords2[i][0], safeCoords2[i][1], float(int(W/500)), arcade.color.BLUE)
        
       
    
## end myGame class
    
def main():
   # f = open("data.txt", "w+")
    #f.write("") 
   
    
    window = MyGame(W, H, TITLE)
    arcade.run()
   
   

main()