#!/usr/bin/env python
# Advent of code day 18.

import re
import time
from threading import Event, Thread
import collections

class Computer(Thread):
  def __init__(self, name):
    super(Computer, self).__init__()
    self.name = name
    self.registers = {} # 'a' to something
    self.program = []
    self.index = 0
    self.freq = -1
    self.other_computer = None
    self.messages = collections.deque()
    self.waiting = False
    self.send_count = 0

  def run(self):
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

  def value(self, x):
    if len(x) == 1 and ord(x) in range(97, 123):  # it's a letter
      try:
        return self.registers[x]
      except KeyError:
        return 0
    # it's a number
    try:
      return int(x)
    except TypeError:
      print "Couldn't convert", x
      exit()

  def snd(self, x, _):
    #print "snd", x
    value = self.value(x)
    self.freq = value
    self.other_computer.messages.append(value)
    self.index += 1
    self.send_count += 1

  def setreg(self, x, y):
    #print "setreg", x, y
    value = self.value(y)
    self.registers[x] = value
    self.index += 1

  def add(self, x, y):
    #print "add", x, y
    value = self.value(y)
    try:
      self.registers[x] += value
    except KeyError:
      self.registers[x] = value
    self.index += 1

  def mul(self, x, y):
    #print "mul", x, y
    value = self.value(y)
    try:
      self.registers[x] *= value
    except KeyError:
      self.registers[x] = 0
    self.index += 1

  def mod(self, x, y):
    #print "mod", x, y
    value = self.value(y)
    try:
      self.registers[x] %= value
    except KeyError:
      self.registers[x] = 0
    self.index += 1

  def rcv(self, x, _):
    #print "rcv", x
    sleep_count = 0
    while len(self.messages) == 0:
      if sleep_count > 10:  # waited a bunch of times
        self.waiting = True
      if self.other_computer.waiting:
        self.waiting = True
        print "Both computers waiting. Deadlock detected."
        print self.name, ": final registers:", self.registers
        print self.name, ": I sent", self.send_count
        exit()
      sleep_count += 1
      time.sleep(0.001)
    self.waiting = False
    value = self.messages.popleft()
    self.registers[x] = value
    # Part 1
    # value = self.value(x)
    #if value != 0:
    #  print "Frequency is", self.freq
    #  exit()
    self.index += 1


  def jgz(self, x, y):
    #print "jgz", x, y
    xvalue = self.value(x)
    yvalue = self.value(y)
    if xvalue > 0:
      self.index += yvalue
    else:
      self.index += 1


line_re = "^(\w{3}) (\w) ?([-\w]+)?$"

with open("input18.txt", "r") as f:
  lines = f.readlines()

"""
lines = [
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
]

lines = [
  "snd 1",
  "snd 2",
  "snd p",
  "rcv a",
  "rcv b",
  "rcv c",
  "rcv d",
]
"""
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


computera = Computer("ComputerA")
computerb = Computer("ComputerB")

computera.other_computer = computerb
computerb.other_computer = computera

computera.registers['p'] = 0
computerb.registers['p'] = 1

computera.program = list(program)
computerb.program = list(program)

computera.start()
computerb.start()

computera.join(1)
computerb.join(1)
