#!/usr/bin/env python

import math

class Pattern(object):
  def __init__(self, initial, output):
    """Initialise a new pattern.
    Initial and output are strings, because that's how we get them from the puzzle
    input, but we turn them into 'rows', i.e., a list of strings.
    """
    matches = set() # set([str, ...])
    self.output = output.split("/")
    self.variants = [] # list of strings.
    input_rows = initial.split("/")
    self.make_variants(input_rows)

  def match(self, square):
    matchable = "".join(square)
    # print "Matching %s against\n%s" % (matchable, self.variants)
    if matchable in self.variants:
      return True
    return False

  def make_variants(self, pattern):
    """Create and store all variants of this pattern.

    Args:
      initial: ([str, ...])
    """
    for i in range(4):
      pattern = SquareChanger.rotate(pattern)
      self.variants.append("".join(pattern))
    pattern = SquareChanger.flip(pattern)
    for i in range(4):
      pattern = SquareChanger.rotate(pattern)
      self.variants.append("".join(pattern))


class SquareChanger(object):
  """Static methods to muck around with squares."""

  @staticmethod
  def flip(pattern):
    """Flip a pattern upside down.
      ["ab"
       "cd"]
      becomes
      ["cd",
       "ab"]

      Can handle patterns with 1-3 rows.
      Args:
        pattern: ([str, ...]) a square list of strings
      Returns:
        same, but flipped

    """
    if len(pattern) > 3:
      print ("BUG: Didn't expect a pattern this shape: %s" % pattern)
      exit()
    tmp = pattern[0]
    pattern[0] = pattern[-1]
    pattern[-1] = tmp
    return pattern

  @staticmethod
  def rotate(pattern):
    """
    This is a matrix rotation problem and if I was less lazy I would probably
    implement a matrix rotation algorithm but let the record show that I am
    exactly this lazy. Same args, philosophy as flip().
    """
    #print "Rotating", pattern
    newrows = []
    for i in range(len(pattern)):
      # turn columns into rows by creating new lists with the 1st element of
      # each row, then the 2nd, etc. [::-1] means we're starting with the last
      # row.
      newrows.append("".join([row[i] for row in pattern[::-1]]))
    return newrows

  @staticmethod
  def split(sq):
    print("Got a %d x %d square; splitting it." % (len(sq), len(sq[0])))
    rowcount = len(sq) # number of rows; width of initial square

    # 6x6 becomes 9 2x2 squares
    if rowcount <= 3:
      return [sq]
    if rowcount % 2 == 0:
      newsqlen = 2
    elif rowcount % 3 == 0:
      newsqlen = 3
    else:
      print("BUG: Unexpected square newsqlen %d" % rowcount)
      exit()
    sqsperrow = rowcount / newsqlen

    height = newsqlen # just for code clarity because this is confusing
    y = 0
    x = 0
    newsqs = []
    while y < rowcount:
      # calculate the N squares in this set of rows then move down
      while x < rowcount: # width here because it's a square
        newsq = []
        # calculate the square starting at this X then move right
        for i in range(newsqlen): # each row in the square
          #print i, "print appending", sq[y + i][x:x + newsqlen]
          newsq.append(sq[y + i][x:x + newsqlen])
        #print "Made a square", newsq
        newsqs.append(newsq)
        x += newsqlen
      y += height
      x = 0
    return newsqs

  @staticmethod
  def join(sqs):
    """
    Wow, I bet there's an easy way to do this, but I didn't find it.

    assert SquareChanger.join([["12", "56"], ["34", "78"],
                               ["9A", "DE"], ["BC", "FG"]]) == 
                               ["1234", "5678", "9ABC", "DEFG"]
    """
    print("Got %d squares of size %d, joining" % (len(sqs), len(sqs[0])))
    sqcount = len(sqs)  # How many squares
    if sqcount == 1:
      return sqs[0]
    sqlen = len(sqs[0]) # width of one input square
    sqperrow = int(math.sqrt(sqcount))
    rowcount = sqlen * sqperrow
    # print("We have", rowcount, "rows, working in batches of", sqlen, "with", sqperrow, "per row")
    grid = []  # [str, ...]

    y = 0
    sqno = 0 # iterate through the squares
    while y < rowcount:
      # operate on the next `sqlen` rows
      rows = [""] * sqlen
      # combine this row from the next N squares
      for j in range(sqlen): # this many rows
        for x in range(sqperrow): # this many squares across
          rows[j] += sqs[sqno + x][(y + j) % sqlen] # this row of the square
      sqno += sqperrow
      y += sqlen
      grid.extend(rows)
    return grid



