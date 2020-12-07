#!/usr/bin/env python

inputfile = "input6.txt"

with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

"""
lines = [
  "abc",
  "",
  "a",
  "b",
  "c",
  "",
  "ab",
  "ac",
  "",
  "a",
  "a",
  "a",
  "a",
  "",
  "b",
]
"""
count = 0

current = {}
group_size = 0
for line in lines:
  if line == "":
    print group_size, current
    for k in current:
      if current[k] == group_size:
        count += 1
    current.clear()
    group_size = 0
    print "Count is now", count
    continue
  group_size += 1
  for char in line:
    if char in current.keys():
      current[char] += 1
    else:
      current[char] = 1
  
for k in current:
  if current[k] == group_size:
    count += 1
print count
