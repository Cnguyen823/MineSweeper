from game import Game
from board import Board

size = (9, 9)
p = 0.5
board = Board(size, p)
screenSize = (500,500)
game = Game(board, screenSize)
game.run()
#yo nerd