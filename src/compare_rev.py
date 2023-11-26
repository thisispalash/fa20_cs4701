import os
import sys

from play import PLAYERS

import pprint

def read_tests(in_dir):
  tests = dict()
  for f in os.listdir(in_dir):
    with open(os.path.join(in_dir,f)) as test_file:
      test = []; name = test_file.name.split('/')[-1]
      for case in test_file:
        test.append(case.strip())
      tests[name] = test
  return tests

def read_results(out_dir):
  results = dict()
  for f in os.listdir(out_dir):
    with open(os.path.join(out_dir,f)) as the_file:
      res = []; name = the_file.name.split('/')[-1]
      results[name] = dict()
      for line in the_file:
        if line.startswith('!--'): continue # comments
        elif line.startswith('-!-'): # stats
          key,val = line.split()
          key = key[len('-!-'):]
          try: results[name][key] = int(val)
          except ValueError: 
            results[name][key] = int(float(val) * 10**6)
        else: # individual test-results
          state,score,delta,nodes = line.split()
          try: score = int(score)
          except: score = None
          try: delta = int(delta)
          except: delta = None
          try: nodes = int(nodes)
          except: nodes = None
          res.append((state,score,delta,nodes))
      results[name]['results'] = res
  return results
        

if __name__=='__main__':

  test_dir = os.path.join(os.getcwd(),'tests')
  in_dir = os.path.join(test_dir,'in_rev')
  out_dir = os.path.join(test_dir,'out_rev')

  try: log = sys.argv[1]
  except: log = False

  tests = dict()
  for back_move in os.listdir(in_dir):
    read_dir = os.path.join(in_dir,back_move)
    if not os.path.isdir(read_dir): continue
    tests[back_move] = read_tests(read_dir)

  results = dict()
  for agent in PLAYERS.keys():
    agent_dir = os.path.join(out_dir,agent)
    if not os.path.isdir(agent_dir): continue
    results[agent] = dict()
    for f in os.listdir(agent_dir):
      results[agent][f] = read_results(os.path.join(agent_dir,f))

  if log:
    pprint.pprint(results, depth=4)
    pprint.pprint(results, depth=3)
    pprint.pprint(results, depth=2)
    pprint.pprint(results, depth=1)
    # pprint.pprint(tests, depth=3) ~ max_depth
    pprint.pprint(tests, depth=2)
    pprint.pprint(tests, depth=1)
