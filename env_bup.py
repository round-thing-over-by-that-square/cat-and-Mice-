#Alex Lewandowski
#Cat and Mice
#Environment Class

import arcade
import time
import math
import random
from random import uniform
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
        cheeseDoors = [[W/5, H-(H/40)], [W/5, (H/2) - (H/40)], [W/5, (H/10) - (H/20)]]
        targetDoor = [[-1,-1], 1000000]
        for door in cheeseDoors:
            dist = self.distance(mouse.getCoords(), door)
            if  dist < targetDoor[1]:
                targetDoor[0] = door
                targetDoor[1] = dist
        return targetDoor[0]

    def findNearestCheese(self, mouse):
        targetCheese = [[-1,-1], 100000]
        for cheese in self.cheeseBasket:
            dist = self.distance(cheese.getCoords(), mouse.getCoords())
            if dist < targetCheese[1]:
                targetCheese = [cheese, dist]
        return targetCheese[0].getCoords()

    def findNearestWater(self, mouse):
        targetWaterDish = [[-1, -1], 100000]
        for waterDish in self.waterPitcher:
            dist = self.distance(waterDish.getCoords(), mouse.getCoords())
            if dist < targetWaterDish[1]:
                targetWaterDish = [waterDish, dist]
        return targetWaterDish[0].getCoords()

    def findNearestWaterDoor(self, mouse):
        waterDoors = [[W - (W/5), H-(H/20)], [W - (W/5), (H/2)-(H/40)]]
        targetDoor = [[-1, -1], 1000000]
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
            # smallest mouse: never take
            if mouse.getSmallSpacePrefLevel() == "00" and mouse.getSize() == "00":
                mouse.setTakePassage(False)
            # smallest mouse: take 25% of time
            elif mouse.getSmallSpacePrefLevel() == "01" and mouse.getSize() == "00":
                mouse.setTakePassage(random.choice([True, False, False, False]))
            # smallest mouse: take 50% of time
            elif mouse.getSmallSpacePrefLevel() == "10" and mouse.getSize() == "00":
                mouse.setTakePassage(random.choice([True, False]))
            # smallest mouse: take 75% of time
            elif mouse.getSmallSpacePrefLevel() == "11" and mouse.getSize() == "00":
                mouse.setTakePassage(random.choice([True, True, True, False]))
            
            # second-smallest mouse: never take
            elif mouse.getSmallSpacePrefLevel() == "01" and mouse.getSize() == "01":
                mouse.setTakePassage(False)
            # second-smallest mouse: take 16.6% of the time
            elif mouse.getSmallSpacePrefLevel() == "10" and mouse.getSize() == "01":
                mouse.setTakePassage(random.choice([True, False, False, False, False, False]))
            # second-smallest mouse: take 25% of the time
            elif mouse.getSmallSpacePrefLevel() == "11" and mouse.getSize() == "01":
                mouse.setTakePassage(random.choice([True, False, False, False]))
            # second-smallest mouse: take 40% of the time
            elif mouse.getSmallSpacePrefLevel() == "11" and mouse.getSize() == "01":
                mouse.setTakePassage(random.choice([True, True, False, False, False,]))
            else:
                mouse.setTakePassage(False)
        else:
            mouse.setTakePassage(False)

    def wander(self, mouse, speed):
        if (self.isInsideCheeseRoom(mouse) and mouse.getWanderDestination() == [-1, -1]):# or self.distance(mouse.getWanderDestination(), mouse.getCoords()) < H/80:
            destination = [uniform(W/10, (W/5)-(H/80)), uniform(0, H)]
            mouse.setWanderDestination(destination)
            self.move(destination, mouse, speed)
        elif (self.isInsideWaterRoom(mouse) and mouse.getWanderDestination() == [-1, -1]):# or self.distance(mouse.getWanderDestination(), mouse.getCoords()) < H/80:
            destination1 = [uniform(W-W/10, W-W/5+(H/80)), uniform(0, H)]
            mouse.setWanderDestination(destination1)
            self.move(destination1, mouse, speed)
        elif mouse.getWanderDestination() != [-1, -1]:
            if self.distance(mouse.getWanderDestination(), mouse.getCoords()) > H/80:
                self.move(mouse.getWanderDestination(), mouse, speed)
            else:
                mouse.setWanderDestination([-1, -1])


            
    ################################################################################################################################
    ################################################################################################################################
    # Heuristics that factor into move direction:
    # -needState: 1-3 go towards, 4 go away from
    # -preferenceForConfinedSpaces, increased probablility of taking confined route, if small enough to fit
    # -make short runs to safe zones
    # -when fleeing, only run to real safe zones
    # -if obstacle in the way of real safe zone, recaluclate to the route around it to closest real path  
    def mouseMove(self, mouse):

        # Apply speed gene gene  
        if mouse.getSpeed() == "00":
            speed = .5
        if mouse.getSpeed() == "01":
            speed = 1
        if mouse.getSpeed() == "10":
            speed = 2
        if mouse.getSpeed() == "11":
            speed = 5

        # Apply catFear gene
        if mouse.getCatFear() == "00":
            fearDistance = H/30
        if mouse.getCatFear() == "01":
            fearDistance = H/20
        if mouse.getCatFear() == "10":
            fearDistance = H/10
        if mouse.getCatFear() == "11":
            fearDistance = H/5

        #Trigger flee state if the cat is within mouse's fear distance
        if self.distance(mouse.getCoords(), self.cat.getCoords()) < fearDistance:
            if mouse.getCoords()[0] > W/5 and mouse.getCoords()[1] > H/40 and mouse.getCoords()[0] < W-(W/5)-(H/39):
                mouse.setNeedState(4)
            elif mouse.getCoords()[0] > W-(W/5)-(H/30) and mouse.getCoords()[1] > (H/2) + (H/40) and mouse.getCoords()[0] < W-(W/5):
                mouse.setNeedState(4)

        #if need state = Eat   
        if mouse.getNeedState() == 1:
            goNorth = [mouse.getCoords()[0], (H/2)]
            if time.clock() - mouse.getStateClock() > 35:
                self.population.killMouse(mouse) #dies of starvation
            cheeseDoorCoord = self.findNearestCheeseDoor(mouse)
            waterDoorCoord = self.findNearestWaterDoor(mouse)
            if not self.isInsideWaterRoom(mouse):
                if mouse.getTakePassage() == -1:
                    self.ponderPassage(mouse)
                if self.isInsideWaterRoom(mouse) and mouse.getCoords()[1] < H/3:
                    mouse.setWanderDestination(goNorth)
                    self.move(mouse.getWanderDestination(), mouse, speed)
                    
                elif self.isInsideWaterRoom(mouse) and mouse.getTakePassage() == True:
                    mouse.setNeedState(6)
                elif self.isInsideWaterRoom(mouse) and mouse.getTakePassage() == False:
                    self.move([waterDoorCoord[0] - (H/150), waterDoorCoord[1]], mouse, speed)##############
                else:
                    self.move([cheeseDoorCoord[0] -(H/80), cheeseDoorCoord[1]], mouse, speed)
           # elif self.distance(mouse.getCoords(), [W-(W/5)-(H/40), (H/2)-(H/10)]) < H/80:

            else:
                cheeseCoord = self.findNearestCheese(mouse)
                if self.distance(mouse.getCoords(), cheeseCoord) > H/40:
                    mouse.setWanderDestination([-1, -1])
                    self.move(cheeseCoord, mouse, speed)
                else:
                    mouse.setStateClock(time.clock())
                    self.ponderPassage(mouse)
                    mouse.setNeedState(5)
                

        #if need state = Drink
        elif mouse.getNeedState() == 2:
            if time.clock() - mouse.getStateClock() > 35: 
                self.population.killMouse(mouse) #dies of thirst 
            if not self.isInsideWaterRoom(mouse):
                if mouse.getTakePassage() == -1:
                    self.ponderPassage(mouse)
                cheeseDoorCoord = self.findNearestCheeseDoor(mouse)
                waterDoorCoord = self.findNearestWaterDoor(mouse)
                if self.isInsideCheeseRoom(mouse) and mouse.getTakePassage() == True:
                    mouse.setNeedState(6)
                elif self.isInsideCheeseRoom(mouse) and mouse.getTakePassage() == False:
                    self.move([cheeseDoorCoord[0] + (H/80), cheeseDoorCoord[1]], mouse, speed)
                else:
                    self.move([waterDoorCoord[0] + (H/80), waterDoorCoord[1]], mouse, speed)
            else:
                waterCoord = self.findNearestWater(mouse)
                if self.distance(mouse.getCoords(), waterCoord) > H/40:
                    mouse.setWanderDestination([-1, -1])
                    self.move(waterCoord, mouse, speed)
                else:
                    mouse.setStateClock(time.clock())
                    self.ponderPassage(mouse)
                    mouse.setNeedState(5)

    

        #if need state = Reproduce    
        elif mouse.getNeedState() == 3:
            
            potentialMate = [mouse, 10000000]
            for m in self.population.getMice():
                d = self.distance(mouse.getCoords(), m.getCoords())
                if d < potentialMate[1]: # and potentialMate[0].getNeedState() == 3:
                    potentialMate[0] = m
                    potentialMate[1] = d
            if self.distance(mouse.getCoords(), [potentialMate[0].getCoords()[0], potentialMate[0].getCoords()[1]]) < H/120:
                self.population.reproduce(self.population.getIndex(mouse), self.population.getIndex(potentialMate[0]), random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13]))
                potentialMate[0].setNeedState(1)
                mouse.setNeedState(2)
                
            else:
                self.move(potentialMate[0].getCoords(), mouse, speed)
        
        #if need state = flee
        elif mouse.getNeedState() == 4:
            safeCoord = self.getFleeCoord(mouse)
            self.move(safeCoord, mouse, speed)
            mouse.setStateClock(time.clock() + 25)
            if self.distance(mouse.getCoords(), safeCoord) < H/80:
                mouse.setNeedState(5)

        #if need state = wander
        elif mouse.getNeedState() == 5:
            if time.clock() - mouse.getStateClock() > 30: 
                mouse.setStateClock(time.clock())
                if self.isInsideCheeseRoom(mouse):
                    mouse.setNeedState(2)
                else:
                    mouse.setNeedState(1)
            else:
                self.wander(mouse, speed)

        #if taking passage
        elif mouse.getNeedState() == 6:
            coords = mouse.getCoords()
            passageEntranceWater = [W-(W/5)-(H/60), (W/2 + H/40)]
            passageEntranceCheese = [W/5, H/40]
            passageCornerToCheese = [W-(W/5)-(H/60), H/40]
            passageCornerToWater = passageCornerToCheese
            
            # Heading for Cheese
            if coords[0] > W-(W/5)-(H/60):
                mouse.setWanderDestination(passageEntranceWater)
            elif self.distance(coords, passageEntranceWater) < H/80 and mouse.getWanderDestination() == passageEntranceWater:
                mouse.setWanderDestination(passageCornerToCheese)

            # Heading for Water
            elif coords[0] < (W/5):
                mouse.setWanderDestination(passageEntranceCheese)
            elif self.distance(mouse.getCoords(), passageEntranceCheese) < H/80 and mouse.getWanderDestination() == passageEntranceCheese:
                mouse.setWanderDestination(passageCornerToWater)

            self.move(mouse.getWanderDestination(), mouse, speed)


    #################################################################################################################################
    #################################################################################################################################         

    #Mouse Move Utility Functions
    def getFleeCoord(self, mouse):
        fleecoords = [[float(int(W/5)-(H/40)), float(int(H - H/40))], [float(int(W/5)-(H/40)), float(int(H - (H/2) - (H/40)))], [float(int((W - (W/5))+(H/40))), (float(int(H - H/40)))], [float(int(W - (W/5)+(H/40))), float(int(H - (H/2) - (H/40)))]]
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