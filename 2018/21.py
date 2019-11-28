#!/usr/bin/env python
# Advent of code Day 21

import sys
from blist import blist

def read_file():
  with open("day21input.txt", "r") as f:
    lines = f.readlines()
    instructions = []

  for line in lines:
    if line.startswith("#"):
      ip = int(line.split()[1])
    else:
      words = line.strip().split()
      instructions.append((words[0], int(words[1]), int(words[2]), int(words[3])))
  return ip, instructions


class Computer(object):
  """A very tiny computer. Each returns a, b, c"""
  def __init__(self):
    self.registers = blist([0, 0, 0, 0, 0, 0])

  def addr(self, a, b, c):
    """stores into register C the result of adding register A and register B"""
    self.registers[c] = self.registers[a] + self.registers[b]

  def addi(self, a, b, c):
    """stores into register C the result of adding register A and value B"""
    self.registers[c] = self.registers[a] + b

  def mulr(self, a, b, c):
    """stores into register C the result of multiplying register A and register B"""
    self.registers[c] = self.registers[a] * self.registers[b]

  def muli(self, a, b, c):
    """stores into register C the result of multiplying register A and value B"""
    self.registers[c] = self.registers[a] * b

  def banr(self, a, b, c):
    """banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B."""
    self.registers[c] = self.registers[a] & self.registers[b]

  def bani(self, a, b, c):
    """bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B."""
    numeric_bitwise = self.registers[a] & b
    self.registers[c] = numeric_bitwise


  def borr(self, a, b, c):
    """borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B"""
    self.registers[c] = self.registers[a] | self.registers[b]

  def bori(self, a, b, c):
    """bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B."""
    self.registers[c] = self.registers[a] | b

  def setr(self, a, b, c):
    """"copies the contents of register A into register C. (Input B is ignored.)"""
    self.registers[c] = self.registers[a]

  def seti(self, a, b, c):
    """seti (set immediate) stores value A into register C. (Input B is ignored.)"""
    self.registers[c] = a

  def gtir(self, a, b, c):
    """gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0."""
    if a > self.registers[b]:
      self.registers[c] = 1
    else:
      self.registers[c] = 0

  def gtri(self, a, b, c):
    """(greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0."""
    if self.registers[a] > b:
      self.registers[c] = 1
    else:
      self.registers[c] = 0

  def gtrr(self, a, b, c):
    """(greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0."""
    if self.registers[a] > self.registers[b]:
      self.registers[c] = 1
    else:
      self.registers[c] = 0

  def eqir(self, a, b, c):
    """eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0."""
    if a == self.registers[b]:
      self.registers[c] = 1
    else:
      self.registers[c] = 0

  def eqri(self, a, b, c):
    """(equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0."""
    if self.registers[a] == b:
      self.registers[c] = 1
    else:
      self.registers[c] = 0

  def eqrr(self, a, b, c):
    """equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0."""
    if self.registers[a] == self.registers[b]:
      self.registers[c] = 1
    else:
      self.registers[c] = 0


# main
ip, program = read_file()
computer = Computer()

############
# Part one #
############
# Nasty hackery to start at zero.
computer.registers[ip] = -1

# Running the program shows "eqrr 4 0 2" trying to match 5745418
to_match = 5745418

# computer.registers[0] = to_match  # part 1

eqrr_loop = set()

i = 0
eqrrs = 0

"""
while eqrrs < 6:
  computer.registers[ip] += 1
  if computer.registers[ip] >= len(program):
    # Out of program bounds
    print "HALT"
    break
  prev = computer.registers[ip]
  line = program[computer.registers[ip]]

  prereg = list(computer.registers) # copy() in py3.3
  funcname, a, b, c = line
  func = getattr(computer, funcname)
  i += 1
  if funcname == "eqrr":
    eqrrs += 1
    if computer.registers[4] in eqrr_loop:
      sys.exit(0)
    eqrr_loop.add(computer.registers[4])
  x = func(a, b, c)
  print "ip=%01d->%01d %s %s %d %d %d %s" % (prev, computer.registers[ip], prereg, funcname, a, b, c, computer.registers)

print "Part one:", to_match

sys.exit(0)
"""

############
# Part two #
############

"""
ip=28->28 [0, 1, 1, 1, 5745418, 28] eqrr 4 0 2 blist([0, 1, 0, 1, 5745418, 28]) 1847
ip=28->28 [0, 1, 1, 87, 2658765, 28] eqrr 4 0 2 blist([0, 1, 0, 87, 2658765, 28]) 159602
ip=28->28 [0, 1, 1, 41, 12442882, 28] eqrr 4 0 2 blist([0, 1, 0, 41, 12442882, 28]) 234421
ip=28->28 [0, 1, 1, 189, 10012665, 28] eqrr 4 0 2 blist([0, 1, 0, 189, 10012665, 28]) 576024
ip=28->28 [0, 1, 1, 153, 9760028, 28] eqrr 4 0 2 blist([0, 1, 0, 153, 9760028, 28]) 852709
ip=28->28 [0, 1, 1, 149, 7281471, 28] eqrr 4 0 2 blist([0, 1, 0, 149, 7281471, 28]) 1122464
"""


def run_program(x, y, z):
  # input is the eqrr check. reg2,reg3,reg4 entering the check.
  reg0 = 0 # what we aim to find

  #print "eqrr:", x, y, z
  if z == reg0: # HALT
    print "success"
    sys.exit(0)
  else:
    x = 0

    #### eqrr to gtir ####
  y = z | 65536 # bori 4 65536 3
  z = 14464005 # seti 14464005 5 4
  x = y & 255 # bani 3 255 2
  z += x # addr 4 2 4
  z = z & 16777215 # bani 4 16777215
  z *= 65899 # muli 4 65899 4
  z = z & 16777215 # bani 4 16777215
  if 256 > y: # gtir 256 3 2
    x = 1
  else:
    x = 0

  x = 0
  reg1 = 2  # TODO: this is actually a +2; is it always 0?
  reg1 *= 256

  #### loop until reg1 > reg3:  ####
  while reg1 <= y:
    x += 1
    reg1 = x * 256
  x -= 1
  #print "After the first loop", x, y, z

  y = x
  x = y & 255
  z += x
  z = z & 16777215
  z *= 65899
  z = z & 16777215

  if 256 > y:
    x = 1
  else:
    x = 0
  #print "after gtir", x, y, z

  x = 0
  reg1 = 0  # maybe?

  # the second small loop
  while reg1 <= y:
    x += 1
    reg1 = x * 256
  x -= 1
  #print "After the second loop %d, %d, %d" % (x, y, z)

  y = x
  x = y & 255
  z += x
  z = z & 16777215
  z = z * 65899
  z = z & 16777215
  if 256 > y:
    x = 1
  else:
    x = 0

  return x, y, z

x, y, z = 1, 1, 5745418

eqrrs = set()

for i in range(0, 50000):
  x, y, z = run_program(x, y, z)
  if z in eqrrs:
    print "loop on", z
    sys.exit(0)
  else:
    # The last non-looped z is the answer.
    print z
  eqrrs.add(z)

