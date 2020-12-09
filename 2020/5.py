#!/usr/bin/env python

inputfile = "input5.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

rows = {}

for line in lines:
  row = line.replace("B", "1")[0:7]
  row = int(row.replace("F", "0"), 2)

  seat = line.replace("L", "0")[7:]
  seat = int(seat.replace("R", "1"), 2)

  #print row, seat, row*8 + seat

  try:
    rows[row].append(seat)
  except KeyError:
    rows[row] = [seat]

for row in rows:
  print str(row).zfill(3), sorted(rows[row])
