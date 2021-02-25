from game import Game
from board import Board
from agent import Agent

size = (9, 9)
p = 0.2
board = Board(size, p)
agent = Agent(size)
screenSize = (500,500)
game = Game(board, screenSize, agent)
game.run()