from piece import Piece
from random import random
from time import sleep

class Board():
    def __init__(self, dim, p):
        self.dim = dim
        self.p = p
        self.won = False
        self.numClicked = 0
        self.numNonBombs = 0
        self.setBoard()
        # layout of dictionary -> piece : [clue, safe neighbors, mine neighbors, hidden neighbors]
        self.boardStatus = {}
        self.flagList = []
        self.finishedList = []
        self.bombList = []

    # set all the pieces in the board
    def setBoard(self):
        self.board = []
        for row in range(self.dim[0]):
            row = []
            for col in range(self.dim[1]):
                # generate a random boolean for a bomb and set the piece as a bomb based on it
                isBomb = random() < self.p
                if (not isBomb):
                    # increment the number of bombs on the board
                    self.numNonBombs += 1
                # set the piece as a bomb
                piece = Piece(isBomb)
                # append the piece to the board
                row.append(piece)
            self.board.append(row)
        self.setNeighbors()

    # set all the neighbors for each piece
    def setNeighbors(self):
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                piece = self.getPiece((row, col))
                neighbors = self.getListOfNeighbors((row, col))
                piece.setNeighbors(neighbors)

    # get all the neighbors of a piece passed
    def getListOfNeighbors(self, index):
        neighbors = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                # do not count it as a neighbor if the coordinate is out of bounds
                outOfBounds = row < 0 or row >= self.dim[0] or col < 0 or col >= self.dim[1]
                same = row == index[0] and col == index[1]
                if (same or outOfBounds):
                    continue
                neighbors.append(self.getPiece((row, col)))
        return neighbors

    # return the size of the board
    def getSize(self):
        return self.dim

    # return the piece based on a passed in index
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

        # if the piece that we clicked has bomb 
        if (piece.getIsBomb()):       
            for neighbor in piece.getNeighbors():
                self.updateNeighborStatus(neighbor)
            self.bombList.append(piece.getIndex())
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

        # if piece is bomb
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
            elif neighbor.getClicked() and neighbor.getIsBomb():
                mineNeighbors += 1
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
        
        if piece.getIsBomb():
            return
        # Dont Update if its a flag
        if piece.getFlagged() or not piece.getClicked():
            return
        if piece.getIndex() in self.finishedList:
            return

        # Check each neighbor of a piece for mines, safe, and hidden neighbors
        for neighbor in piece.getNeighbors():
            if neighbor.getFlagged():
                mineNeighbors += 1
            elif neighbor.getClicked() and neighbor.getIsBomb():
                mineNeighbors += 1
            elif neighbor.getClicked():
                safeNeighbors += 1
            else:
                hiddenNeighbors += 1

        value = [clue, safeNeighbors, mineNeighbors, hiddenNeighbors, "N/A"]

        # append all the found values for each neighbor into the boardStatus dictionary
        self.boardStatus[piece.getIndex()] = value
 
    # set whether the neighbors of a piece can determined definitvely based on the basic strategy
    def setDictionaryStrategy(self):
        for keys, values in self.boardStatus.items():
            if values[0] == 0:
                values[4] = "N/A"
            elif values[0] - values[2] == values[3]:
                values[4] = "NeighborsAreBombs"
            elif values[0] == values[2]:
                values[4] = "NeighborsAreSafe"
            else:
                values[4] = "Unsure"
    
    # cleans the dictionary holding the pieces of board
    def cleanDictionary(self):
        for keys, values in self.boardStatus.copy().items():
            # cleans if all the Neighbors Are bombs, if there are no more hidden neighbors, and if all Neighbors are safe
            if values[3] == 0 :
                self.boardStatus.pop(keys)
                self.finishedList.append(keys)
    
    def getWon(self):
        return self.numNonBombs == self.numClicked

    # commits the changes for the agent's knowledge based off the clues
    def initializePieces (self) :
        
        for keys, values in self.boardStatus.copy().items():
            self.setDictionaryStrategy()
            if values[4] == "NeighborsAreBombs":
                piece = self.getPiece(keys)
                self.setAllFlag(piece)
            elif values[4] == "NeighborsAreSafe":
                piece = self.getPiece(keys)
                self.revealAllNeighbors(piece)

    # set all neighbors of a piece to be flagged if it has not been clicked or flagged already
    def setAllFlag (self, piece):
        for neighbor in piece.getNeighbors():   
            if neighbor.getClicked() or neighbor.getFlagged() :
                continue
            else :
                self.handleClick(neighbor,True)
    
    # click all neighbors if all hidden neighbors around the piece are safe
    def revealAllNeighbors (self, piece):
        for neighbor in piece.getNeighbors():
            if neighbor.getClicked() or neighbor.getFlagged() :
                continue
            else :
                self.handleClick(neighbor,False)   
                self.setBoardStatus(neighbor)                 

    



