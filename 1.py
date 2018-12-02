# Advent of code Day 1.
#!/usr/bin/env python

freq = 0

with open("day1input.txt", "r") as f:
  lines = f.readlines()

  found = set()
  found.add(0)
  first_dup = None

  while not first_dup:
    print("Starting a run at frequency %d" % freq)
    for line in lines:
      freq += int(line.strip())
      if not first_dup:
        if freq in found:
          first_dup = freq
        found.add(freq)
    print("Ending a run at frequency %d" % freq)

  print("First duplicate was %d" % first_dup)
