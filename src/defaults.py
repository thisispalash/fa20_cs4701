WIDTH = 7 # 5 or 7 for it is a tie (https://tromp.github.io/c4/c4.html)
HEIGHT = 6

MIN_SCORE = -(WIDTH*HEIGHT//2 - 3) # cuz connect 4 and 7 move game
MAX_SCORE = (WIDTH*HEIGHT+1)//2 - 3 # `+1` for odd cells

MARKS = ('x','o')

DIRS = [ # ('<dir>', (<row-upd>,<col-update))
  ('N',(-1,0)), 
  ('NE',(-1,1)), 
  ('E',(0,1)), 
  ('SE',(1,1)), 
  ('S',(1,0)), 
  ('SW',(1,-1)), 
  ('W',(0,-1)), 
  ('NW',(-1,-1))
] # N/S reversed as board implemented upside down

CMD_OPT = {
  'help': ['help'],
  'width': ['-w', '--width'],
  'height': ['-h', '--height'],
  'init_state': ['-s', '--init', '--start'],
  'players': ['-p', '--players'],
  'debug': ['-d', '--debug']
}




# TODO bitboard stuff

MAX_SIZE = WIDTH * HEIGHT

from math import log
'''
  MAX_SIZE :: one bit per cell
  WIDTH :: one bit per col to 
  CURRENT_PLAYER :: one bit for move
  log(MAX_SIZE,2) :: number of bits to store move_num
'''
BIT_SIZE = MAX_SIZE + WIDTH + 1 + log(MAX_SIZE, 2) 