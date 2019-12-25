#!/usr/bin/env python
# Advent of code Day 22.

import sys

def cut(n, deck):
  if n == 0: # TODO handle zero n
    raise ValueError
  p1 = deck[n:]
  p1.extend(deck[0:n])
  return p1

def incr(n, deck):
  tmp = [0] * len(deck)
  for i in range(len(deck)):
    tmp[(i * n) % len(deck)] = deck[i]
  return tmp

def shuffle(lines, deck):
  print "\n## Shuffling", len(deck)
  for line in lines:
    #print line
    line.strip()
    if line == "deal into new stack":
      deck.reverse()
    if line.startswith("deal with increment"):
      count = int(line.strip("deal with increment "))
      deck = incr(count, deck)
    if line.startswith("cut"):
      count = int(line.strip("cut "))
      deck = cut(count, deck)
  return deck

with open("input22.txt", "r") as f:
  lines = f.readlines()

## Tests
assert cut(3, [1,2,3,4,5,6]) == [4,5,6,1,2,3]
assert cut(1, [45,67,89]) == [67, 89, 45]
assert cut(-1, [1,2,3,4,5,6]) == [6,1,2,3,4,5]
assert cut(-3, [100,50,25,12,6,3,1]) == [6,3,1,100,50,25,12]
assert(incr(3, [0,1,2,3,4,5,6,7,8,9])) == [0,7,4,1,8,5,2,9,6,3]
assert(incr(7, [0,1,2,3,4,5,6,7,8,9])) == [0,3,6,9,2,5,8,1,4,7]

deck = []
for i in range(0, 10):
  deck.append(i)
assert shuffle([
  "deal with increment 7",
  "deal into new stack",
  "deal into new stack",
], deck) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]

deck = []
for i in range(0, 10):
  deck.append(i)
assert shuffle([
"cut 6",
"deal with increment 7",
"deal into new stack",
], deck) == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]

deck = []
for i in range(0, 10):
  deck.append(i)
assert shuffle([
"deal into new stack",
"cut -2",
"deal with increment 7",
"cut 8",
"cut -4",
"deal with increment 7",
"cut 3",
"deal with increment 9",
"deal with increment 3",
"cut -1",
], deck) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

deck = []
for i in range(0, 10):
  deck.append(i)
assert shuffle([
"deal with increment 7",
"deal with increment 9",
"cut -2",
], deck) == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]


## Main
deck = []
for i in range(0, 10007):
  deck.append(i)

deck = shuffle(lines, deck)
#print deck[0:80]
print deck.index(2019)

# 6780 too high
# 3226 too low

