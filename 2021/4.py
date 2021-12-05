#!/usr/bin/env python

inputfile = "input.txt"
with open(inputfile, "r") as f:
  values = f.readline().strip()
  lines = [x.strip() for x in f.readlines()]


class Grid(object):
  def __init__(self, lines):
    self.lines = lines
    self.rows = []  # list of sets
    self.grid = []
    for line in lines:
      self.grid.append([int(x) for x in line.split()])

    self.lookup = set() # duplicating the rows, ugh

    # Add a row for each line
    for line in self.grid:
      row = set()
      for number in line:
        row.add(number)
        self.lookup.add(number)
      self.rows.append(row)

    # Add each column
    for i in range(len(self.grid)):
      row = set()
      for line in self.grid:
        row.add(line[i])
        self.lookup.add(line[i])
      self.rows.append(row)

  def unmarked(self):
    score = 0
    for number in self.lookup:
      score += number
    return score

  def run_bingo(self, value_str):
    value = int(value_str)
    for row in self.rows:
      if value in row:
        row.remove(value)
        try:
          self.lookup.remove(value)
        except KeyError:
          pass
        if not row:  # it's empty
          score = self.unmarked() * value
          return True, score
    return False, 0


  def __repr__(self):
    return "|".join(self.lines)

#lines = """22 13 17 11  0
# 8  2 23  4 24
#21  9 14 16  7
# 6 10  3 18  5
# 1 12 20 15 19
#
# 3 15  0  2 22
# 9 18 13 17  5
#19  8  7 25 23
#20 11 10 24  4
#14 21 16 12  6
#
#14 21 17 24  4
#10 16 15  9 19
#18  8 23 26 20
#22 11 13  6  5
# 2  0 12  3  7""".split("\n")
#values = "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1"



grids = []
grid = []
for line in lines:
  if line == "":
    if len(grid) > 0:
      grids.append(Grid(grid))
      grid = []
  else:
    grid.append(line)
if grid:
  grids.append(Grid(grid))

never_won = set(grids)

for value in values.split(","):
  for grid in grids:
    win, score = grid.run_bingo(value)
    if win:
      if grid in never_won:
        print("First win for %s! %d" % (grid, score))
        never_won.remove(grid)
      if not never_won: #empty
        exit()

answer = None
print ("Answer is:", answer)
