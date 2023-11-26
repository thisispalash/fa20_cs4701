import os
import sys
import datetime
import multiprocessing as mp

import agents
import defaults

from play import PLAYERS
from state import State

out_file = None
done = 0

def read_tests(test_dir):

  tests = dict()

  for f in os.listdir(test_dir):
    if not f.startswith('test-01'): continue
    with open(os.path.join(test_dir,f)) as test_file:
      test = []; name = test_file.name.split('/')[-1]
      for case in test_file:
        test.append(case.strip())
      tests[name] = test
  
  return tests

def write_out(line):
  out_file.write(line + '\n')

def get_micro(delta):
  mic = 0
  if delta.microseconds: mic += delta.microseconds
  if delta.seconds: mic += delta.seconds * 1000 * 1000
  if delta.days: mic += delta.days * 24 * 60 * 60 * 1000 * 1000
  return mic

def worker(state,agent,game,score=None):
  start = datetime.datetime.now()
  solver = agent.solve(game)['score']
  delta = datetime.datetime.now()-start
  # try: assert solver == score # BP
  # except AssertionError as e:
  #   e.args += (state,solver,get_micro(delta))
  #   raise
  return (state,solver,get_micro(delta))

def callback(t):
  state = t[0]
  score = t[1]
  delta = t[2]/10**6
  write_out(str(state) + ' ' + str(score) + ' ' + str(delta) + 's')

def error_callback(e):
  state = e.args[0]
  score = e.args[1]
  delta = e.args[2]/10**6
  write_out('~e ' + str(state) + ' ' + str(score) + ' ' + str(delta) + 's')


if __name__ == '__main__':

  START = datetime.datetime.now()


  test_dir = os.path.join(os.getcwd(),'tests')
  res_dir = os.path.join(test_dir,'res')
  if not os.path.isdir(res_dir): os.mkdir(res_dir)

  curr_dir = datetime.datetime.now().strftime('%m%d-%H%M%S.')
  try: curr_dir += sys.argv[1]
  except:
    print(' usage: $ python3 benchmark_mp.py <agent-name>')
    print('  agents: ' + ','.join(PLAYERS.keys()))
    sys.exit()
  curr_dir = os.path.join(res_dir,curr_dir)
  os.mkdir(curr_dir)
  
  # TODO :: sys.argv
  timeout = 2
  nproc = 1
  
  tests = read_tests(os.path.join(test_dir,'files'))
  
  for test_file in tests:
    print(test_file)
    out_file = open(os.path.join(curr_dir,test_file), 'w+')
    
    for j in range(len(tests[test_file])):
      pool = mp.Pool(processes=nproc) # nproc = 1
      state = tests[test_file][j]
      agent = PLAYERS[sys.argv[1]](len(state)%2) # agent to move next turn
      game = State(defaults.WIDTH,defaults.HEIGHT,state)
      res = pool.apply_async(worker, args=(state,agent,game),
        callback=callback, error_callback=error_callback)
      done += 1
      print(' test-'+str(j))
    

    # out_file.close()
  
  # pool.close()
  # pool.join()

  delta = datetime.datetime.now() - START
  print(f'done {done} tests in {delta}')