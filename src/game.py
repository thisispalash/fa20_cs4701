from errors import OutsideBoard, ColumnFull, IllegalMove
from errors import GameTied, PlayerOneWins, PlayerTwoWins
from defaults import DIRS, MARKS

class Board:
  ''' The actual game implementation ;; 
    contains all game related functions
  '''

  def __init__(self, w, h):
    self.WIDTH = w; self.HEIGHT = h
    self.board = [[0] * w for _ in range(h)]
    self.full = [False] * w
    self._last = []

  def __str__(self):
    table = '\n  |'
    for i in range(self.WIDTH): table += ' ' + str(i) + ' |'
    table += '\n'
    for j in range(self.HEIGHT):
      num = (self.HEIGHT-1) - j # board stored upside down
      row = self.board[num] 
      table += str(num) + ' |'
      for x in row: table += ' _ |' if type(x) is int else ' '+x+' |'
      table += '\n'
    return table

  def is_legal(self, c, sim=True):
    if c < 0:
      raise OutsideBoard('Column numbers are not negative', sim)
    if c >= self.WIDTH:
      raise OutsideBoard('Column numbers are 0-indexed', sim)
    if self.full[c]:
      raise ColumnFull('Try a different column', sim)

  # raises `GameEnd` if tied after move at `c`
  def update(self, c, mark, sim=True):
    ''' first available empty row in c filled
      ==> board stored upside down '''
    for r in range(self.HEIGHT):
      if not self.board[r][c]: 
        self.board[r][c] = mark
        self._last.append((r,c))
        break
    if self.board[self.HEIGHT-1][c]: 
      self.full[c] = True
    if all(self.full): raise GameTied(self.__str__(), sim)

  def reset(self):
    self.board = [[0] *  self.WIDTH for _ in range(self.HEIGHT)]
    self.full = [False] * self.WIDTH
    self._last = []
    return self

  def undo(self):
    if not self._last: return # TODO raise exception
    r,c = self._last[-1]
    self.board[r][c] = 0
    if r == self.HEIGHT-1: self.full[c] = False
    self._last = self._last[:-1]

  # raises `GameEnd` if aligned, or tied
  def is_aligned(self, c, r=None, sim=True):
    if all(self.full): raise GameTied(self.__str__(), sim)
    if not r: r = self.get_last_row(c)
    if not self.board[r][c]: return
      # check for alignment in every direction only if there is a mark
    for d in DIRS: # BUG :: fix by starting at staring position
      count = self.get_seq_count(r,c,direction=d)
      # print(count)
      # print()
      if count >= 4: # TODO :: make connect-length variable
        seq = []
        for mul in range(count):
          i,j = d[1]; i*=mul; j*=mul
          seq.append((r+i,c+j))
        if MARKS.index(self.board[r][c]): # MARKS = ('x','o')
          raise PlayerTwoWins(seq, self.get_score(), self.__str__(), sim)
        else: raise PlayerOneWins(seq, self.get_score(), self.__str__(), sim)

  ## helper methods ##
  
  def get_score(self):
    left = (self.WIDTH*self.HEIGHT) - len(self._last)
    return (left+1)//2
    
  def is_inside(self, r, c):
    return ((r>=0 and r<self.HEIGHT) and 
      (c>=0 and c<self.WIDTH))

  def next_cell(self, r, c, tup):
    # tup = ('<dir>', (<row-upd>,<col-update))
    i,j = tup[1]
    return (r+i,c+j)

  def get_seq_count(self, r, c, count=1, direction=None):
    assert direction
    nr,nc = self.next_cell(r,c,direction)
    if not self.is_inside(nr,nc): return count
    if self.board[nr][nc] == self.board[r][c]:
      return self.get_seq_count(nr,nc,count+1,direction)
    return count
    
  def get_last_row(self, c):
    r = self.HEIGHT
    while r>=0:
      r-=1
      if self.board[r][c]: 
        return r
    return 0 # column is empty

  def get_legal_positions(self):
    valid_locations = []
    for c in range(self.WIDTH):
      if self.is_valid_location(c):
        valid_locations.append(c)
    return valid_locations

  def is_valid_location(self, c):
    try: self.is_legal(c)
    except IllegalMove: return
    else: return c