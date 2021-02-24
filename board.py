from piece import Piece
from random import random

class Board():
    def __init__(self, dim, p):
        self.dim = dim
        self.p = p
        self.explode = False
        self.won = False
        self.numClicked = 0
        self.numNonBombs = 0
        self.setBoard()

    def setBoard(self):
        self.board = []
        for row in range(self.dim[0]):
            row = []
            for col in range(self.dim[1]):
                isBomb = random() < self.p
                if (not isBomb):
                    self.numNonBombs += 1
                piece = Piece(isBomb)
                row.append(piece)
            self.board.append(row)
        self.setNeighbors()

    def setNeighbors(self):
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                piece = self.getPiece((row, col))
                neighbors = self.getListOfNeighbors((row, col))
                piece.setNeighbors(neighbors)

    def getListOfNeighbors(self, index):
        neighbors = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                outOfBounds = row < 0 or row >= self.dim[0] or col < 0 or col >= self.dim[1]
                same = row == index[0] and col == index[1]
                if (same or outOfBounds):
                    continue
                neighbors.append(self.getPiece((row, col)))
        return neighbors

    def getSize(self):
        return self.dim

    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    #handles click on board
    def handleClick(self, piece, flag):
        #cannot click on piece that is flagged or that has been clicked
        if (piece.getClicked() or (not flag and piece.getFlagged())):
            return

        # if flag then get flag then set proper value
        if (flag):
            piece.setFlag()
            return

        # else we left clicked
        piece.click()

        # if the piece that we clicked has bomb we explode
        if (piece.getIsBomb()):
            self.explode = True
            return
        
        # increment how many piece we have clicked
        self.numClicked += 1

        if (piece.getNumOfBombs() != 0):
            return
        
        for neighbor in piece.getNeighbors():
            if (not neighbor.getIsBomb() and not neighbor.getClicked()):
                self.handleClick(neighbor,False)

        
    def getExplode(self):
        return self.explode
    
    def getWon(self):
        return self.numNonBombs == self.numClicked


