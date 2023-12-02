#!/usr/bin/env python3

VERBOSE = True
TEST = False

import functools
import operator

with open("input2.txt", "r") as f:
  lines = f.readlines()

example = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

if TEST:
  lines = example.strip().split("\n")

def parse(line):
  first, second = line.strip().split(":")
  name = int(first.strip().split()[1])
  all_groups = []
  subsets = second.strip().split(";")
  for subset in subsets:
    colorgroups = [ (y, int(x))
      for x,y in (s.split()
        for s in subset.strip().split(",")) ]
    all_groups.append(colorgroups)
  return (name, all_groups)


# Part 1: Determine which games would have been possible if the bag had been
# loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes.

# Part 2: what is the fewest number of cubes of each color that could
# have been in the bag to make the game possible?
bag = { "red": 12, "green": 13, "blue": 14 }

part1 = 0
part2 = 0

for game in lines:
  possible = True
  name, groups = parse(game)
  if VERBOSE: print("### Starting game", name)

  minimal_bag = { "red": 0, "green": 0, "blue": 0 }
  for group in groups:
    for (color, count) in group:
      if count > bag[color]:
        possible = False
      if minimal_bag[color] < count:
        minimal_bag[color] = count

  if possible:
    if VERBOSE: print("Game", name, ": possible")
    part1 += name
  else:
    if VERBOSE: print("Game", name, ": NOPE")

  # This is just about the least readable way to multiple the values for
  # red, green and blue, but I'm having fun with functions.
  minimum_power = functools.reduce(operator.mul, minimal_bag.values())
  if VERBOSE: print ("Minimal bag:", minimum_power)
  part2 += minimum_power

print("Part 1", part1)
print("Part 2", part2)
