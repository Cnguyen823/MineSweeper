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
        # layout of dictionary -> piece : [clue, safe neighbors, mine neighbors, hidden neighbors]
        self.boardStatus = {}
        self.flagList = []
        self.finishedList = []

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
        # update the neighbors of flagged pieces so we can keep track of safe neighbors
        if (flag):
            piece.setFlag()
            for neighbor in piece.getNeighbors():
                self.updateNeighborStatus(neighbor)
            self.setDictionaryStrategy()
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
        
        # recursively click neighbors for empty spaces update board status along with recursive clicks
        for neighbor in piece.getNeighbors():
            if (not neighbor.getIsBomb() and not neighbor.getClicked()):
                self.handleClick(neighbor,False)   
                self.setBoardStatus(neighbor)             

    
     # Sets initial information and clues of each piece clicked
    def setBoardStatus(self, piece):
        safeNeighbors = 0
        mineNeighbors = 0
        hiddenNeighbors = 0
        clue = piece.getNumOfBombs()

        # if piece is bomb dont keep track end game
        if piece.getIsBomb():
            return

        # don't add piece to list if it's already been solved
        if piece.getIndex() in self.finishedList:
            return

        # if piece is flag we append to flag list and update its neighbors do not need to keep track of its clues in board status 
        if piece.getFlagged():
            self.flagList.append(piece.getIndex())
            for neighbor in piece.getNeighbors():
                if neighbor.getClicked():
                    self.updateNeighborStatus(neighbor)
            return

        # if piece was previously flagged but is no longer we remove from flag list
        if piece.getIndex() in self.flagList:
            self.flagList.remove(piece.getIndex())
            return

        # Updates the clues of neighbor if clicked and gets clues for current piece
        for neighbor in piece.getNeighbors():
            if neighbor.getFlagged():
                mineNeighbors += 1
                indexOfPiece = neighbor.getIndex()
                if indexOfPiece not in self.flagList:
                    temp = self.boardStatus.pop(indexOfPiece,None)
                    self.flagList.append(indexOfPiece)
            elif neighbor.getClicked():
                safeNeighbors += 1
                self.updateNeighborStatus(neighbor)
            else:
                hiddenNeighbors += 1

        value = [clue, safeNeighbors, mineNeighbors, hiddenNeighbors, "N/A"]

        # Sets index of piece as key with its clues as the value
        self.boardStatus[piece.getIndex()] = value
        
        self.setDictionaryStrategy()

    
    # Updates the clues and information of pieces already clicked
    def updateNeighborStatus(self, piece):
        safeNeighbors = 0
        mineNeighbors = 0
        hiddenNeighbors = 0
        clue = piece.getNumOfBombs()
        
        # Dont Update if its a flag
        if piece.getFlagged() or not piece.getClicked():
            return

        if piece.getIndex() in self.finishedList:
            return

        for neighbor in piece.getNeighbors():
            if neighbor.getFlagged():
                mineNeighbors += 1
            elif neighbor.getClicked():
                safeNeighbors += 1
            else:
                hiddenNeighbors += 1

        value = [clue, safeNeighbors, mineNeighbors, hiddenNeighbors, "N/A"]

        self.boardStatus[piece.getIndex()] = value
 
    def setDictionaryStrategy(self):
        for keys, values in self.boardStatus.items():
            if values[0] == 0:
                values[4] = "N/A"
            elif values[0] - values[2] == values[3]:
                values[4] = "NeighborsAreBombs"
            elif (8 - values[0]) - values[1] == values[3]:
                if not self.isBorder(keys):
                    values[4] = "NeighborsAreSafe"
                else:
                    values[4] = "Unsure"
            else:
                values[4] = "Unsure"

    def isBorder(self, index):
        if index[0] == 0 or index[1] == 0 or index[0] == self.dim[0]-1 or index[1] == self.dim[0]-1:
            return True
        return False
    
    def cleanDictionary(self):
        for keys, values in self.boardStatus.copy().items():
            if values[4] == "NeighborsAreBombs" or values[3] == 0 or values[4] == "NeighborsAreSafe":
                self.boardStatus.pop(keys)
                self.finishedList.append(keys)

    
    def getExplode(self):
        return self.explode
    
    def getWon(self):
        return self.numNonBombs == self.numClicked

    



