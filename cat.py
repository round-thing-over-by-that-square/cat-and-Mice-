#Alex Lewandowski
#Cat and Mice
#Cat Class
import arcade
import random
import time
from board import W
from board import H

class Cat:

    def __init__(self):
        self.age = 0
        self.time = 0
        self.coords = [float(int(W/2)), float(int(H - H/5))]
        self.target = 0

    def getCoords(self):
        return self.coords

    def setCoords(self, coords):
        self.coords = coords

    def setTarget(self, mouse):
        self.target = mouse

    def getTarget(self):
        return self.target

    def draw(self):
        arcade.draw_circle_filled(self.coords[0], self.coords[1], float(int(W/50)), arcade.color.RED_DEVIL)
    
    def move(self, xDist, yDist):
        self.coords[0] = self.coords[0] + xDist
        self.coords[1] = self.coords[1] + yDist

     