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

    #called by mapSafeCoords()
    #returns the coords for the edge of the cylindrical obsticle's walls from the perpective of the cat. 
    #Lines extended from the cat to each coord act as bounds, inside of which, behind the obstical, exists a safe area, hidden from the cat's view.
    def getSafeZoneCoords(self, obstacle, cat):
        #slope of line between cat and obstical
        m1 = (cat.getCoords()[1] - obstacle.getCoords()[1])/(cat.getCoords()[0] - obstacle.getCoords()[0])
        #slope of line perpenticular to line between cat and obstical
        m2 = -1 / m1
        #Calculate x and y coords 
        coord1 = [obstacle.getCoords()[0] + (int(obstacle.getRadius() * math.cos(math.atan(m2)))), obstacle.getCoords()[1] + (int(obstacle.getRadius() * math.cos(math.atan(m2))))]
        coord2 = [obstacle.getCoords()[0] + (int(obstacle.getRadius() * -1 * math.cos(math.atan(m2)))), obstacle.getCoords()[1] + (int(obstacle.getRadius() * -1 * math.cos(math.atan(m2))))]
       
        arcade.draw_circle_filled(coord1[0], coord1[1], float(int(W/100)), arcade.color.PURPLE)############
        arcade.draw_circle_filled(coord2[0], coord2[1], float(int(W/100)), arcade.color.PURPLE)###########
        return [coord1, coord2]
    
    def getMinOrMaxXandY(self, obstacle, cat, coords):
        minX = -1
        maxX = -1
        minY = -1
        maxY = -1
        cenX = -1
        cenX = -1

        if cat.getCoords()[1] >= obstacle.getCoords()[1] + obstacle.getRadius(): 
            maxY = max(coords[0][1], coords[1][1])
        elif cat.getCoords()[1] < obstacle.getCoords()[1] + obstacle.getRadius(): 
            minY = min(coords[0][1], coords[1][1])

        if cat.getCoords()[0] >= obstacle.getCoords()[0] + obstacle.getRadius(): 
            maxX = max(coords[0][0], coords[1][0])
        elif cat.getCoords()[0] < obstacle.getCoords()[0] + obstacle.getRadius(): 
            minX = min(coords[0][0], coords[1][0]) 

        if cat.getCoords()[1] > obstacle.getCoords()[1] - obstacle.getRadius() and cat.getCoords()[1] > obstacle.getCoords()[1] + obstacle.getRadius():
            cenY = 0
        if cat.getCoords()[0] > obstacle.getCoords()[0] - obstacle.getRadius() and cat.getCoords()[0] > obstacle.getCoords()[0] + obstacle.getRadius():
             cenX = 0
        
        coords = [[-1, -1],[-1, -1]]
        if minX != -1:
            coords[0] = ["minX", minX]
        elif maxX != -1:
            coords[0] = ["maxX", maxX]
        elif cenX != -1:
            coords[0] = ["cenX", -1]
        if minY != -1:
            coords[1] = ["minY", minY]
        elif maxY != -1:
            coords[1] = ["maxY", maxY]
        elif cenY != -1:
            coords[1] = ["cenY", -1]
        return coords

    #takes the pre-filtered coordinate bounds and returns list filled with coords of safe zone
    def fillSafeZoneMap(self, cat, coords, xStart, xEnd, yStart, yEnd):
        safeZone = []
        for x in range (int(xStart), int(xEnd)):
            for y in range (int(yStart), int(yEnd)):
                #if the line between the current coord and the cat lies between the lines formed by the cat and object sides
                coor = cat.getCoords()[0]
                if (cat.getCoords()[0] - x) == 0 or (cat.getCoords()[0] - coords[1][0]) == 0  or (cat.getCoords()[0] - coords[0][0]) == 0:
                    coor = coor+1

         #       slopeCatToCurLoc = (cat.getCoords()[1] - y) / (coor - x) ################################################
          #      slopeCatObs1 = (cat.getCoords()[1] - coords[0][1]) / (cat.getCoords()[0] - coords[0][0]) #####################
           #     slopeCatObs2 = (cat.getCoords()[1] - coords[1][1]) / (cat.getCoords()[0] - coords[1][0])  #####################
                
                if ((((cat.getCoords()[1] - y) / (coor - x) > (cat.getCoords()[1] - coords[0][1]) / (cat.getCoords()[0] - coords[0][0])) and
                ((cat.getCoords()[1] - y) / (coor - x) < (cat.getCoords()[1] - coords[1][1]) / (cat.getCoords()[0] - coords[1][0]))) or
                (((cat.getCoords()[1] - y) / (coor - x) < (cat.getCoords()[1] - coords[0][1]) / (cat.getCoords()[0] - coords[0][0])) and
                ((cat.getCoords()[1] - y) / (coor - x) > (cat.getCoords()[1] - coords[1][1]) / (cat.getCoords()[0] - coords[1][0])))):
                    safeZone.append([x, y])
        return safeZone

    def mapSafeZones(self, obstacle, cat):
        coords = self.getSafeZoneCoords(obstacle, cat)
        extremes = self.getMinOrMaxXandY(obstacle, cat, coords)
        
        if extremes[0][0] == "minX":
            minX = extremes[0][1]
        else:
            maxX = extremes[0][1]
        if extremes[1][0] == "minY":
            minY = extremes[1][1]
        else:
            maxY = extremes[1][1]

        # Optimization prunes coordinate set to portion of room in which safe-zone will reside, prior to calculating
        # if each coordinate lies between bounds of lines created by obstacle sides and cat 
        if extremes[0][0] == "minX" and extremes[1][0] == "minY":
            return self.fillSafeZoneMap(cat, coords, minX, float(int(W - W/5)), minY, H)
        elif extremes[0][0] == "minX" and extremes[1][0] == "maxY":
            return self.fillSafeZoneMap(cat, coords, minX, float(int(W - W/5)), 0, maxY)
        elif extremes[0][0] == "maxX" and extremes[1][0] == "minY":
            return self.fillSafeZoneMap(cat, coords, float(int(W/5)), maxX, minY, H) 
        elif extremes[0][0] == "maxX" and extremes[1][0] == "maxY":      
            return self.fillSafeZoneMap(cat, coords, float(int(W/5)), maxX, 0, maxY) 
        elif extremes[0][0] == "cenX" and extremes[1][0] == "minY":
            return self.fillSafeZoneMap(cat, coords, float(int(W/5)), float(int(W - W/5)), minY, H)
        elif extremes[0][0] == "cenX" and extremes[1][0] == "maxY":
            return self.fillSafeZoneMap(cat, coords, float(int(W/5)), float(int(W - W/5)), 0, maxY)
        elif extremes[0][0] == "maxX" and extremes[1][0] == "cenY":
            return self.fillSafeZoneMap(cat, coords, float(int(W/5)), maxX, 0, H)
        elif extremes[0][0] == "maxX" and extremes[1][0] == "cenY":
            return self.fillSafeZoneMap(cat, coords, float(int(W/5)), maxX, 0, H)     
        else:
            return "error"      



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