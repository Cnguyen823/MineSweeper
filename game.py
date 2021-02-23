import pygame
import os

class Game():
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        self.imageSize = self.screenSize[0] // self.board.getSize()[1], self.screenSize[1] // self.board.getSize()[0]
        self.loadImages()
    
    def run(self):
        pygame.init()
        self.gui = pygame.display.set_mode(self.screenSize)
        while True:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
                self.drawBoard()
                pygame.display.flip()

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
            if(file.endswith(".png")):
                image = pygame.image.load(r"images/" + file)
                image = pygame.transform.scale(image, self.imageSize)
                self.imageDict[file.split(".")[0]] = image

    def getImage(self, piece):
        string = "Gutz" if piece.getIsBomb() else str(piece.getNumOfBombs())

        return self.imageDict[string]
