from graphics import *
from token import Token
import time, random

class Snake:
    def __init__(self, window, upperX, upperY, lowerX, lowerY):
        self.win = window
        self.upperX, self.upperY = upperX, upperY
        self.lowerX, self.lowerY = lowerX, lowerY
        self.speed = 0.3    # Sets initial speed value (time between each "move", in seconds).
        self.score = 0      # User's score initialized to zero.
        self.direction = "Down"    # Game begins with snake moving in 'down' direction.
        self.gameOver = False      # While False, game loop in main() executes.

        self.token = Token(self.win)
        # Initializes self.snakeBody to a list of rectangles representing the snake. 
        self.snakeBody = [Rectangle(Point(self.upperX, self.upperY), Point(self.lowerX, self.lowerY)), 
        Rectangle(Point(self.upperX, self.upperY + 30), Point(self.lowerX, self.lowerY + 30)), 
        Rectangle(Point(self.upperX, self.upperY + 60), Point(self.lowerX, self.lowerY + 60))]

    def drawBoard(self):
        '''Draws the board onto the window as a chessboard-patterned grid.'''
        
        i = 0
        j = 0
        for k in range(20):    # Nested loops to make a 20-by-20 grid of rectangles representing the board.
            while i <= 600 and j <= 600:
                oneGrid = Rectangle(Point(i, j), Point(i + 30, j + 30))
                oneGrid.draw(self.win)
                i += 30
                if (i // 30) % 2 == 0 and k % 2 == 0:    # Colors the grid with two alternating colors.
                    oneGrid.setFill("green")
                elif k % 2 == 1 and (i // 30) % 2 == 1:
                    oneGrid.setFill("green")
                else:
                    oneGrid.setFill("light green")
            i = 0
            j += 30

    def moveBody(self):
        '''Draws and undraws each rectangle in the snake's body, moving each piece forward by one.'''

        for i in range(len(self.snakeBody) - 1, 0, -1):    # Iterates through a reversed list of snakeBody 
                                                           # rectangles, updating each piece's position to
                                                           # the piece in front of it. 
            self.snakeBody[i].undraw()
            self.snakeBody[i] = self.snakeBody[i - 1].clone()
            self.snakeBody[i].draw(self.win)
        self.snakeBody[0].undraw()    # Undraws the snake's head (redrawn in methods below). 

    def drawHead(self):
        '''Draws the snake's head in its updated position.'''

        self.snakeBody[0] = Rectangle(Point(self.upperX, self.upperY), Point(self.lowerX, self.lowerY))
        self.headBodyCollision()    # Calls a later method to check whether head has collided with body.
        
        if self.gameOver == True:   # If collision has occurred, head's updated position is not drawn.
            return
        else:   # If collision has not occurred, draws head in its new position. 
            self.snakeBody[0].setFill("gold")
            self.snakeBody[0].draw(self.win)

    def moveHead(self):
        '''Detects arrowkey presses from the user and moves snake's head accordingly.'''

        # Prevents the user from reversing the snake's direction (only allows 90-degree turns). 
        if self.win.lastKey == "Right" and self.direction != "Left":
            self.direction = "Right"
        elif self.win.lastKey == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif self.win.lastKey == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif self.win.lastKey == "Down" and self.direction != "Up":
            self.direction = "Down"

        if self.direction == "Right":   # Moves the snake's head to the right and updates its x- and y-coordinates. 
            if self.lowerX < 600:
                self.snakeBody[0].move(30, 0)
                self.upperX += 30
                self.lowerX += 30
                if (((self.upperX + self.lowerX) / 2) == self.token.xCoord) and (((self.upperY + 
                self.lowerY) / 2) == self.token.yCoord):    # Checks coordinates to determine whether snake's head
                                                            # has come into contact with a token. 
                    self.eatToken()
            else:   # If snake's head has collided with the border, set self.gameOver to True. 
                self.gameOver = True
                return
            time.sleep(self.speed) # Pause for some interval (given in seconds by self.speed) before moving again.
        elif self.direction == "Left":   # Moves the snake's head to the left and updates its x- and y-coordinates. 
            if self.upperX > 0:
                self.snakeBody[0].move(-30, 0)
                self.upperX -= 30
                self.lowerX -= 30
                if (((self.upperX + self.lowerX) / 2) == self.token.xCoord) and (((self.upperY + 
                self.lowerY) / 2) == self.token.yCoord):
                    self.eatToken()
            else:
                self.gameOver = True
                return
            time.sleep(self.speed)
        elif self.direction == "Down":   # Moves the snake's head downwards and updates its x- and y-coordinates. 
            if self.lowerY < 600:
                self.snakeBody[0].move(0, 30)
                self.upperY += 30
                self.lowerY += 30
                if (((self.upperX + self.lowerX) / 2) == self.token.xCoord) and (((self.upperY + 
                self.lowerY) / 2) == self.token.yCoord):
                    self.eatToken()
            else:
                self.gameOver = True
                return
            time.sleep(self.speed)
        elif self.direction == "Up":   # Moves the snake's head upwards and updates its x- and y-coordinates. 
            if self.upperY > 0:
                self.snakeBody[0].move(0,-30)
                self.upperY -= 30
                self.lowerY -= 30
                if (((self.upperX + self.lowerX) / 2) == self.token.xCoord) and (((self.upperY + 
                self.lowerY) / 2) == self.token.yCoord):
                    self.eatToken()
            else:
                self.gameOver = True
                return
            time.sleep(self.speed)

    def updateLength(self):
        '''Increases the snake's length by one rectangle (for every two tokens eaten).'''

        if (self.score != 0) and (self.score % 2) == 0:
            # Adds new rectangle to the snakeBody list.
            self.snakeBody.append(self.snakeBody[len(self.snakeBody) - 1].clone())
            self.wonGame()  # Calls wonGame() to check if the snake's body occupies the entire board. 

    def headBodyCollision(self):
        '''Checks whether snake's head has collided with its body. If so, sets self.gameOver to True.'''

        # For each rectangle in snakeBody list, compares position to head's position.
        for i in range(2, len(self.snakeBody)):
            if (str(self.snakeBody[i].getCenter()) == str(self.snakeBody[0].getCenter())):
                self.gameOver = True
                return

    def updateSpeed(self):
        '''Speeds up movement by decreasing pause intervals.'''
        self.speed = self.speed * 0.92

    def updateScore(self):
        '''Increments the user's score by one.'''
        self.score += 1

    def getScore(self):
        '''Returns the user's score as a string.'''
        return str(self.score)

    def eatToken(self):
        '''Calls other setter methods to update score, speed, and length. 
        Removes the eaten token and makes a new one.'''

        self.updateScore()
        self.updateSpeed()
        self.updateLength()
        self.token.removeToken()
        self.token = Token(self.win)
        self.redrawToken()

    def redrawToken(self):
        '''Prevents token from being drawn under snake's body by redrawing it if so.'''

        self.tokenAI()  # Calls tokenAI() to draw a token (either strategically or randomly).
        for i in range(0, len(self.snakeBody)):
            # Checks token position against each rectangle in snakeBody--if positions match, redraws token. 
            while (str(self.snakeBody[i].getCenter()) == str(self.token.getCircleCenter())):
                self.token.removeToken()
                self.tokenAI()
                for i in range(0, len(self.snakeBody)):
                    # Acts as a backup to prevent token from appearing under snake's body twice in a row. 
                    while (str(self.snakeBody[i].getCenter()) == str(self.token.getCircleCenter())):
                        self.token.removeToken()
                        self.tokenAI()

    def tokenAI(self):
        '''Depending on user's current score, decides the frequency of token 
        being drawn in hard-to-reach spots (edge cells) vs. random spots.'''

        self.token = Token(self.win)
        num = random.randint(1, 10)    # Assigns a random int between 1 and 10 to 'num'. 

        if self.score <= 10:    # If user's score is 10 or less, 100% chance of random token placement. 
            self.token.drawToken()
        elif self.score <= 20:  # If user's score is between 11 and 20, 10% chance of strategic (edge) token placement.
            if num == 1:
                self.token.drawEdgeToken()
            else:   # 90% chance of random token placement. 
                self.token.drawToken()
        elif self.score <= 30:  # If user's score is between 21 and 30, 20% chance of strategic (edge) token placement.
            if num == 1 or num == 2:
                self.token.drawEdgeToken()
            else:   # 80% chance of random token placement. 
                self.token.drawToken()
        else:   # If user's score is greater than 30, 60% chance of strategic (edge) token placement. 
            if num != 10 and num != 9 and num != 8 and num != 7:
                self.token.drawEdgeToken()
            else:   # 40% chance of random token placement. 
                self.token.drawToken()

    def wonGame(self):
        '''Checks to see if the user has won the game.'''

        if len(self.snakeBody) == 398:  # If snake's body is 398 rectangles long, no more space is available for tokens.
            self.gameOver = True        # If user has won, self.gameOver is set to True. 
            return self.gameOver

    def restartGame(self):
        '''Returns a boolean depending on user's most recent key input.'''

        if self.win.checkKey() == "r":
            return True
        elif self.win.checkKey() == "q":
            return False
