import os
import sys
import datetime
import multiprocessing as mp

import agents
import defaults

from play import PLAYERS
from state import State

def read_tests(in_dir):
  tests = dict()
  for f in os.listdir(in_dir):
    with open(os.path.join(in_dir,f)) as test_file:
      test = []; name = test_file.name.split('/')[-1]
      for case in test_file:
        test.append(case.strip())
      tests[name] = test
  return tests

def get_micro(delta):
  mic = 0
  if delta.microseconds: mic += delta.microseconds
  if delta.seconds: mic += delta.seconds * 1000 * 1000
  if delta.days: mic += delta.days * 24 * 60 * 60 * 1000 * 1000
  return mic

def job(d, j, agent, game):
  start = datetime.datetime.now()
  solver = agent.solve(game)
  delta = datetime.datetime.now()-start
  with mp.Lock():
    t = d[j]
    t['score'] = solver['score']
    t['delta'] = get_micro(delta)
    t['nodes'] = solver['explored']
    d[j] = t


if __name__ == '__main__':

  try: 
    agent_key = sys.argv[1]
    assert agent_key in PLAYERS.keys()
    moves = sys.argv[2]
  except: # TODO use flags
    print(' usage: $ python3 benchmark.py <agent-name> <moves> (<timeout>) (<debug>) (<log>)')
    print('  agents: ' + ','.join(PLAYERS.keys()))
    sys.exit()

  test_dir = os.path.join(os.getcwd(),'tests')
  in_dir = os.path.join(test_dir,'in_rev')
  out_dir = os.path.join(test_dir,'out_rev')
  if not os.path.isdir(out_dir): os.mkdir(out_dir)

  curr_dir = os.path.join(out_dir,agent_key)
  if not os.path.isdir(curr_dir): os.mkdir(curr_dir)
  curr_dir = os.path.join(curr_dir,moves)
  if not os.path.isdir(curr_dir): os.mkdir(curr_dir)

  try: timeout = int(sys.argv[3])
  except: timeout = 2
  try: log = sys.argv[5]
  except: log = False
  if log: mp.log_to_stderr(logging.DEBUG)
  
  tests = read_tests(os.path.join(in_dir,moves))
  total = 0
  START = datetime.datetime.now()

  for test_file in tests:
    if "debug=False" not in sys.argv: 
      print('---------',test_file)
    done = 0
    with open(os.path.join(curr_dir,test_file), 'w+') as out_file:
      out_file.write('!--<state> <score> <time> <nodes>\n')
      manager = mp.Manager()
      procs = []; d = manager.dict()
      for j in range(len(tests[test_file])):
        state = tests[test_file][j]
        agent = PLAYERS[agent_key](len(state)%2) # agent to move next turn
        game = State(defaults.WIDTH,defaults.HEIGHT,state)
        d[j] = {'state':state, 'score':None, 'delta':None, 'nodes':None}
        p = mp.Process(target=job, args=(d,j,agent,game,))
        p.start(); procs.append(p)
      
      # kill all child procs
      # TODO :: make async
      killed = 0 
      for p in procs: 
        p.join(timeout) 
        if p.is_alive():
          p.terminate()
          killed += 1
        done += 1
      
      time = tnodes = 0
      for key in d.copy():
        state = d[key]['state']
        score = d[key]['score']
        delta = d[key]['delta']
        nodes = d[key]['nodes']
        if delta: time += delta
        else: time += timeout*10**6 # microseconds
        if nodes: tnodes += nodes
        out_file.write(str(state) + ' ' + str(score) 
          + ' ' + str(delta) + ' ' + str(nodes) + '\n')
      out_file.write(
        '-!-moves ' + str(moves) + '\n' + 
        '-!-timeout ' + str(timeout) + '\n' + 
        '-!-tests ' + str(done) + '\n' + 
        '-!-killed ' + str(killed) + '\n' + 
        '-!-seconds ' + str(time/10**6) + '\n' + 
        '-!-explored ' + str(tnodes))
      if log: print(d[x] for x in d.copy())
    if "debug=False" not in sys.argv:
      print('-----------elapsed:',datetime.datetime.now()-START)
    total += done

  DELTA = datetime.datetime.now() - START
  if "debug=False" not in sys.argv:
    print(f'done {total} tests in {DELTA}')