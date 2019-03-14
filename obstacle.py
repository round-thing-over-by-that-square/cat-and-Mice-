#Alex Lewandowski   
#Obstacle Class

import arcade

class Obstacle:
    def __init__(self, radius, centerCoords):
        self.radius = radius
        self.centerCoords = centerCoords

    def getCoords(self):
        return self.centerCoords

    def getRadius(self):
        return self.radius
    
    def draw(self):
        arcade.draw_circle_filled(self.centerCoords[0], self.centerCoords[1], self.radius, arcade.color.BLACK)  