#!/usr/bin/env python3

n = 4 # part1
n = 14 # part2

with open("input6.txt", "r") as f:
  line = f.readlines()[0].strip()
  print (line)
  for i in range (n - 1, len(line) + 1):
    if len(set(list(line[i - n:i]))) == n:
      print (i, line[i - n:i])
      exit(0)
