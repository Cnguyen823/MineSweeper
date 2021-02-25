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

        #if piece is bomb dont keep track end game
        if piece.getIsBomb():
            return

        # if piece is flag we append to flag list and do not need to keep track of its clues in board status 
        if piece.getFlagged():
            self.flagList.append(piece.getIndex())
            print(self.flagList)
            return

        # if piece was previously flagged but is no longer we remove from flag list
        if piece.getIndex() in self.flagList:
            self.flagList.remove(piece.getIndex())
            print(self.flagList)
            print(self.boardStatus)
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

        value = [clue, safeNeighbors, mineNeighbors, hiddenNeighbors]

        # Sets index of piece as key with its clues as the value
        self.boardStatus[piece.getIndex()] = value
        print(self.boardStatus)
        print(self.flagList)

    
    # Updates the clues and information of pieces already clicked
    def updateNeighborStatus(self, piece):
        safeNeighbors = 0
        mineNeighbors = 0
        hiddenNeighbors = 0
        clue = piece.getNumOfBombs()
            
        for neighbor in piece.getNeighbors():
            if neighbor.getFlagged():
                mineNeighbors += 1
            elif neighbor.getClicked():
                safeNeighbors += 1
            else:
                hiddenNeighbors += 1

        value = [clue, safeNeighbors, mineNeighbors, hiddenNeighbors]

        self.boardStatus[piece.getIndex()] = value
    
    def getExplode(self):
        return self.explode
    
    def getWon(self):
        return self.numNonBombs == self.numClicked



