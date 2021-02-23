class Piece():
    def __init__(self, isBomb):
        self.isBomb = isBomb
        self.clicked = False
        self.flagged = False

    def getIsBomb(self):
        return self.isBomb

    def getClicked(self):
        return self.clicked

    def getFlagged(self):
        return self.flagged

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        self.setNumOfBombs()
    
    def setNumOfBombs(self):
        self.numOfBombs = 0
        for piece in self.neighbors:
            if(piece.getIsBomb()):
                self.numOfBombs += 1

    def getNumOfBombs(self):
        return self.numOfBombs