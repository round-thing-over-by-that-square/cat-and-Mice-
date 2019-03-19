#Alex Lewandowski
#An Othello Clone
#2/09/19
#CS405 Homework 1

import cProfile
import re

import arcade
import time
import copy

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

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.LIGHT_GRAY) 
        self.board = Board() # an 8x8 board
        self.environment = Environment()
        
   
   
    def on_draw(self):
        arcade.start_render()
        self.board.draw()
        self.environment.draw()
        self.environment.setSafeZones(self.environment.getObstacles(), self.environment.getCat())
        
        safeCoords1 = self.environment.mapSafeZone(self.environment.getObstacles()[0][0], self.environment.getCat()) #debugging
        safeCoords2 = self.environment.mapSafeZone(self.environment.getObstacles()[1][0], self.environment.getCat()) #debugging
        
        #add blue safe zone dots for testing
        for i in range (0, len(safeCoords1)):
            arcade.draw_circle_filled(safeCoords1[i][0], safeCoords1[i][1], float(int(W/500)), arcade.color.BLUE)
        for i in range (0, len(safeCoords2)):
            arcade.draw_circle_filled(safeCoords2[i][0], safeCoords2[i][1], float(int(W/500)), arcade.color.BLUE)
        
        #move cat for testing
        if self.environment.cat.getCoords()[1] > H/40 + (W/50):
            self.environment.cat.move(0, -10)

        
    
## end myGame class
    
def main():
   # f = open("data.txt", "w+")
    #f.write("") 
    window = MyGame(W, H, TITLE)
    arcade.run()
   
   

main()