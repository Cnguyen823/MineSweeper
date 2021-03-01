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
        rightClick = False

        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(self.screenSize[0] // 2, self.screenSize[1] // 2)))

        while running:
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
                    
                    # print(rightClick)

                    # handles the click based on what was pressed 
                    self.handleClick(event.pos, rightClick)

                    self.board.cleanDictionary()

                    print("Last:")
                    print(self.board.boardStatus)
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

    def postEvent(self):
        for keys, values in self.board.boardStatus.items():
            if values[4] == "NeighborsAreSafe":
                print("Key is here in NeighborsAreSafe: ", keys)
                piece = self.board.getPiece(keys)
                for neighbor in piece.getNeighbors():
                    if neighbor.getFlagged() or neighbor.getClicked():
                        continue
                    else:
                        post = neighbor.getIndex()
                        postX = post[1] * self.imageSize[1]
                        postY = post[0] * self.imageSize[0]
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(postX, postY)))
                        print("This is post in NeighborsAreSafe: ",post)
                        return
            elif values[4] == "NeighborsAreBombs":
                print("Key is here in NeighborsAreBombs: ", keys)
                piece = self.board.getPiece(keys)
                for neighbor in piece.getNeighbors():
                    if neighbor.getFlagged() or neighbor.getClicked():
                        continue
                    else:
                        post = neighbor.getIndex()
                        postX = post[1] * self.imageSize[1]
                        postY = post[0] * self.imageSize[0]
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=3, pos=(postX, postY)))
                        print("This is post in NeighborsAreBombs: ",post)
                        return
        
        self.postRandomEvent()

    def postRandomEvent(self):
        for key in self.board.boardStatus:
            print("This is the key in random event: ", key)
            randomPiece = self.board.getPiece(key)
            for neighbor in randomPiece.getNeighbors():
                if neighbor.getFlagged() or neighbor.getClicked():
                    continue
                else:
                    post = neighbor.getIndex()
                    postX = post[1] * self.imageSize[1]
                    postY = post[0] * self.imageSize[0]
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(postX, postY)))
                    print("This is post in NeighborsAreSafe: ",post)
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
        # if we have lost do not handle clicks anymore
        print("This is position: ", position)
        if(self.board.getExplode()):
            return
        # gets index of piece that was clicked
        # print("Positon[1]: ", position[1], "imageSize[1]: ", self.imageSize[1], "position[0]: ", position[0], "imageSize[0]: ", self.imageSize[0])
        index = position[1] // self.imageSize[1], position[0] // self.imageSize[0]
        # print("This is the index in handClick: ", index)

        # grabs the piece from the board
        piece = self.board.getPiece(index)
        
        # passes the piece to board to handle functionality of the click
        self.board.handleClick(piece, rightClick)

        # updates the status of the agent
        self.board.setBoardStatus(piece)

        # Agent does stuff
        self.board.initializePieces()

        print("middle:")
        print(self.board.boardStatus)


        
