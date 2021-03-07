class Piece():
    def __init__(self, isBomb):
        self.isBomb = isBomb
        self.clicked = False
        self.flagged = False
        self.index = ()
        self.hiddenNeighbors = []
        self.setNormalForm = ()

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
        for neighbor in self.neighbors:
            if(neighbor.getIsBomb()):
                self.numOfBombs += 1

    def getNumOfBombs(self):
        return self.numOfBombs
    
    def setFlag(self):
        self.flagged = not self.flagged
    
    def click(self):
        self.clicked = True
    
    def getNeighbors(self):
        return self.neighbors

    def setIndex(self, index):
        self.index = index

    def getIndex(self):
        return self.index

    def setHiddenNeighbors(self, hList):
        self.hiddenNeighbors = hList

    def getHiddenNeighbors(self):
        return self.hiddenNeighbors