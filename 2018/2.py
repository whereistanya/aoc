#!/usr/bin/env python
# Advent of code Day 2.

with open("day2input.txt", "r") as f:
  lines = f.readlines()

######################################
# Part one
######################################

#  lines = [
#    "aaabbc",
#    "panda",
#    "ppppaaaassssdddd",
#    "qwerty",
#    "ababab",
#    "xxoox",
#   ]
twos = set()
threes = set()

for line in lines:
  counts = {}
  for letter in line:
    try:
      counts[letter] += 1
    except KeyError:
      counts[letter] = 1
  for v in list(counts.values()):
    if v == 2:
      twos.add(line)
    elif v == 3:
      threes.add(line)

print("Twos: %s" % len(twos))
print("Threes: %s" % len(threes))
print("Checksum: %s" % (len(twos) * len(threes)))


######################################
# Part two
######################################

patterns = {}  # {pattern: word that matches it,}

for line in lines:
  word = line.strip()
  for i in range(0, len(word)):
    pattern = word[0:i] + "_" + word[i+1: len(word)]
    if pattern in patterns:
      print("Match! %s and %s!" % (word, patterns[pattern]))
      print("Letters in common are %s" % pattern.replace("_", ""))
    patterns[pattern] = word
