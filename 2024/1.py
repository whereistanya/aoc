#!/usr/bin/env python

filename = "input.txt"
#filename = "test1"

with open(filename, "r") as f:
  lines = f.readlines()


firsts = sorted([int(x.split()[0]) for x in lines])
seconds = sorted([int(x.split()[1]) for x in lines])

diffs = [abs(x[0] - x[1]) for x in zip(firsts, seconds)]
print(firsts)
print(seconds)
print(sum(diffs))

d = {}
for n in seconds:
  try:
    d[n] += 1
  except KeyError:
    d[n] = 1

total = 0
for n in firsts:
  try:
    total += n * d[n]
  except KeyError:
    pass

print(total)
