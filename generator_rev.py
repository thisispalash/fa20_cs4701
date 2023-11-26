import os
import sys
import pprint

import defaults
from agents import Random
from state import State
from errors import IllegalMove, GameEnd

def main(num_tests, moves):

  players = (Random(0),Random(1))
  states = []
  game = State(defaults.WIDTH,defaults.HEIGHT)
  # stop_move = defaults.WIDTH*defaults.HEIGHT - back_move
  done = 0
  while done<num_tests:
    
    game = game.reset()
    current = None
    spree = 0
    while game.get_moves() != moves:
      if game.get_moves()%2: # if moves-done = 1,3,5..
        current = (players[1],defaults.MARKS[1])
      else: current = (players[0],defaults.MARKS[0])
      try: 
        # print('<',game.__repr__())
        # print('=',spree)
        game.play(current[0].play(game),current[1],True)
        print(game.__repr__())
      except GameEnd: 
        game.undo(); spree += 1
        if spree >= game.WIDTH:
          for _ in range(spree): game.undo()
      else: spree = 0
        
    states.append(game.get_state())
    done += 1

  return states

if __name__=='__main__':
  try:
    num_tests = sys.argv[1]
    moves = sys.argv[2]
    file_num = sys.argv[3]
  except: 
    print(' usage: $ python3 generator.py <num-tests> <back-moves> <file-num>')
    sys.exit()

  result = main(int(num_tests),int(moves))

  test_dir = os.path.join(os.path.join(os.getcwd(),'tests'),'in_rev')
  if not os.path.isdir(test_dir): os.mkdir(test_dir)

  out_dir = os.path.join(test_dir,moves)
  if not os.path.isdir(out_dir): os.mkdir(out_dir)

  with open(os.path.join(out_dir,'test'+file_num),'w+') as out_file:
    out_file.write('\n'.join(result))