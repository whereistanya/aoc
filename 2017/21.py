#!/usr/bin/env python

import math

class Square(object):
  """A Square is represented as a list of strings, like this:
    [ ".#.",
      "...",
      "###",
    ]
    Each character is a pixel, which may be on ("#") or off (".")
  """
  def __init__(self, rows):
    self.rows = rows  # [ str, ...]
    self.width = len(rows[0])

  def count_on(self):
    count = 0
    for row in self.rows:
      for char in row:
        if char == "#":
          count += 1
    return count

  def __repr__(self):
    s = ""
    for i in range(self.width):
      s += "%s\n" % (self.pattern[i * self.width: i * self.width + self.width])
    return s

class Pattern(Square):
  def __init__(self, initial, output):
    """Initialise a new pattern.
    Initial and output are strings, because that's how we get them from the puzzle
    input, but we turn them into 'rows', i.e., a list of strings.
    """
    matches = set() # set([str, ...])
    self.output = output
    self.variants = set() # set of strings
    #self.make_variants(initial)

  def match(self, square):
    # Not awesome to do this string wrangling, but nice to check set
    # membership and can't do that for lists.
    matchable = "".join(square)
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
      #self.add_string_variant()
    pattern = SquareChanger.flip(pattern)
    for i in range(4):
      pattern = SquareChanger.rotate(pattern)
      #self.add_string_variant()


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
    newrows = []
    for i in range(len(pattern)):
      # turn columns into rows by creating new lists with the 1st element of
      # each row, then the 2nd, etc. [::-1] means we're starting with the last
      # row.
      newrows.append("".join([row[i] for row in pattern[::-1]]))
    return newrows

  @staticmethod
  def split4(square):
    """Returns this square split in 4, or None if it's not at least 4 wide.
     row0   00 01 | 02 03
     row1   04 05 | 06 07
        -----   -----
     row2   08 09 | 10 11
     row3   12 13 | 14 15

    Returns([Square, Square, ...] where each square is 2x2
    """
    pass
    """
    p = self.pattern
    if self.width % 4 != 0:
      print "Can't split: width is", self.width
      return None
    new_square = [
      Square(p[0] + p[1] + p[4] + p[5]),
      Square(p[2] + p[3] + p[6] + p[7]),
      Square(p[8] + p[9] + p[12] + p[13]),
      Square(p[10] + p[11] + p[14] + p[15]),
    ]
    return new_square
    """

  @staticmethod
  def split9(square):
    """Returns this square split in 9, or None if it's not at least 9 wide.

    row0 00 01 02 | 03 04 05 | 06 07 08 |
    row1 09 10 11 | 12 13 14 | 15 16 17 |
    row2 18 19 20 | 21 22 23 | 24 25 26 |
         -------- | -------- | --------
    row3 27 28 29 | 30 31 32 | 33 34 35 |
    row4 36 37 38 | 39 40 41 | 42 43 44 |
    row5 45 46 47 | 48 49 50 | 51 52 53 |
         -------  | -------- | --------
    row6 54 55 56 | 57 58 59 | 60 61 62 |
    row7 63 64 65 | 66 67 68 | 69 70 71 |
    row8 72 73 74 | 75 76 77 | 78 79 80 |
  Returns([Square, Square, ...] where each square is 3x3
  """
    pass
    """
    p = self.pattern
    if self.width % 9 != 0:
      print "Can't split: width is", self.width
      return None
    new_square = [
      #Square("".join[p[00], p[01], p[02], p[09], p[10], p[11], p[18], p[19], p[20]]),
      #Square("".join[p[03], p[04], p[05], p[12], p[13], p[14], p[21], p[22], p[23]]),
      #Square("".join[p[06], p[07], p[08], p[15], p[16], p[17], p[24], p[25], p[26]]),
#
#      Square("".join[p[27], p[28], p[29], p[36], p[37], p[38], p[45], p[46], p[47]]),
#      Square("".join[p[30], p[31], p[32], p[39], p[40], p[41], p[48], p[49], p[50]]),
#      Square("".join[p[33], p[34], p[35], p[42], p[43], p[44], p[51], p[52], p[53]]),
#
#      Square("".join[p[54], p[55], p[56], p[63], p[64], p[65], p[72], p[73], p[74]]),
#      Square("".join[p[57], p[58], p[59], p[66], p[67], p[68], p[75], p[76], p[77]]),
#      Square("".join[p[60], p[61], p[62], p[69], p[70], p[71], p[78], p[79], p[80]]),
    ]
    return new_square
  """

  @staticmethod
  def split(square):
    print("Got square of %d x %d, splitting") % (self.width, self.width)
    pass
    """
    if self.width == 2:
      return [self]
    if self.width == 3:
      return [self]
    if self.width == 4:
      return split4()
    if self.width == 9:
      return split9()
    print "BUG: Unexpected width:", self.width
    exit()
    return None
    """


class Grid(object):
  """A grid is a 2D array of squares, like this:

  [
    [ Square, Square, Square, ],
    [ Square, Square, Square, ],
    [ Square, Square, Square, ],
  ]
  Each square has rows inside.
  """

  def __init__(self, initial):
    self.squares = [[ Square(initial) ]] # [ [ Square, ...], [Square, ...] ]  # in rows
    self.rules = [] # [Pattern, ...]

  def set_rules(self, rules):
    for rule in rules:
      x, y = rule.strip().replace("/", "").split(" => ")
      self.rules.append(Pattern(x, y))

  def run(self):
    print "Starting iteration %d with %d squares" % (iteration, len(self.squares))
    next_squares = []
    # TODO: understand the expected size of the new grid and initialise it with
    # Nones or something, so we can put the new squares in in place.

    for row in self.squares:
      for square in row:
        print "Processing square of width", square.width
        # divide into 2x2 or 3x3 squares
        new_squares = square.split()  # [Square, ...]

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
      # TODO: Put the new squares in their place in the new grid
      # TODO: Then, if needed, rebalance the grid.


# main()
# Test lines
lines = [
  "../.# => ##./#../...",
  ".#./..#/### => #..#/..../..../#..#",
]

# Real lines
with open("input21.txt", "r") as f:
  lines = f.readlines()

# Starter
starter = [
  ".#.",
  "..#",
  "###",
]

iteration = 1
grid = Grid(starter)
grid.set_rules(lines)

assert SquareChanger.flip(["123", "456", "789"]) == [ "789", "456", "123"]
assert SquareChanger.flip(["12", "34"]) == [ "34", "12"]
assert SquareChanger.flip(["1",]) == [ "1"]
assert SquareChanger.rotate(["123", "456", "789"]) == ["741", "852", "963"]
assert SquareChanger.rotate(["12", "34"]) == ["31", "42"]
assert SquareChanger.rotate(["1"]) == ["1"]
print ("Tests passed.")


# 125 too low
# 292 too high.
