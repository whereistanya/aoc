#!/usr/bin/env python
# Advent of code Day 19.

import re
import sys
from blist import blist

line_re = "(\w+):\s*\[(\d+), (\d+), (\d+), (\d+)\]"

def read_file():
  with open("day19input.txt", "r") as f:
    lines = f.readlines()
  declaration = ""
  instructions = []

  """
  lines = [
    "#ip 0",
    "seti 5 0 1",
    "seti 6 0 2",
    "addi 0 1 0",
    "addr 1 2 3",
    "setr 1 0 0",
    "seti 8 0 4",
    "seti 9 0 5",
  ]
  """

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
    self.registers[c] = self.registers[a] & b

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
i = 0
while True:
  i += 1
  if computer.registers[ip] +1 >= len(program):
    # Last instruction.
    print("HALT")
    break
  computer.registers[ip] += 1
  line = program[computer.registers[ip]]

  prereg = list(computer.registers) # copy() in py3.3
  funcname, a, b, c = line
  func = getattr(computer, funcname)
  x = func(a, b, c)
  # print "ip=%01d %s %s %d %d %d %s" % (computer.registers[ip], prereg, funcname, a, b, c, computer.registers)

print("Part one:", computer.registers[0])

############
# Part two #
############

# What this program is actually trying to do...
to_factor = 10551314
total = to_factor

for i in range(1, to_factor / 2 + 1):
  if to_factor % i == 0:
    total += i

print("Part two:", total)
