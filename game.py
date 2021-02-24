import pygame
import os
from time import sleep
class Game():
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        self.imageSize = self.screenSize[0] // self.board.getSize()[1], self.screenSize[1] // self.board.getSize()[0]
        self.loadImages()
    
    def run(self):
        pygame.init()
        self.gui = pygame.display.set_mode(self.screenSize)
        running = True
        while running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()

                # when mouse is pressed
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    # gets the position of where the mouse was clicked
                    position = pygame.mouse.get_pos()
                    
                    # checks if click was right click or left click
                    rightClick = pygame.mouse.get_pressed()[2]

                    # handles the click based on what was pressed 
                    self.handleClick(position, rightClick)
                self.drawBoard()
                pygame.display.flip()
                if(self.board.getWon()):
                    #sound.play()
                    #sleep(3)
                    print("You Have Won!");
                    running = False
                elif (self.board.getExplode()):
                    print("sucks to suck")
                    running = False

    def drawBoard(self):
        topLeft = (0,0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.gui.blit(image, topLeft)
                topLeft = topLeft[0] + self.imageSize[0], topLeft[1]
            topLeft = 0, topLeft[1] + self.imageSize[1]

    def loadImages(self):
        self.imageDict = {}
        for file in os.listdir("images"):
            if (file.endswith(".png")):
                image = pygame.image.load(r"images/" + file)
                image = pygame.transform.scale(image, self.imageSize)
                self.imageDict[file.split(".")[0]] = image

    # chooses what image to display if clicked or not
    def getImage(self, piece):
        string = None

        # if piece that is clicked is bomb render a bomb else render the picture with number of bombs around
        if (piece.getClicked()):
            string = "bomb-at-clicked-block" if piece.getIsBomb() else str(piece.getNumOfBombs())
        else:
            string = "flag" if piece.getFlagged() else "empty-block"

        return self.imageDict[string]
    
    # Converts positon into an index
    def handleClick(self, position, rightClick):
        # if we have lost do not handle clicks anymore
        if(self.board.getExplode()):
            return
        # gets index of piece that was clicked
        index = position[1] // self.imageSize[1], position[0] // self.imageSize[0]

        # grabs the piece from the board
        piece = self.board.getPiece(index)
        
        # passes the piece to board to handle functionality of the click
        self.board.handleClick(piece, rightClick)