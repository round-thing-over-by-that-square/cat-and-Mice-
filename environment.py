#Alex Lewandowski
#Cat and Mice
#Environment Class

import math
from population import Population
from cat import Cat


class Environment:
    def __init__(self):
        self.population = Population()
        self.population.generate()
        self.population.bowChickaWowWow(0, 1, 4)
        self.cat = Cat()


    def targetMouse(self): #still needs to factor in smell type and strength and ignore out of sight mice
        target = [-1, 1000000]
        for mouse in self.population.getMice():
            distance = self.distance(self.cat.getCoords(), mouse.getCoords())
            distance = self.adjustDistForSmell(distance, mouse)
            if  distance < target[1]:
                target[0] = mouse
                target[1] = distance
        return target[0]

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

    def getFleePath(self, mouse, cat):
        #find the most direct route to the closest real safe zone
        return "dummy coord"

    def findNearestSafeZone(self, mouse):
        return "dummy coord"

    def takeTunnel(self, mouse):
        return "dummy bool"

    def flee(self, mouse, cat):
        return "dummy coord"

