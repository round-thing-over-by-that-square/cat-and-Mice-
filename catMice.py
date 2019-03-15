#Alex Lewandowski
#An Othello Clone
#2/09/19
#CS405 Homework 1

import arcade
import time
import copy

from board import Board
from board import W
from board import H
from environment import Environment


##### CONSTANTS #####
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = int(WINDOW_WIDTH * 0.75)
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
        safeZone = self.environment.mapSafeZones(self.environment.getObstacles()[0][0], self.environment.getCat()) #debugging
        for coord in range (0, len(safeZone)):
            if coord%50 == 0:
                arcade.draw_circle_filled(safeZone[coord][0], safeZone[coord][1], float(int(W/300)), arcade.color.BLUE)
        safeZone1 = self.environment.mapSafeZones(self.environment.getObstacles()[1][0], self.environment.getCat()) #debugging
        for coord in range (0, len(safeZone1)):
            if coord%50 == 0:
                arcade.draw_circle_filled(safeZone1[coord][0], safeZone1[coord][1], float(int(W/300)), arcade.color.BLUE)

        
    
## end myGame class
    
def main():
   # f = open("data.txt", "w+")
    #f.write("") 
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)
   # environment = Environment()
    #target = environment.targetMouse()
   # environment.eatMouse(environment.population.getMice()[0]) #####testing eatMouse()
    #safeZone = environment.mapSafeZones(environment.getObstacles()[0], environment.getCat())
    arcade.run()
   
   

main()