def xor(tab1, tab2):
  y = len(tab1)
  x = len(tab1[0])
  # TODO :: the cool python way - [[x^y for x,y in row1,row2] for row1,row2 in tab1,tab2]
  res = [[0] * x] * y
  for i in range(x):
    for j in range(y):
      res[i][j] = tab1[i][j] ^ tab2[i][j]
  return res