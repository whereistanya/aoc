#!/usr/bin/env python
# Advent of code Day 14.

import math
import sys
from blist import blist

######################################
# This is part two. Part one got
# refactored out of existence.
######################################

class elf(object):
  def __init__(self):
    self.current_pos = 0
    self.current_value = 0

def combine(e1, e2, score):
  n = e1.current_value + e2.current_value
  if n == 0:
    scores.append(0)
    return 1
  #print "adding", n
  digits = math.floor(math.log10(n))
  added = int(digits) + 1   # jfc this is confusing

  while digits >= 0:
    first = int(n // (10 ** digits))
    scores.append(first)
    #print scores
    n -= first * 10 ** digits
    digits -= 1
  return added

def advance(e1, e2, scores):
  new_pos = (1 + e1.current_pos + e1.current_value)
  wrapped = new_pos % len(scores)
  e1.current_pos = wrapped
  e1.current_value = scores[wrapped]

  new_pos = (1 + e2.current_pos + e2.current_value)
  wrapped = new_pos % len(scores)
  e2.current_pos = wrapped
  e2.current_value = scores[wrapped]

e1 = elf()
e1.current_value = 3
e1.current_pos = 0
e2 = elf()
e2.current_value = 7
e2.current_pos = 1

scores = blist([])
scores.append(e1.current_value)
scores.append(e2.current_value)

#to_find = [5,9,4,1,4] # Should be 2018
#to_find = [5,1,5,8,9] # Should be 9
to_find = [7, 0, 2, 8, 3, 1]

l = len(to_find)

print(to_find)
print(scores)
while True:
  added = combine(e1, e2, scores)
  advance(e1, e2, scores)
  if added > 1:
    for i in range (1, added):
      if to_find == scores[-l -i: -i]:
        print(len(scores) - (l + i))
        sys.exit(0)
  if to_find == scores[-l:]:
    print(len(scores) - l)
    sys.exit(0)
