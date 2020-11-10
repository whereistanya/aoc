#!/usr/bin/env python
# Advent of code day 18.

import re

with open("input18.txt", "r") as f:
  lines = f.readlines()

"""lines = [
  "set a 1",
  "add a 2",
  "mul a a",
  "mod a 5",
  "snd a",
  "set a 0",
  "rcv a",
  "jgz a -1",
  "set a 1",
  "jgz a -2",
]"""


class Computer(object):
  def __init__(self):
    self.registers = {} # 'a' to something
    self.program = []
    self.index = 0
    self.freq = -1

  def run(self, program):
    self.program = program
    fns = {
      "snd" : self.snd,
      "set": self.setreg,
      "add" : self.add,
      "mul": self.mul,
      "mod": self.mod,
      "rcv": self.rcv,
      "jgz": self.jgz,
    }
    while True:
      op, register, value = self.program[self.index]
      fn = fns[op]
      fn(register, value)  # value may be None
      self.index += 1

  def snd(self, x, _):
    self.freq = x
    print "snd", x

  def setreg(self, x, y):
    print "setreg", x, y

  def add(self, x, y):
    print "add", x, y

  def mul(self, x, y):
    print "mul", x, y

  def mod(self, x, y):
    print "mod", x, y

  def rcv(self, x, y):
    print "rcv", x, y

  def jgz(self, x, y):
    print "jgz", x, y


line_re = "^(\w{3}) (\w) ?([-\w]+)?$"

computer = Computer()
program = []

for line in lines:
  search = re.search(line_re, line)
  if not search:
    print "Couldn't match", line
    continue
  groups = search.groups()
  op = groups[0]
  register = groups[1]
  value = groups[2]
  program.append((op, register, value))
computer.run(program)
