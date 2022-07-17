from graphics import *
from token import Token
from snake import Snake
import time

def constructText(window, text):
    '''Formats and draws a given Text object onto the window.'''

    text.setStyle("bold")
    text.setSize(25)
    text.draw(window)

def main():
    playAgain = True    # When set to True, while loop below executes and game can be played. 

    while playAgain:
        win = GraphWin("Snake", 600, 650)   # Constructs our graphical window. 

        scoreOutput = Text(Point(300, 625), "Your score: 0")    # Makes a new text object with scoring information.
        constructText(win, scoreOutput)

        snake = Snake(win, 150, 210, 180, 240)    # Makes an instance of class Snake. 
        snake.drawBoard()    # Calls Snake's drawBoard() method to construct grid of cells. 
        snake.redrawToken()    # Draws a token onto our window. 

        while not snake.gameOver:   # While snake.gameOver == False, loops continuously to allow gameplay. 
            snake.moveBody()    # Draws/moves the snake's body according to head position. 
            snake.drawHead()    # Draws the snake's head onto the window. 
            snake.moveHead()    # Moves the snake's head according to user's arrowkey inputs. 

            scoreOutput.undraw()    # Updates text with new scoring info. 
            scoreOutput = Text(Point(300, 625), "Your score: " + snake.getScore())
            constructText(win, scoreOutput)

        snake.token.removeToken()   # After exiting above loop, undraws token and snake's body. 
        for i in range(0, len(snake.snakeBody)):
            snake.snakeBody[i].undraw()

        scoreOutput.undraw()    
        if not snake.wonGame():     # Displays new info about final score. 
            scoreOutput = Text(Point(300, 625), "The game has ended. You ate " + snake.getScore() + " tokens!")
        else:   # If user won the game, displays info informing them of their win. 
            scoreOutput = Text(Point(300, 625), "The game has ended. You won!")
        constructText(win, scoreOutput)
        time.sleep(3)   # Pauses for three seconds, allowing user to read message. 
        
        scoreOutput.undraw()    # Displays post-game instructions about how to restart or quit.  
        scoreOutput = Text(Point(300, 625), "Press 'r' to restart game. Press 'q' to quit.")
        constructText(win, scoreOutput)
        time.sleep(3)   # Pauses for three seconds, allowing user to read message. 
        
        if snake.gameOver:  # Restarts or quits game depending on user key inputs. 
            if snake.restartGame():
                playAgain = True
                snake.gameOver = False
                win.close()
            else:
                print("Thanks for playing!")
                playAgain = False
                sys.exit()


main()
