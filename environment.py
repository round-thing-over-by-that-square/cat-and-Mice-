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
from needs import Need
import copy

class Environment(arcade.Sprite):
    def __init__(self):
        self.population = Population()
        self.population.generate()
        self.population.bowChickaWowWow(0, 1, 4)
        self.cat = Cat()
        self.obstacles = [[Obstacle(float(int(W/15)), [float(int(W-(W/3))), float(int(H/4))])], [Obstacle(float(int(W/25)), [float(int(W/3)), float(int(H/3))])]]
        self.allSafeZones = 0
        cheeseSprite = arcade.Sprite("images/cheese.png", 1)
        waterSprite = arcade.Sprite("images/water.png", 1)
        self.cheeseList = arcade.SpriteList()  
        self.waterList = arcade.SpriteList()     
        self.cheeseBasket = [Need('E', [W/20, H/5], copy.deepcopy(cheeseSprite)), Need('E', [W/20, 2*H/5], copy.deepcopy(cheeseSprite)), Need('E', [W/20, 3*H/5], copy.deepcopy(cheeseSprite)), Need('E', [W/20, 4*H/5], copy.deepcopy(cheeseSprite))]
        self.waterPitcher = [Need('D', [W-(W/20), H/5], copy.deepcopy(waterSprite)), Need('D', [W-(W/20), 2*H/5], copy.deepcopy(waterSprite)), Need('D', [W-(W/20), 3*H/5], copy.deepcopy(waterSprite)), Need('D', [W-(W/20), 4*H/5], copy.deepcopy(waterSprite))]
        for cheese in self.cheeseBasket:
            self.cheeseList.append(cheese.getSprite())
        for waterBowl in self.waterPitcher:
            self.waterList.append(waterBowl.getSprite())
    
    def draw(self):
        for obstacle in self.obstacles:
            obstacle[0].draw()
        self.waterList.draw()
        self.cheeseList.draw()
        for mouse in self.population.getMice():
            self.mouseMove(mouse) ###################################
            mouse.draw()
        self.cat.draw()

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

    def catMove(self):
        x = "dummy"

    #moves mouse or cat towards current need by a distance related to it s speed 
    def move(self, coord, mouseOrCat, speed):
        #prevent divide by zero
        deltaX = (coord[0]-mouseOrCat.getCoords()[0])
        if deltaX == 0:
            deltaX = 0.00000000001

        #m = (coord[1]-mouseOrCat.getCoords()[1]) / deltaX
        d = 1 * speed

        if self.distance(mouseOrCat.getCoords(), coord) <= d:
            #move to need coords
            mouseOrCat.setCoords([coord[0], coord[1]])
        midCoord = [coord[0], coord[1]]
        while self.distance(midCoord, mouseOrCat.getCoords()) >= d + 1.5:
            x = (mouseOrCat.getCoords()[0] + midCoord[0]) / 2
            y = (mouseOrCat.getCoords()[1] + midCoord[1]) / 2
            midCoord = [x, y]
        mouseOrCat.setCoords(midCoord)
        

    def findNearestCheeseDoor(self, mouse):
        cheeseDoors = [[W/5, H-(H/40)], [W/5, H - (H/2) - (H/40)], [W/5, H/40]]
        targetDoor = [-1, 1000000]
        for door in cheeseDoors:
            dist = self.distance(mouse.getCoords(), door)
            if  dist < targetDoor[1]:
                targetDoor[0] = door
                targetDoor[1] = dist
        return targetDoor[0]

    def findNearestCheese(self, mouse):
        targetCheese = [-1, 100000]
        for cheese in self.cheeseBasket:
            dist = self.distance(cheese.getCoords(), mouse.getCoords())
            if dist < targetCheese[1]:
                targetCheese = [cheese, dist]
        return targetCheese[0].getCoords()

    def findNearestWaterDoor(self, mouse):
        waterDoors = [[W - (W/5), H-(H/40)], [W - (W/5), H - (H/2) - (H/40)]]
        targetDoor = [-1, 1000000]
        for door in waterDoors:
            dist = self.distance(mouse.getCoords(), door)
            if  dist < targetDoor[1]:
                targetDoor[0] = door
                targetDoor[1] = dist
        return targetDoor[0]

    def isInsideWaterRoom(self, mouse):
        if mouse.getCoords()[0] > W - (W/5):
            return True
        else:
            return False

    def isInsideCheeseRoom(self, mouse):
        if mouse.getCoords()[0] < W/5:
            return True
        else:
            return False

    

    def ponderPassage(self, mouse):
        if self.isInsideWaterRoom(mouse) or self.isInsideCheeseRoom(mouse):
            if mouse.getSmallSpacePrefLevel() == "00" and mouse.getSize() == "00":
                mouse.setTakePassage(random.choice([True, False, False, False]))
            elif mouse.getSmallSpacePrefLevel() == "01" and mouse.getSize() == "00":
                mouse.setTakePassage(random.choice([True, True, False, False]))
            elif mouse.getSmallSpacePrefLevel() == "10" and mouse.getSize() == "00":
                mouse.setTakePassage(random.choice([True, True, True, False]))
            elif mouse.getSmallSpacePrefLevel() == "11" and mouse.getSize() == "00":
                mouse.setTakePassage(random.choice([True, True, True, True]))
            else:
                mouse.setTakePassage(False)
        else:
            mouse.setTakePassage(False)


    # Heuristics that factor into move direction:
    # -needState: 1-3 go towards, 4 go away from
    # -preferenceForConfinedSpaces, increased probablility of taking confined route, if small enough to fit
    # -make short runs to safe zones
    # -when fleeing, only run to real safe zones
    # -if obstacle in the way of real safe zone, recaluclate to the route around it to closest real path  
    def mouseMove(self, mouse):
        if mouse.getSpeed() == "00":
            speed = 2
        if mouse.getSpeed() == "01":
            speed = 4
        if mouse.getSpeed() == "10":
            speed = 6
        if mouse.getSpeed() == "11":
            speed = 8

        
        #if need state = Eat   
        if mouse.getNeedState() == 1:
            if not self.isInsideCheeseRoom(mouse):
                #ponder taking the passage (if mouse is small enough)
                self.ponderPassage(mouse)
                cheeseDoorCoord = self.findNearestCheeseDoor(mouse)
                if self.isInsideWaterRoom(mouse) and mouse.getTakePassage() == True:
                    self.move([W/5, H/40], mouse, speed)
                elif self.isInsideWaterRoom(mouse) and mouse.getTakePassage() == False:
                    waterDoorCoord = self.findNearestWaterDoor(mouse)
                    self.move([waterDoorCoord[0] - (H/80), waterDoorCoord[1]], mouse, speed)
                elif self.distance(cheeseDoorCoord, mouse.getCoords()) < H/80:
                    cheeseCoord = self.findNearestCheese(mouse)
                    self.move(cheeseCoord, mouse, speed)
                else:
                    self.move(cheeseDoorCoord, mouse, speed)
                
                
        #if need state = Drink
        elif mouse.getNeedState() == 2:
            if not self.isInsideWaterRoom(mouse):
                self.ponderPassage(mouse)
                if self.isInsideCheeseRoom(mouse) and mouse.getTakePassage() == True:
                    self.move([W-(W/5)-(H/40), (W/2 + H/40)], mouse, speed)
                else:
                    coord = self.findNearestWaterDoor(mouse)
                    self.move(coord, mouse, speed)
    

        #if need state = Reproduce    
        elif mouse.getNeedState() == 3:
            potentialMate = [mouse, 10000000]
            for m in self.population.getMice():
                d = self.distance(mouse.getCoords(), m.getCoords())
                if d < potentialMate[1]:
                    potentialMate[0] = m
                    potentialMate[1] = d
            self.move(potentialMate[0].getCoords(), mouse, speed)
        
        #if need state = flee
        elif mouse.getNeedState() == 4:
            coord = self.getFleeCoord(mouse)
            self.move(coord, mouse, speed)

            

    #Mouse Move Utility Functions
    def getFleeCoord(self, mouse):
        fleecoords = [[float(int(W/5)), float(int(H - H/40))], [float(int(W/5)), float(int(H - (H/2) - (H/40)))], [float(int((W - (W/5)))), (float(int(H - H/40)))], [float(int(W - (W/5))), float(int(H - (H/2) - (H/40)))]]
        minDist = [0, 1000000]
        for coord in fleecoords:
            d = self.distance(mouse.getCoords(), coord)
            if d < minDist[1]:
                minDist[0] = coord
                minDist[1] = d
        return minDist[0]

    def setSafeZones(self, obstacles, cat):
        allSafeCoords = []
        for obstacle in obstacles:
            safeCoords = self.mapSafeZone(obstacle[0], cat)
            for coord in safeCoords:
                allSafeCoords.append(coord)
        self.allSafeZones = allSafeCoords

    def mapSafeZone(self, obstacle, cat):
        safeZone = []
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
                    if vertY > H/40 and vertY < H and x < W - (W/5) - (H/40) and x > W/5:
                        safeZone.append([x,vertY])
        elif cat.getCoords()[1] < obstacle.getCoords()[1] and m == .00000001:
            vertY = int(obstacle.getCoords()[1] + obstacle.getRadius())
            for i in range (0, int(H - obstacle.getCoords()[1] + obstacle.getRadius())):
                if i%10 == 0:
                    vertY = vertY + 10
                    if vertY > H/40 and vertY < H and x < W - (W/5) - (H/40) and x > W/5:
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

    #return distance between two coords
    def getDistance(self, coord1, coord2):
        return math.sqrt((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2)

    #(int(W/5), int(W - W/5)): #only search in the cat room
    def findNearestSafeZone(self, mouse):
        minCoord = [[-1, -1], 10000000]
        for coord in self.allSafeZones:
            d = self.distance(mouse.getCoords(), coord)
            if  d < minCoord[1]:
                minCoord = [coord, d]
        return minCoord[0]

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