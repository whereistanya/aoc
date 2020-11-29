#!/usr/bin/env python
# Advent of code Day 11.

class PowerGrid(object):
	def __init__(self, serial):
		self.max = 300
		self.grid = {}
		self.squares = {}  # (x, y, size)
		self.serial = serial
		for x in range(0, self.max):
			for y in range(0, self.max):
				self.grid[(x, y)] = self.get_power_level(x, y)
				self.squares[(x, y, 1)] = self.grid[(x, y)]

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

	def get_highest_square(self, size):
		for x in range(0, self.max):
			for y in range(0, self.max): # center of 3x3 square
				for z in range(1, size):
					total_power = self.get_square(x, y, size)
					if total_power:
						self.squares[(x, y, size)] = total_power

		max_total = 0
		max_point = None
		for key, total in self.squares.items():
			if total > max_total:
				max_total = total
				max_point = key

		return max_point, max_total

	def get_square(self, x, y, size):
		if (x + size) > self.max or (y + size) > self.max:
			return None
		if (x, y, size) in self.squares:
			return self.squares[(x, y, size)]

		total_power = self.get_square(x, y, size - 1)
		for i in range (0, size - 1):
			xi = x + i
			yi = y + i
			total_power += self.grid[(xi, y + size -1)]
			total_power += self.grid[(x + size -1, yi)]
		total_power += self.grid[(x + size -1, y + size -1)]
		self.squares[(x, y, size)] = total_power
		return total_power

"""
# tests
assert PowerGrid(8).get_power_level(3, 5) == 4
assert PowerGrid(57).get_power_level(122, 79) == -5
assert PowerGrid(39).get_power_level(217, 196) == 0
assert PowerGrid(71).get_power_level(101, 153) == 4
assert PowerGrid(18).get_highest_square(3) == ((33, 45, 3), 29)
assert PowerGrid(42).get_highest_square(3) == ((21, 61, 3), 30)
assert PowerGrid(18).get_highest_square(17) == ((90,269,16), 113)
assert PowerGrid(42).get_highest_square(17) == ((232,251,12), 119)
"""


serial = 9306
grid = PowerGrid(serial)

# Guessing this is a square of 20 or less. Can try bigger ones but it's slow.
print(grid.get_highest_square(20))  # Submit without a space

