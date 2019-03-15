#Alex Lewandowski
#Cat and Mice
#Environment Class

import arcade
import math
import random
from obstacle import Obstacle
from population import Population
from cat import Cat
from board import W
from board import H

class Environment:
    def __init__(self):
        self.population = Population()
        self.population.generate()
        self.population.bowChickaWowWow(0, 1, 4)
        self.cat = Cat()
        self.obstacles = [[Obstacle(float(int(W/15)), [float(int(W-(W/3))), float(int(H/4))])], [Obstacle(float(int(W/25)), [float(int(W/3)), float(int(H/3))])]]

    def draw(self):
        for obstacle in self.obstacles:
            obstacle[0].draw()
        self.cat.draw()
        for mouse in self.population.getMice():
            mouse.draw()
        #arcade.draw_circle_filled(715, 236, float(int(W/100)), arcade.color.PURPLE)
        #arcade.draw_circle_filled(617, 138, float(int(W/100)), arcade.color.PURPLE)

    def getObstacles(self):
        return self.obstacles

    def getCat(self):
        return self.cat

    def getStringBin(self, stringBin):
        num = 0
        for char in (0, len(stringBin)):
            num = num + (2**char)
        return num

    #Apply smell type and strength gene heuristics
    def adjustDistForSmell(self, distance, mouse):
        smellType = mouse.getSmellType()
        smellStrength = mouse.getSmellStrength()
        distance = distance - ((5 * distance * self.getStringBin(smellType)) / 100)
        return distance - ((distance * self.getStringBin(smellStrength)) / 10)


    def distance(self, object1Coords, object2Coords):
        a = abs(object1Coords[0]-object2Coords[0])
        b = abs(object1Coords[1]-object2Coords[1])
        return math.sqrt(a*a + b*b)
        
    def eatMouse(self, mouse):
        self.population.getMice().remove(mouse)

    # Heuristics that factor into move direction:
    # -needState: 1-3 go towards, 4 go away from
    # -preferenceForConfinedSpaces, increased probablility of taking confined route, if small enough to fit
    # -make short runs to safe zones
    # -when fleeing, only run to real safe zones
    # -if obstacle in the way of real safe zone, recaluclate to the route around it to closest real path  
    def move(self, catOrMouse, direction, speed):
        x  = "dummy"
        #catOrMouse.setCoords(catOrMouse.getCoords())

    #Mouse Move Utility Functions
    def getFleePath(self, mouse):
        #find the most direct route to the closest real safe zone
        return "dummy coord"


    def mapSafeZones(self, obstacle, cat):
        safeZone = []
        test = cat.getCoords() #######################
        test1 = obstacle.getCoords()[0]


        if ((cat.getCoords()[0] - obstacle.getCoords()[0])) == 0:
            m = .00000001
        else:
            m = (cat.getCoords()[1] - obstacle.getCoords()[1])/(cat.getCoords()[0] - obstacle.getCoords()[0])
        x = obstacle.getCoords()[0]
        y = obstacle.getCoords()[1]
        b = obstacle.getCoords()[1] - (m * x)

        #Handle undefined slopes
        if cat.getCoords()[1] > obstacle.getCoords()[1] and m == .00000001:
            vertY = int(obstacle.getCoords()[1] - obstacle.getRadius())
            for i in range (0, int(obstacle.getCoords()[1] - obstacle.getRadius())):
                if i%10 == 0:
                    vertY = vertY - 10
                    if vertY > H/20 and vertY < H and x < W - (W/5) - (H/20) and x > W/5:
                        safeZone.append([x,vertY])
        elif cat.getCoords()[1] < obstacle.getCoords()[1] and m == .00000001:
            vertY = int(obstacle.getCoords()[1] + obstacle.getRadius())
            for i in range (0, int(H - obstacle.getCoords()[1] + obstacle.getRadius())):
                if i%10 == 0:
                    vertY = vertY + 10
                    if vertY > H/20 and vertY < H and x < W - (W/5) - (H/20) and x > W/5:
                        safeZone.append([x,vertY])

        #Handle defined slopes
        else:
            for i in range (0, 100):
                y = ((m * x) + b) 
                if y > H/20 and y < H and x < W - (W/5) - (H/20) and x > W/5:
                    if self.getDistance([x,y], [obstacle.getCoords()[0], obstacle.getCoords()[1]]) > obstacle.getRadius():
                        safeZone.append([x,y])
                if cat.getCoords()[1] > obstacle.getCoords()[1]:
                    if m < 0:
                        x = x + 10
                    else:
                        x = x - 10
                else:
                    if m > 0:
                        x = x + 10
                    else:
                        x = x - 10
        return safeZone

    def getDistance(self, coord1, coord2):
        return math.sqrt((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2)

 #(int(W/5), int(W - W/5)): #only search in the cat room
    def findNearestSafeZone(self, mouse):
        return "dummy coord"

    def takeTunnel(self, mouse):
        if mouse.getSize().self.getStringBin() == 0:
            takeTun = random.choice([True, True, False])
            return takeTun
        else:
            return False

    #distance at which mouse will allow cat to get before fleeing affected by catFear
    def flee(self, mouse, cat):
        return "dummy coord"

    #Cat move utility function
    def targetMouse(self): #still needs to factor in smell type and strength and ignore out of sight mice
        target = [-1, 1000000]
        for mouse in self.population.getMice():
            distance = self.distance(self.cat.getCoords(), mouse.getCoords())
            distance = self.adjustDistForSmell(distance, mouse)
            if  distance < target[1]:
                target[0] = mouse
                target[1] = distance
        return target[0]