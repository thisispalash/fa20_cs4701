import os
import sys
import pprint

import defaults
from agents import Random
from state import State
from errors import IllegalMove, GameEnd

def main(num_tests, back_move):

  players = (Random(0),Random(1))
  states = []
  game = State(defaults.WIDTH,defaults.HEIGHT)

  done = 0
  while done<num_tests:
    
    game = game.reset()
    current = None
    while True:
      if game.get_moves()%2: # if moves-done = 1,3,5..
        current = (players[1],defaults.MARKS[1])
      else: current = (players[0],defaults.MARKS[0])

      try: game.play(current[0].play(game),current[1],True)
      except GameEnd:
        for _ in range(back_move): game.undo()
        if not game.get_state(): continue # game reset while undo
        states.append(game.get_state())
        done += 1
        break

  return states

if __name__=='__main__':
  try:
    num_tests = sys.argv[1]
    back_move = sys.argv[2]
    file_num = sys.argv[3]
  except: 
    print(' usage: $ python3 generator.py <num-tests> <back-moves> <file-num>')
    sys.exit()

  result = main(int(num_tests),int(back_move))

  test_dir = os.path.join(os.path.join(os.getcwd(),'tests'),'in')
  if not os.path.isdir(test_dir): os.mkdir(test_dir)

  out_dir = os.path.join(test_dir,back_move)
  if not os.path.isdir(out_dir): os.mkdir(out_dir)

  with open(os.path.join(out_dir,'test'+file_num),'w+') as out_file:
    out_file.write('\n'.join(result))