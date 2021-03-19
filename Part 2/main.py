from game import Game
from board import Board


size = (9, 9)
p = 10 / (size[0] * size[1])
board = Board(size, p)
screenSize = (500,500)
game = Game(board, screenSize)
game.run()