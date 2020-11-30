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
    self.variants = [] # list of lists of strings.
    self.initial = initial
    input_rows = initial.split("/")
    self.make_variants(input_rows)

  def match(self, square):
    # it'd be nice if variants was a set but you can't hash lists and the number
    # of variants is small so we'll survive.
    print "Matching %s against\n%s" % (square, self.variants)
    if square in self.variants:
      return True
    return False


  def make_variants(self, pattern):
    """Create and store all variants of this pattern.

    Args:
      initial: ([str, ...])
    """
    for i in range(4):
      pattern = SquareChanger.rotate(pattern)
      self.variants.append(pattern)
    pattern = SquareChanger.flip(pattern)
    for i in range(4):
      pattern = SquareChanger.rotate(pattern)
      self.variants.append(pattern)
    print ("Variants of %s are %s" % (self.initial, self.variants))


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
    print "Rotating", pattern
    newrows = []
    for i in range(len(pattern)):
      # turn columns into rows by creating new lists with the 1st element of
      # each row, then the 2nd, etc. [::-1] means we're starting with the last
      # row.
      newrows.append("".join([row[i] for row in pattern[::-1]]))
    return newrows

  @staticmethod
  def split(sq):
    # TODO: sqlen and width probably should be swapped. Confusing names.
    print("Got square of %d x %d, splitting" % (len(sq), len(sq[0])))
    sqlen = len(sq)
    if sqlen <= 3:
      return [sq]
    if sqlen % 2 == 0:
      width = sqlen / 2
    elif sqlen % 3 == 0:
      width = sqlen / 3
    else:
      print("BUG: Unexpected square width %d" % sqlen)
      exit()

    height = width # just for code clarity because this is confusing
    y = 0
    x = 0
    newsqs = []
    while y < sqlen:
      # calculate the N squares in this set of rows then move down
      while x < sqlen:
        newsq = []
        # calculate the square starting at this X then move right
        for i in range(width): # each row in the square
          newsq.append(sq[y + i][x:x + width])
        newsqs.append(newsq)
        x += width
      y += height
      x = 0
    print("Turned %s into %s" % (sq, newsqs))
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
    sqlen = len(sqs[0]) # width of one input square
    gridlen = len(sqs)  # width of the output square
    grid = []  # [str, ...]

    y = 0
    sqno = 0 # iterate through the squares
    while y < gridlen: # operate on the next `sqlen` rows
      rows = [""] * sqlen
      # combine this row from the next N squares
      for j in range(sqlen): # this many rows
        print("Creating row", y + j)
        for x in range(sqlen): # this many squares across
          rows[j] += sqs[sqno + x][(y + j) % sqlen] # this row of the square
      sqno += sqlen
      y += sqlen
      grid.extend(rows)
    return grid



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
      x, y = rule.strip().split(" => ")
      self.rules.append(Pattern(x, y))

  def run(self):
    next_squares = []
    # TODO: understand the expected size of the new grid and initialise it with
    # Nones or something, so we can put the new squares in in place.

    for row in self.squares:
      for square in row:
        print "Processing square of width", square.width
        # divide into 2x2 or 3x3 squares
        new_squares = SquareChanger.split(square.rows)  # return a list of lists of strings;
                                      #  should use Squares instead.
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
      grid = SquareChanger.join(to_join)
      # TODO: Put the new squares in their place in the new grid
      # TODO: Then, if needed, rebalance the grid.


# main()
# Test lines
lines = [
  "../.# => ##./#../...",
  ".#./..#/### => #..#/..../..../#..#",
]

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



# Real lines
# with open("input21.txt", "r") as f:
#  lines = f.readlines()

# Starter
starter = [
  ".#.",
  "..#",
  "###",
]

grid = Grid(starter)
grid.set_rules(lines)
grid.run()
print "Grid after 1:", grid

# 125 too low
# 292 too high.
