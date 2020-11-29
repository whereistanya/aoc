#!/usr/bin/env python
# Advent of code Day 12

import re
import sys

# Set up the patterns to match against
line_re = "(.....) => (.)"

with open("day12input.txt", "r") as f:
  initial = f.readline().split(": ")[1].strip()
  lines = f.readlines()

"""
initial = "#..#.#..##......###...###"
lines = [
	"...## => #",
	"..#.. => #",
	".#... => #",
	".#.#. => #",
	".#.## => #",
	".##.. => #",
	".#### => #",
	"#.#.# => #",
	"#.### => #",
	"##.#. => #",
	"##.## => #",
	"###.. => #",
	"###.# => #",
	"####. => #",
]
"""

patterns = {}
for line in lines:
  if line == "\n":
    continue
  line.strip()
  groups = re.search(line_re, line).groups()
  if len(groups) != 2:
    print("error in", line)
    continue
  match, out = groups
  patterns[match] = out

# Set up the pots, with a whole lot of empties before and after

pots = []
for char in initial:
  pots.append(char)
pot_zero = len(pots) / 2
pots = ["."] * pot_zero + pots + ["."] * pot_zero
#print ''.join(pots)[pot_zero - 5: 170]

# Run the generations
def do_generation(pots, gen):
  if '#' in pots[-10:]:
    pots = pots + ["."] * 20
  pot_str = ''.join(pots)
  new_pots = ["."] * len(pots)
  for i in range(0, len(pot_str)):
    s = pot_str[i - 2: i + 3]

    if s in patterns:
      new_pots[i] = patterns[s]

  return new_pots

for i in range(0, 128):
  pots = do_generation(pots, i)

# After 128 generations, the pattern settles into an equilibrium: (gen-26) leading
# dots, then two on, three off for  iterations

for gen in range(128, 1001):
  pots = do_generation(pots, gen)

# first way to calculate
  total = 0
  i = 0 - pot_zero
  for pot in pots:
    if pot == "#":
      total += i
    i += 1

# second way to calculate
  second_total = 0
  leading_dots = 0
  for pot in pots[pot_zero:]:
    if pot == r".":
      leading_dots += 1
    else:
      break
  assert leading_dots == gen - 26
  plant = leading_dots
  for i in range(0, 26):
    second_total += 2 * plant + 1
    plant += 5
  assert total == second_total

# Having ascertained that the fast way works as well as the slow way...

total = 0
# because I worked out the algorithm for a loop that ended in N and oh well it works
gen = 50000000000
gen -= 1 
plant = gen - 26
for i in range(0, 26):
  total += 2 * plant + 1
  plant += 5
print(total)
