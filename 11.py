#!/usr/bin/env python
# Advent of code Day 11.

def get_power_level(x, y, serial):
  rack_id = x + 10
  power_level = rack_id * y
  power_level += serial
  power_level *= rack_id
  if power_level < 100:
    power_level = 0
  else:
    power_level = int(str(power_level)[-3])
  power_level -= 5
  return power_level

def get_square(serial):
  grid = {}

  for x in range(0, 300):
    for y in range(0, 300):
      grid[(x, y)] = get_power_level(x, y, serial)

  totals = {}

  for x in range(1, 299):
    for y in range(1, 299): # center of 3x3 square
      total_power =  grid[(x - 1, y - 1)]
      total_power += grid[(x    , y - 1)]
      total_power += grid[(x + 1, y - 1)]
      total_power += grid[(x - 1, y)]
      total_power += grid[(x    , y)]
      total_power += grid[(x + 1, y)]
      total_power += grid[(x - 1, y + 1)]
      total_power += grid[(x    , y + 1)]
      total_power += grid[(x + 1, y + 1)]
      totals[(x - 1, y - 1)] = total_power

  max_total = 0
  max_point = None
  for key, total in totals.iteritems():
    if total > max_total:
      max_total = total
      max_point = key

  return max_point, max_total

# tests
assert get_power_level(3, 5, 8) == 4
assert get_power_level(122, 79, 57) == -5
assert get_power_level(217, 196, 39) == 0
assert get_power_level(101, 153, 71) == 4
assert get_square(18) == ((33, 45), 29)
assert get_square(42) == ((21, 61), 30)

serial = 9306
print get_square(serial)  # Submit without a space

