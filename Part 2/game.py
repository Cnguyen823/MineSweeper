import pygame
import os
from time import sleep
import random

class Game():
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        self.imageSize = self.screenSize[0] // self.board.getSize()[1], self.screenSize[1] // self.board.getSize()[0]
        self.loadImages()
    
    #Runs Mine Sweeper
    def run(self):
        pygame.init()
        self.gui = pygame.display.set_mode(self.screenSize)
        running = True
        rightClick = False

        #Initiates first random click
        self.postRandomEvent()

        while running:
            sleep(1)
            # posts the next even to be completed
            self.postEvent()

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()

                # when mouse is pressed
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    # gets the position of where the mouse was clicked
                    
                    # checks if click was right click or left click

                    if event.button == 1:
                        rightClick = False
                    elif event.button == 3:
                        rightClick = True
                    
                    # handles the click based on what was pressed 
                    self.handleClick(event.pos, rightClick)

                    # cleans the clues from board dictionary that we no longer need
                    self.board.cleanDictionary()

               
                self.drawBoard()
                pygame.display.flip()
                if(self.board.getWon()):
                    pygame.mixer.music.load("audio/Armenia.mp3")
                    pygame.mixer.music.play(start=12)
                    sleep(10)
                    print("You Have Won!");
                    running = False

# Based on current clues implements the basic strategies and posts the event for the next iteration
    def postEvent(self):
        self.board.setDictionaryStrategy();
        for keys, values in self.board.boardStatus.items():
            if values[4] == "NeighborsAreSafe":
                piece = self.board.getPiece(keys)
                for neighbor in piece.getNeighbors():
                    if neighbor.getFlagged() or neighbor.getClicked():
                        continue
                    else:
                        post = neighbor.getIndex()
                        postX = post[1] * self.imageSize[1]
                        postY = post[0] * self.imageSize[0]
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(postX, postY)))
                        return
            elif values[4] == "NeighborsAreBombs":
                piece = self.board.getPiece(keys)
                for neighbor in piece.getNeighbors():
                    if neighbor.getFlagged() or neighbor.getClicked():
                        continue
                    else:
                        post = neighbor.getIndex()
                        postX = post[1] * self.imageSize[1]
                        postY = post[0] * self.imageSize[0]
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=3, pos=(postX, postY)))
                        return
        
        self.board.inference()

        self.postRandomEvent()

# add a random click event to queue to be executed next iteration
    def postRandomEvent(self):
        while True:
            post = (random.randint(0,self.board.dim[0]-1), random.randint(0,self.board.dim[1]-1))
            piece = self.board.getPiece(post)
            if piece.getClicked() or piece.getFlagged():
                continue
            else:
                postX = post[1] * self.imageSize[1]
                postY = post[0] * self.imageSize[0]
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(postX, postY)))
                return


    def drawBoard(self):
        topLeft = (0,0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                piece.setIndex((row,col))
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
            string = "Flag-Pins-Armenia-Vietnam" if piece.getFlagged() else "empty-block"

        return self.imageDict[string]
    
    # Converts positon into an index
    def handleClick(self, position, rightClick):
        # gets index of piece that was clicked
        index = position[1] // self.imageSize[1], position[0] // self.imageSize[0]

        # grabs the piece from the board
        piece = self.board.getPiece(index)
        
        # passes the piece to board to handle functionality of the click
        self.board.handleClick(piece, rightClick)

        # updates the status of the agent
        self.board.setBoardStatus(piece)

        # Agents grabs its clues
        self.board.initializePieces()

       


        
