#!/usr/bin/env python

input10 = "183,0,31,146,254,240,223,150,2,206,161,1,255,232,199,88"
lengths = [int(x) for x in input10.split(",")]

n = 256

#lengths = [3, 4, 1, 5]
#n = 5

values = [x for x in range(0, n)]
skip_size = 0
index = 0

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

print "Part 1:", values[0] * values[1]

# Part 2
print
print "Part 2"
print

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


assert run_hash("") == "a2582a3a0e66e6e86e3812dcb672a272"
assert run_hash("1,2,3") == "3efbe78a8d82f29979031a4aa0b16a9d"
assert run_hash("1,2,4") == "63960835bcdc130f0b66d7ff4f6a5a8e"

print "Dense hash", run_hash(input10)
