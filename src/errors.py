class IllegalMove(Exception):
  ''' Base class for all illegal moves by player '''
  def __init__(self, msg):
    print(msg)

class OutsideBoard(IllegalMove):
  ''' Column selected is <0 or >=WIDTH '''
  def __init__(self, msg, sim):
    if not sim: super().__init__(msg)

class ColumnFull(IllegalMove):
  ''' Column selected is already full '''
  def __init__(self, msg, sim):
    if not sim: super().__init__(msg)


class GameEnd(Exception):
  ''' Base Class for Game End '''
  def __init__(self, score, board):
    print()
    print('---------- final board ----------')
    print(board)
    if score: print('winning score :: ' + str(score))
    
class PlayerOneWins(GameEnd):
  def __init__(self, seq, score, board, sim):
    if sim: return
    super().__init__(score, board)
    print('Player 1 WINS !!!')
    print('winning sequence :: ' + ''.join(str(seq)))

class PlayerTwoWins(GameEnd):
  def __init__(self, seq, score, board, sim):
    if sim: return
    super().__init__(score, board)
    print('Player 2 WINS !!!')
    print('winning sequence :: ' + ''.join(str(seq)))

class GameTied(GameEnd):
  def __init__(self, board, sim):
    if sim: return
    super().__init__(0, board)
    print('the board is full,\n the game is tied\n  good game, well played..')