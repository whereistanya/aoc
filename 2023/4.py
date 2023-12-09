#!/usr/bin/env python3

VERBOSE = True
TEST = False

with open("input4.txt", "r") as f:
  lines = f.readlines()

example = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

if TEST:
  lines = example.strip().split("\n")

cardcounts = len(lines) * [1]

part1_total = 0

for i in range(len(lines)):
  line = lines[i]
  copies = cardcounts[i]
  (first, second) = tuple(line.strip().split(": ")[1].split(" | "))
  winners = set(first.strip().split())
  have = set(second.strip().split())
  winner_count = len(winners.intersection(have))
  if VERBOSE: print(winner_count)

  if winner_count > 0:
    for j in range(1, winner_count + 1):
      try:
        cardcounts [ i + j] += copies
      except IndexError:  # don't go off the end
        pass
    value = pow(2, winner_count - 1)
    part1_total += value

print(part1_total)
print(sum(cardcounts))
