from board import Board
class Agent():
    def __init__(self, dim):
        self.dim = dim
        # layout of dictionary -> piece : [clue, safe neighbors, mine neighbors, hidden neighbors]
        self.boardStatus = {}
        self.flagList = []

   
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
            return

        # if piece was previously flagged but is no longer we remove from flag list and add to board status
        if piece.getIndex() in self.flagList:
            self.flagList.remove(piece.getIndex())

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
    


            
                