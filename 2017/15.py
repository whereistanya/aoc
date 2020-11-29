#!/usr/bin/env python
# Advent of code Day 1.5

#Generator A starts with 699
#Generator B starts with 124

class Generator(object):
  def __init__(self, start, factor):
    self.value = start
    self.factor = factor
    self.binary = ""
    self.divisor = 1

  def calculate(self):
    while True:
      value = self.value
      # 2,147,483,647 is 2^31-1, the maximum value for a 32 bit signed int.
      # so we're taking the last 32 bits by getting the modulus here.
      new = value * self.factor % 2147483647
      self.value = new
      returnable = new % 65536
      if returnable % self.divisor == 0:
        return new % 65536

gena = Generator(699, 16807)
genb = Generator(124, 48271)

# Test input
# gena = Generator(65, 16807)
# genb = Generator(8921, 48271)
gena.divisor = 4
genb.divisor = 8

matches = 0
for i in range(5000000):
  a = gena.calculate()
  b = genb.calculate()
  if a == b:
    print(matches, a)
    matches += 1

matches, "matches"
