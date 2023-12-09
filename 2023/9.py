#!/usr/bin/env python3

from itertools import pairwise

VERBOSE = True
TEST = True
TEST = False

with open("input9.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]

example = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

if TEST:
  lines = example.strip().split("\n")

total= 0
total2 = 0
for line in lines:
  initial_seq = [int(x) for x in line.strip().split()]

  step_count = 0
  finals = [initial_seq[-1]]
  firsts = [initial_seq[0]]
  seq = list(initial_seq)
  while sum(seq) != 0:
    seq = [ y - x for (x, y) in list(pairwise(seq)) ]
    finals.append(seq[-1])
    firsts.append(seq[0])
    step_count += 1
  total += sum(finals)

  end = 0
  for f in reversed(firsts):
    end = f - end
  total2 += end

print("Part 1", total)
print("Part 2", total2)