class Grid(object):
  """A grid is a list of strings."""

  def __init__(self, initial):
    self.rules = [] # [Pattern, ...]
    self.grid = initial

  def __repr__(self):
    s = "\n"
    for row in self.grid:
      s += "%s\n" % row
    return s

  def set_rules(self, rules):
    for rule in rules:
      x, y = rule.strip().split(" => ")
      self.rules.append(Pattern(x, y))

  def run(self):
    new_squares = SquareChanger.split(self.grid)
    to_join = []
    for new_square in new_squares:
      matched = False
      for rule in self.rules:
        if rule.match(new_square):
          to_join.append(rule.output)
          matched = True
          break
      if not matched:
        print "BUG: didn't match:"
        print new_square
        exit()
    print ("Matched all of them. Now have %d of size %d" % (len(to_join),
                                                           len(to_join[0])))
    self.grid = SquareChanger.join(to_join)

  def count_on(self):
    count = 0
    for row in self.grid:
      for char in row:
        if char == "#":
          count += 1
    return count



def run_tests():
  assert SquareChanger.flip(["123", "456", "789"]) == [ "789", "456", "123"]
  assert SquareChanger.flip(["12", "34"]) == [ "34", "12"]
  assert SquareChanger.flip(["1",]) == [ "1"]
  assert SquareChanger.rotate(["123", "456", "789"]) == ["741", "852", "963"]
  assert SquareChanger.rotate(["12", "34"]) == ["31", "42"]
  assert SquareChanger.rotate(["1"]) == ["1"]

  assert SquareChanger.split(["1234", "5678", "9ABC", "DEFG"]) == [
                              ["12", "56"], ["34", "78"], ["9A", "DE"], ["BC", "FG"] ]
  assert SquareChanger.split(["000111222",
                              "000111222",
                              "000111222",
                              "333444555",
                              "333444555",
                              "333444555",
                              "666777888",
                              "666777888",
                              "666777888",]) == [
                                ["000", "000", "000"],
                                ["111", "111", "111"],
                                ["222", "222", "222"],
                                ["333", "333", "333"],
                                ["444", "444", "444"],
                                ["555", "555", "555"],
                                ["666", "666", "666"],
                                ["777", "777", "777"],
                                ["888", "888", "888"],
                              ]

  assert SquareChanger.join([["12", "56"], ["34", "78"],
                             ["9A", "DE"], ["BC", "FG"]]) == ["1234", "5678", "9ABC", "DEFG"]
  assert SquareChanger.join([
                                ["000", "000", "000"],
                                ["111", "111", "111"],
                                ["222", "222", "222"],
                                ["333", "333", "333"],
                                ["444", "444", "444"],
                                ["555", "555", "555"],
                                ["666", "666", "666"],
                                ["777", "777", "777"],
                                ["888", "888", "888"],
                              ]) == [
                              "000111222",
                              "000111222",
                              "000111222",
                              "333444555",
                              "333444555",
                              "333444555",
                              "666777888",
                              "666777888",
                              "666777888" ]
  print ("Tests passed.")


# main()
# Test lines
lines = [
  "../.# => ##./#../...",
  ".#./..#/### => #..#/..../..../#..#",
]


# Real lines
with open("input21.txt", "r") as f:
  lines = f.readlines()

run_tests()

# Starter
starter = [
  ".#.",
  "..#",
  "###",
]

iterations_to_run = 18  # 5 for part 1

grid = Grid(starter)
grid.set_rules(lines)

for i in range(iterations_to_run):
  grid.run()

#print ("Grid after %d: %s" % (i, grid))
print grid.count_on()
