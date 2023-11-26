from game import Board
from defaults import MARKS
from errors import IllegalMove, GameTied, GameEnd

import sys

class State:
  ''' State of the game ;;
    contains only string representation of state
    calls Board for all other tasks
  '''

  def __init__(self, w, h, init=''):
    self.WIDTH = w; self.HEIGHT = h
    self.board = Board(w,h)
    self.state = ''
    if init: # begin game from some position
      index = 0
      for move in init:
        mark = MARKS[index]
        try: self.play(int(move), mark)
        except GameEnd:
          print('Game ended before simulation completed')
          sys.exit(0)
        index = (index+1) % 2

  def __str__(self):
    return str(self.board)

  def __repr__(self):
    return 'Connect4 game with state :: ' + self.state

  def get_state(self):
    return self.state

  def get_moves(self):
    return len(self.state)

  def get_score(self):
    return self.board.get_score()

  def undo(self):
    self.state = self.state[:-1]
    self.board.undo()

  def reset(self):
    self.state = ''
    self.board = self.board.reset()
    return self

  def is_legal(self, c):
    try: self.board.is_legal(c)
    except IllegalMove: return False
    return True
  
  def check_win(self, c, mark):
    try: 
      self.board.update(c, mark)
      self.board.is_aligned(c)
    except GameEnd as end:
      self.board.undo()
      if type(end).__name__ == 'GameTied': 
        return False # TODO :: consts?
      else: return True
    self.board.undo()
    return False

  def get_legal_positions(self): # why is this?
    return self.board.get_legal_positions()

  # raises GameEnd, IllegalMove
  def play(self, c, mark, sim=False):
    self.board.is_legal(c, sim=sim)
    self.board.update(c, mark, sim=sim)
    self.state += str(c)
    self.board.is_aligned(c, sim=sim)