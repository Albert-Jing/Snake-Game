from graphics import *
import random

class Token:
    def __init__(self, window):
        self.win = window
        self.rad = 14   # Set token circle's radius to 14. 
        self.xCoord = random.randrange(15, 585, 30)   # Set token circle's centerpoint to random x and y 
        self.yCoord = random.randrange(15, 585, 30)   # values on intervals of cell width/length. 
        self.center = Point(self.xCoord, self.yCoord)   
        self.token = Circle(self.center, self.rad)
        self.token.setFill("red")   # Set token circle's color to red. 

    def drawToken(self):
        '''Draws a given token onto the board'''
        self.token.draw(self.win)

    def removeToken(self):
        '''Undraws a given token.'''
        self.token.undraw()

    def getCircleCenter(self):
        '''Returns a given token's centerpoint.'''
        return self.center

    def drawEdgeToken(self):
        '''Draws a token along one of the board's edges (instead 
        of placing it in a random cell anywhere on the board).'''
        
        num = random.randint(1,4)   # Assign a random int between 1 and 4 to 'num', so that odds of an 
                                    # edge token being drawn along any one of the four borders are 1 in 4. 
        if num == 1:    # If num is 1, place new token along left edge.
            self.xCoord = 15
            self.center = Point(self.xCoord, self.yCoord)
            self.token = Circle(self.center, self.rad)
        elif num == 2:  # If num is 2, place new token along right edge.
            self.xCoord = 585
            self.center = Point(self.xCoord, self.yCoord)
            self.token = Circle(self.center, self.rad)
        elif num == 3:  # If num is 3, place new token along top edge.
            self.yCoord = 15
            self.center = Point(self.xCoord, self.yCoord)
            self.token = Circle(self.center, self.rad)
        else:       # Else (which means num is 4), place new token along bottom edge.
            self.yCoord = 585
            self.center = Point(self.xCoord, self.yCoord)
            self.token = Circle(self.center, self.rad)
        
        self.token.setFill("red")
        self.token.draw(self.win)   # Draw edge token onto the window.