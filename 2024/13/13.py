#!/usr/bin/env python

import math
import re

from sympy import symbols, Eq, solve
from sympy.solvers.solveset import linsolve

filename = "input.txt"
#filename = "test1"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

class Game(object):
  def __init__(self, adx, ady, bdx, bdy, destx, desty):
    self.adx = adx
    self.ady = ady
    self.bdx = bdx
    self.bdy = bdy
    self.destx = destx
    self.desty = desty
    self.acost = 3
    self.bcost = 1

buttonRE = "Button (\w): X\+(\d+), Y\+(\d+)"
prizeRE = "Prize: X=(\d+), Y=(\d+)"

games = []
for line in lines:
  if line.startswith("Button A:"):
    groups = re.search(buttonRE, line).groups()
    ax, ay = int(groups[1]), int(groups[2])
  if line.startswith("Button B:"):
    groups = re.search(buttonRE, line).groups()
    bx, by = int(groups[1]), int(groups[2])
  if line.startswith("Prize:"):
    groups = re.search(prizeRE, line).groups()
    px, py = int(groups[0]), int(groups[1])
    games.append(Game(ax, ay, bx, by, px, py))


part1 = 0
part2 = 0
a, b = symbols('a, b')  # for sympy!

for game in games:
  # We've solving simultaneous equations!
  # Want to find a and b, how many times to press A, how many times to press B
  # a * adx + b * adx = destx
  # a * ady + b * ady = desty
  # so subtract dest from each to make them both equal to zero.
  solutions = (linsolve([game.adx * a + game.bdx * b - game.destx,
                         game.ady * a + game.bdy * b - game.desty], (a, b)))
  acount, bcount = min(solutions)
  if acount.is_integer and bcount.is_integer:
    part1 += acount * game.acost + bcount * game.bcost

  game.destx += 10000000000000
  game.desty += 10000000000000
  solutions = (linsolve([game.adx * a + game.bdx * b - game.destx,
                         game.ady * a + game.bdy * b - game.desty], (a, b)))
  acount, bcount = min(solutions)
  if acount.is_integer and bcount.is_integer:
    part2 += acount * game.acost + bcount * game.bcost

print("Part 1:", part1)
print("Part 2:", part2)
