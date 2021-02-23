from piece import Piece
from random import random

class Board():
    def __init__(self, dim, p):
        self.dim = dim
        self.p = p
        self.setBoard()

    def setBoard(self):
        self.board = []
        for row in range(self.dim[0]):
            row = []
            for col in range(self.dim[1]):
                isBomb = random() < self.p
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