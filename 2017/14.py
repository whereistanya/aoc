#!/usr/bin/env python
# Advent of code Day 14

import collections

def run_hash(input10):
  n = 256
  lengths = [ord(x) for x in input10]
  lengths.extend([17, 31, 73, 47, 23])
  values = [x for x in range(0, n)]
  skip_size = 0
  index = 0

  for run in range(0, 64):
    #print "Run: %d, index: %d, skip_size: %d" % (run, index, skip_size)
    for length in lengths:
      substr = values[index: index + length]
      if index + length > len(values):
        substr += values[0: (index + length) - len(values)]
      substr.reverse()

      for i in range(len(substr)):
        values[(index + i) % len(values)] = substr[i]
      index += (length + skip_size)
      index = index % len(values)
      skip_size += 1

  dense = ""
  i = 0
  while i < len(values):
    to_xor = values[i:i+16]
    value = 0
    for item in to_xor:
      value = value ^ item
    dense += ("%0.2x" % value)
    i += 16
  return dense

inputstr = "jzgqcdpd"

s = ""
on = set()
for i in range(128):
  out = run_hash("%s-%d" % (inputstr, i))
  binary = bin(int(out, 16))[2:]  # strip the "0b"
  binary = binary.zfill(128)
  #print "flqrgnkx-%d" % i, out, binary[0:8]
  for j in range (len(binary)):
    c = binary[j]
    if c == '1':
      on.add((i, j))
  #    s += "#"
  #  else:
  #    s += "."
  #s += "\n"

print "Part 1:", len(on), "ones"

#print s

groups = 0

while on:
  startnode = on.pop()

  to_check = collections.deque([startnode])
  seen = set()
  while to_check:
    node = to_check.popleft()
    seen.add(node)
    x = node[0]
    y = node[1]
    neighbours = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    for neighbour in neighbours:
      if neighbour not in seen:
        if neighbour in on:
          to_check.append(neighbour)
  groups += 1
  for node in seen:
    if node != startnode:
      on.remove(node)

print "Part 2", groups, "groups"

