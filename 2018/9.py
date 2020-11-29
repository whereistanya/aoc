#!/usr/bin/env python
# Advent of code Day 9.

from blist import blist

players = 447
last_marble = 7151000

marbles = blist([0, 1])
current = 1

scores = {}
for i in range(0, players):
  scores[i] = 0

for i in range (2, last_marble + 1):
  if i % 23 == 0:
    pos = current - 7
    if pos < 0:
      pos = pos % len(marbles)

    removed = marbles.pop(pos)
    scores[i % players] += i
    scores[i % players] += removed
    current = pos

  else:
    pos = (current + 2)
    if pos > len(marbles):
      pos = pos % len(marbles)

    marbles.insert(pos, i)
    current = pos

print(sorted(scores.values())[-1])
