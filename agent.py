class Agent():
    def __init__(self, dim):
        self.dim = dim
        self.boardStatus = {}
    # piece : [clue, safe neighbors, mine neighbors, hidden neighbors]
    def setBoardStatus(self, piece, index):
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

        self.boardStatus[index] = value
        print(self.boardStatus)
            

            
                