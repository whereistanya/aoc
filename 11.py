#!/usr/bin/env python
# Advent of code Day 11.

class PowerGrid(object):
	def __init__(self, serial):
		self.grid = {}
		self.serial = serial
		for x in range(0, 300):
			for y in range(0, 300):
				self.grid[(x, y)] = self.get_power_level(x, y)

	def get_power_level(self, x, y):
		rack_id = x + 10
		power_level = rack_id * y
		power_level += self.serial
		power_level *= rack_id
		if power_level < 100:
			power_level = 0
		else:
			power_level = int(str(power_level)[-3])
		power_level -= 5
		return power_level

	def get_highest_square(self):
		totals = {}
		for x in range(1, 299):
			for y in range(1, 299): # center of 3x3 square
				total_power = self.get_square(x, y, 3)
				totals[(x - 1, y - 1)] = total_power

		max_total = 0
		max_point = None
		for key, total in totals.iteritems():
			if total > max_total:
				max_total = total
				max_point = key

		return max_point, max_total


	def get_square(self, x, y, size):
		total_power =  self.grid[(x - 1, y - 1)]
		total_power += self.grid[(x    , y - 1)]
		total_power += self.grid[(x + 1, y - 1)]
		total_power += self.grid[(x - 1, y)]
		total_power += self.grid[(x    , y)]
		total_power += self.grid[(x + 1, y)]
		total_power += self.grid[(x - 1, y + 1)]
		total_power += self.grid[(x    , y + 1)]
		total_power += self.grid[(x + 1, y + 1)]

		return total_power



# tests
assert PowerGrid(8).get_power_level(3, 5) == 4
assert PowerGrid(57).get_power_level(122, 79) == -5
assert PowerGrid(39).get_power_level(217, 196) == 0
assert PowerGrid(71).get_power_level(101, 153) == 4
assert PowerGrid(18).get_highest_square() == ((33, 45), 29)
assert PowerGrid(42).get_highest_square() == ((21, 61), 30)

serial = 9306
grid = PowerGrid(serial)
print grid.get_highest_square()  # Submit without a space

