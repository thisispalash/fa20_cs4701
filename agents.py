from state import State
from defaults import MARKS
from errors import GameTied
import multiprocessing as mp

import random

class Human:
  def __init__(self, pos):
    self.pos = pos
    self.mark = MARKS[pos]

  def help(self,d,agent,game):
    d[0] = agent.solve(game)

  def play(self, state):
    # TODO :: interactive assist
    timeout = 5
    while True:
      c = input('Enter column number: ')
      pred = None
      try: c = int(c)
      except ValueError as e:
        if c == 'a':
          pred = AlphaBeta(self.pos)
        elif c == 'm':
          pred = NegaMax(self.pos)
        else: 
          print('  Ask our agents - a for alpha-beta; m for minimax')
          continue
        manager = mp.Manager(); d = manager.dict()
        p = mp.Process(target=self.help, args=(d,pred,state,))
        p.start(); p.join(timeout) # timeout = 5s
        if p.is_alive():
          print('  Agent took longer than '+str(timeout)+'s; you are on your own')
          p.terminate()
        else:
          print('  Agent says you should move at col', d[0]['column'])
      else: break
      del pred
    return c

class NegaMax:
  def __init__(self, pos):
    self.pos = pos
    self.mark = MARKS[pos]

  def __str__(self):
    ret = 'minim: '
    ret += 'player-' + str(self.pos+1)
    ret += '(' + self.mark + ')'
    return ret 

  def play(self, state):
    if state.get_moves() < 4: # TODO :: make variable
      return random.randint(0,state.WIDTH-1)
    return self.solve(state)['column'] 
    
  def solve(self, game):

    ret = {
      'score': (-1) * game.WIDTH*game.HEIGHT,
      'column': 0,
      'explored': 0
    }

    # check for winning col
    for col in range(game.WIDTH):
      ret['explored'] += 1 # check_win actually plays, so explored
      if game.is_legal(col) and game.check_win(col, self.mark):
        ret['score'] = game.get_score()
        ret['column'] = col
        return ret
    
    # find the best score by simulating opponent
    opp = NegaMax((self.pos+1)%2)
    for col in range(game.WIDTH):
      sim = State(game.WIDTH,game.HEIGHT,game.state) # simulate new game
      ret['explored'] += 1 # TODO :: count only legal cols?
      if sim.is_legal(col):
        try: sim.play(col, self.mark, sim=True)
        except GameTied: # already checked for win condition
          if 0 > ret['score']: ret['score'] = 0; ret['column'] = col
          break
        # let opponent play; store the negative of score
        opp_res = opp.solve(sim)
        ret['explored'] += opp_res['explored']
        score = (-1) * opp_res['score'] 
        if score > ret['score']: ret['score'] = score; ret['column'] = col
      del sim
    del opp
    return ret

class AlphaBeta:
  def __init__(self, pos):
    self.pos = pos
    self.mark = MARKS[pos]
    self.expl = 0

  def __str__(self):
    ret = 'alpha: '
    ret += 'player-' + str(self.pos+1)
    ret += '(' + self.mark + ')'
    return ret 

  def play(self, state):
    if state.get_moves() < 4: # TODO :: make variable
      return random.randint(0,state.WIDTH-1)
    return self.solve(state)['column'] 
    
  def solve(self, game, alpha=None, beta=None):

    ret = {
      'score': (-1) * game.WIDTH*game.HEIGHT,
      'column': 0,
      'explored': 0
    }

    # check for winning col
    for col in range(game.WIDTH):
      ret['explored'] += 1 # check_win actually plays, so explored
      if game.is_legal(col) and game.check_win(col, self.mark):
        ret['score'] = game.get_score()
        ret['column'] = col
        return ret

    # set search window
    if not alpha: alpha = (-1) * game.WIDTH * game.HEIGHT
    if not beta: beta = game.WIDTH * game.HEIGHT

    # prune ;; 
    if beta > game.get_score():
      beta = game.get_score() 
    if alpha >= beta:
      ret['score'] = beta
      return ret
    # NOTE :: ret['column'] = 0 doesn't matter as initially a=-inf,b=inf

    # find the best score by simulating opponent
    opp = AlphaBeta((self.pos+1)%2)
    for col in range(game.WIDTH):
      sim = State(game.WIDTH,game.HEIGHT,game.state) # simulate new game
      ret['explored'] += 1 # TODO :: count only legal cols?
      if sim.is_legal(col):
        try: sim.play(col, self.mark, sim=True)
        except GameTied: # already checked for win condition
          if 0 > ret['score']: ret['score'] = 0; ret['column'] = col
          break
        # let opponent play; store the negative of score
        opp_res = opp.solve(sim)
        ret['explored'] += opp_res['explored']
        score = (-1) * opp_res['score'] 
        if score >= beta: # found something better
          ret['score'] = score
          ret['column'] = col
          break
        if score > alpha: # reduce window size
          alpha = score
          ret['score'] = alpha
          ret['column'] = col # TODO :: is this right?
      del sim
    del opp
    return ret

class Random:
  def __init__(self, pos):
    self.pos = pos
    self.mark = MARKS[pos]
    self.retries = []

  def array_get(self, arr, i):
    try: return arr[i]
    except IndexError: return -1

  def in_loop(self, col, half):
    same = 0; i = 1
    while self.array_get(self.retries,-i) == col: 
      same += 1
      i += 1

    if same > half: 
      self.retries = []
      return True
    
    return False
  
  def play(self, game):
    col = random.randint(0,game.WIDTH-1)
    while not game.is_legal(col) or self.in_loop(col,game.HEIGHT//2):
      col = random.randint(0,game.WIDTH-1)
      self.retries.append(col)
    return col

class Deeper:
  pass