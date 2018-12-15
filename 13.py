#!/usr/bin/env python
# Advent of code Day 13

import sys

class Cart(object):
  def __init__(self, x, y, next_move):
    self.x = x
    self.y = y
    self.next_move = next_move # up, down, left, right
    self.next_decision = "left" # left, straight, right
    self.active = True

  def __lt__(self, other):
    """For sorting."""
    if self.y < other.y:
      return True
    if self.y > other.y:
      return False
    return self.x < other.x

  def change_direction(self, symbol):
    # if symbol is | or -, cart direction stays the same
    if symbol in ["|", "-"]:
      return

    # if symbol is \ or /, cart goes around a curve
    if symbol == "\\":
      if self.next_move in ["up", "down"]:
        self._turn_anticlockwise()
      else:
        self._turn_clockwise()

    if symbol == "/":
      if self.next_move in ["up", "down"]:
        self._turn_clockwise()
      else:
        self._turn_anticlockwise()

    # If symbol is +, cart chooses a direction
    if symbol == "+":
      if self.next_decision == "straight": # go straight
        self.next_decision = "right"
      elif self.next_decision == "left": # turn left, not go left
        self.next_decision = "straight"
        self._turn_anticlockwise()
      elif self.next_decision == "right":
        self.next_decision = "left"
        self._turn_clockwise()

  def _turn_clockwise(self):
    turn = {
      "right": "down",
      "left": "up",
      "up": "right",
      "down": "left",
    }
    self.next_move = turn[self.next_move]

  def _turn_anticlockwise(self):
    turn = {
      "right": "up",
      "left": "down",
      "up": "left",
      "down": "right",
    }
    self.next_move = turn[self.next_move]

  def __repr__(self):
    return "Cart:(%d,%d %s)" % (self.x, self.y, self.next_move)

class Grid(object):
  """Some sugar around a list of lists."""
  def __init__(self, lines):
    self.grid = []  # [y][x]
    self.carts = []
    self.current_locations = {}  # (x, y): Cart
    cart_symbols = set(["v", "^", "<", ">"])
    for line in lines:
      row = []
      for char in line:
        if char in cart_symbols:
          next_move = self._get_next_move(char)
          cart = Cart(len(row), len(self.grid), next_move)
          self.current_locations[(len(row), len(self.grid))] = cart
          self.carts.append(cart)
          char = "-"  # "|" and "-" are interchangable, except to human eyes
        else:
          assert char in [" ", "|", "-", "\\", "/", "+", "\n"]
        row.append(char)
      self.grid.append(row)

  def __repr__(self):
    s = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    for row in self.grid:
      for item in row:
        s += item
      s += "\n"
    s += "Carts at %s\n" % self.carts
    s += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    return s

  def move(self):
    # Part 2: only one cart left.
    if len(self.current_locations) == 1:
      print self.current_locations
      sys.exit(1)
    for cart in sorted(self.carts):
      if not cart.active:
        continue
      x = cart.x
      y = cart.y
      self.current_locations.pop((x, y))
      move = cart.next_move

      # Expect good data; crash if moves don't exist
      if move == "down":
        symbol = self.grid[y + 1][x]
        cart.y = y + 1
      elif move == "up":
        symbol = self.grid[y - 1][x]

        if symbol not in ["|", "-", "\\", "/", "+"]:
          sys.exit(1)
        cart.y = y - 1
      elif move == "left":
        symbol = self.grid[y][x - 1]
        cart.x = x - 1
      elif move == "right":
        symbol = self.grid[y][x + 1]
        cart.x = x + 1
      else:
        print "move shouldn't be", move

      if (cart.x, cart.y) in self.current_locations.keys():
        print "crash at %d,%d" % (cart.x, cart.y)
        other_cart = self.current_locations.pop((cart.x, cart.y))

        cart.active = False
        other_cart.active = False
      else:
        self.current_locations[(cart.x, cart.y)] = cart
      cart.change_direction(symbol)

  def _get_next_move(self, symbol):
    directions = {
      "^": "up",
      "v": "down",
      ">": "right",
      "<": "left",
    }
    # Crash on bad symbol is fine here.
    return directions[symbol]


with open("day13input.txt", "r") as f:
  lines = f.readlines()

"""
lines = [ # Adding spaces at the end for https://docs.python.org/3/faq/design.html#why-can-t-raw-strings-r-strings-end-with-a-backslash
  r"/->-\ ",
  r"|   |  /----\ ",
  r"| /-+--+-\  | ",
  r"| | |  | v  | ",
  r"\-+-/  \-+--/ ",
  r"\------/ ",
 ]
#"""

"""
lines = [
  "/--->>---\\",
  "^        |",
  "\--------/",
]
"""

grid = Grid(lines)
print sorted(grid.carts)

while True:
# Run until crash
  grid.move()
