import sys

from state import State
from errors import GameEnd, IllegalMove

import agents
import defaults

PLAYERS = { # references to agents
  'human': agents.Human,
  'rando': agents.Random,
  'minim': agents.NegaMax,
  'alpha': agents.AlphaBeta,
  'omega': agents.Deeper
}

def select_players(count=0, types=[]):
  ''' Returns 2 player instances

    @param: count in {1,2}, the number of custom players
    @param: types, list of references to agents in str
  '''
  players = []
  for x in types:
    if x not in PLAYERS.keys():
      print('Invalid player type..')
      print('Available player types :: '
        + ', '.join(PLAYERS.keys()))
      sys.exit()
  if count == 2:
    players.append((PLAYERS[types[0]](0), 0))
    players.append((PLAYERS[types[1]](1), 1))
  elif count == 1:
    players.append((PLAYERS[types[0]](0), 0))
    players.append((PLAYERS['human'](1), 1))
  else: # default game
    players.append((PLAYERS['human'](0), 0))
    players.append((PLAYERS['human'](1), 1))
  return players

def cmd_help():
  print()
  print('--------------- connect4 help ---------------')
  print('default game: 7x6 board, Human vs Human')
  print('------------------- usage -------------------')
  print('HELP :')
  print('  $ python3 play.py help')
  print('GAME :')
  print('  $ python3 play.py [--debug]')
  print('             [-w <width> -h <height>]')
  print('             [-s <initial-state>]')
  print('             [-p <custom-players> <player1-type> <player2-type>]')
  print('------------- players available -------------')
  print(', '.join(PLAYERS.keys()))
  print('--------------- ------------- ---------------')
  print()
  sys.exit(0)

def process_flags(opt):
  ''' Processess command line flags
    @param: opt, sys.argv list, in lowercase
    Returns
      State(width,height,state), new State of the game
      players, 2 instances of agents
      debug, debug flag
  '''
  if any(x in opt for x in defaults.CMD_OPT['help']): cmd_help()

  def get_index_of(flag): # get index of option in cmd args
    for x in defaults.CMD_OPT[flag]:
      if x in opt: return opt.index(x)

  if any(x in opt for x in defaults.CMD_OPT['width']):
    width = int(opt[get_index_of('width')+1])
  else: width = defaults.WIDTH
  if any(x in opt for x in defaults.CMD_OPT['height']):
    height = int(opt[get_index_of('height')+1])
  else: height = defaults.HEIGHT
  
  if any(x in opt for x in defaults.CMD_OPT['init_state']):
    state = opt[get_index_of('init_state')+1]
    try: int(state)
    except ValueError:
      print('The state is the list of columns played in order')
      sys.exit()
  else: state = ''

  if any(x in opt for x in defaults.CMD_OPT['players']):
    index = get_index_of('players')
    count = int(opt[index+1]); assert count in {1,2}
    index += 2 # move to player types
    players = select_players(count, opt[index:index+count])
  else: players = select_players()

  if any(x in opt for x in defaults.CMD_OPT['debug']): debug = True
  else: debug = False

  return State(width,height,state),players,debug

def print_state(game):
  print(game); done = game.get_moves()
  print('player :: ' + str(done%2+1))
  print('move number :: ' + str(done//2+1))

def cleanup():
  print('Goodbye.')

## end helpers ##

def play(game, players, debug=False):
  current = None
  while(True):
    print_state(game)
    if debug: _ = input('press enter to continue: ')
    if game.get_moves()%2: # if moves-done = 1,3,5..
      current = players[1]
    else: current = players[0]
    while(True): # enter the right move hooman!
      try: game.play(current[0].play(game), defaults.MARKS[current[1]]) # TODO this defaults.MARKS implementation is ugly
      except GameEnd: return
      except IllegalMove: continue
      else: break

if __name__ == '__main__':
  s,p,d = process_flags([x.lower() for x in sys.argv])
  play(s,p,d)
  cleanup()
