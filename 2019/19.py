#!/usr/bin/env python
# Advent of code Day 19

import collections
import itertools
import os
import sys
import time
from threading import Event, Thread
from signal import signal, SIGINT


class Computer(Thread):
  def __init__(self, name):
    super(Computer, self).__init__()
    self.name = name
    #print "Starting Computer", self.name
    self.inputs = collections.deque([])
    self.stop_event = Event()
    self.program = {}
    self.output = 0
    self.output_computer = None
    self.relative_base = 0

    self.opcodes = {
      1: self.add,
      2: self.mul,
      3: self.inp,
      4: self.outp,
      5: self.jit,
      6: self.jif,
      7: self.lt,
      8: self.eq,
      9: self.base,
    }

  def halt(self):
    print(self.name, ": halt called!")
    self.stop_event.set()

  def reset(self):
    self.program.clear()
    self.inputs.clear()
    self.output = None
    self.relative_base = 0

  def set_program(self, program):
    self.program.clear()
    for i in range(0, len(program)):
      self.program[i] = program[i]

  def clear_inputs(self):
    self.inputs.clear()

  def set_inputs(self, inputs):
    #print "INPUT!", inputs
    for n in inputs:
      self.inputs.append(n)

  def set_output(self, output_computer):
    self.output_computer = output_computer

  def next_input(self):
    while len(self.inputs) == 0:
      if self.stop_event.is_set():
        return -99
      #print "NO INPUT for", self.name
      #time.sleep(0.1)
    return self.inputs.popleft()

  def read_value(self, index, mode):
    try:
      if mode == 0:  # position mode
        position = self.program[index]
        value = self.program[position]
        return value
      elif mode == 1: # immediate mode
        value = self.program[index]
        return value
      elif mode == 2: # relative mode
        position = self.program[index]
        value = self.program[position + self.relative_base]
        return value
      else:
        print("OMG UNKNOWN MODE")
        return None
    except KeyError:
      return 0

  def read_output_position(self, index, mode):
    try:
      if mode == 0:  # position mode
        return self.program[index]
      elif mode == 2:
        return self.program[index] + self.relative_base
      else:
        raise IndexError
    except KeyError:
      return 0

  def write_value(self, index, value):
    self.program[index] = value

  def jit(self, modes, index):
    #print "jit from index %d, modes %s" % (index, modes)
    x = self.read_value(index + 1, modes[0])
    y = self.read_value(index + 2, modes[1])
    if x != 0:
      return y
    else:
      return index + 3

  def jif(self, modes, index):
    #print "jif from index %d, modes %s" % (index, modes)
    x = self.read_value(index + 1, modes[0])
    y = self.read_value(index + 2, modes[1])
    if x == 0:
        return y
    else:
      return index + 3

  def lt(self, modes, index):
    #print "lt from index %d, modes %s" % (index, modes)
    x = self.read_value(index + 1, modes[0])
    y = self.read_value(index + 2, modes[1])
    out_register = self.read_output_position(index + 3, modes[2])
    if x < y:
      self.write_value(out_register, 1)
    else:
      self.write_value(out_register, 0)
    return index + 4

  def eq(self, modes, index):
    #print "eq from index %d, modes %s" % (index, modes)
    x = self.read_value(index + 1, modes[0])
    y = self.read_value(index + 2, modes[1])
    out_register = self.read_output_position(index + 3, modes[2])

    if x == y:
      self.write_value(out_register, 1)
    else:
      self.write_value(out_register, 0)
    return index + 4

  def inp(self, modes, index):
    #print "inp from index %d, modes %s" % (index, modes)
    #print "Enter input! "
    #value = int(input())
    value = self.next_input()
    #print "Read input: %d" % value
    out_register = self.read_output_position(index + 1, modes[0])
    self.write_value(out_register, value)
    return index + 2

  def outp(self, modes, index):
    x = self.read_value(index + 1, modes[0])
    #print "%s: Diagnostic code: %d" % (self.name, x)
    self.output = x
    if self.output_computer:
      self.output_computer.set_inputs([x])
    return index + 2

  def base(self, modes, index):
    #print "base from index %d, modes %s" % (index, modes)
    x = self.read_value(index + 1, modes[0])
    self.relative_base += x
    return index + 2

  def mul(self, modes, index):
    #print "mul from index %d, modes %s" % (index, modes)
    x = self.read_value(index + 1, modes[0])
    y = self.read_value(index + 2, modes[1])
    out_register = self.read_output_position(index + 3, modes[2])
    self.write_value(out_register, x * y)
    return index + 4

  # Parameters that an instruction writes to will never be in immediate mode.
  def add(self, modes, index):
    #print "add from index %d, modes %s" % (index, modes)
    x = self.read_value(index + 1, modes[0])
    y = self.read_value(index + 2, modes[1])
    out_register = self.read_output_position(index + 3, modes[2])
    self.write_value(out_register, x + y)
    return index + 4


  def run(self):
    """Expects program as a comma separated string of integers"""
    #print "Running for", len(self.program), "values."
    index = 0

    while True:
      n = self.program[index]
      opcode, modes = self.parse(n)
      #print "==> [", index, "]", opcode, modes
      if self.stop_event.is_set():
        break
      if opcode == 99:
        #print "### Got 99 instruction. HALTING ###"
        if self.output_computer:
          self.output_computer.halt()
        break
      opfunc = self.opcodes[opcode]
      index = opfunc(modes, index)

  def parse(self, number):
    mode = [0, 0, 0]
    opcode = number % 100
    number /= 100

    for i in range(0, 3):
      m = number % 10
      if m == 1:
        mode[i] = 1
      if m == 2:
        mode[i] = 2
      number /= 10
    return opcode, mode


def run(program, phase_seq):
  computer.output = 0
  for i in range(0, len(phase_seq)):
    computer.set_inputs([phase_seq[i], computer.output])
    computer.set_program(program)
    computer.run()

# main
with open("input19.txt") as f:
  program = [int(x) for x in f.read().split(",")]


squares = {}

count = 0

def test(x, y, computer):
  computer.clear_inputs()
  computer.set_program(program)
  computer.set_inputs([x, y])
  computer.run()
  out = computer.output
  if out == 1:
    return True
  if out == 0:
    return False
  print("Unexpected return from computer: %d" % out)
  raise ValueError

def find_leftmost_x(x, y, computer):
  # take x as a hint and look for the leftmost true square
  found = test(x, y, computer)
  if found: # x,y is good, look left
    while True:
      x = x - 1
      found = test(x, y, computer)
      if not found:
        return x + 1
  else: # not at x,y so look right
    while True:
      x = x + 1
      found = test(x, y, computer)
      if found:
        return x

def find_rightmost_x(x, y, computer):
  # take x as a hint and look for the rightmost true square
  found = test(x, y, computer)
  if found: # x,y is good, look right
    while True:
      x = x + 1
      found = test(x, y, computer)
      if not found:
        return x - 1
  else: # not at x,y so look left
    while True:
      x = x - 1
      found = test(x, y, computer)
      if found:
        return x
      if x < 0:
        raise ValueError

def look_back(x, y, squares, width):
  #print "look_back", x
  while (x, y) in squares:
    #print "%d,%d; looking at %d,%d" % (
    #    x, y, x, y - (width - 1))
    if ((x, y - (width)) in squares and
        (x + width, y - width) in squares):
        return x
    else:
      x += 1
  return None

count = 0
width = 100
innerwidth = width - 1
computer = Computer("COMPUTER")
left = width / 2 # just a guess
right = width * 3 # same
for y in range(width, width * 20):
  left = find_leftmost_x(left, y, computer)
  right = find_rightmost_x(right, y, computer)
  for x in range(left, right + 1):
    squares[(x, y)] = "#"
    count += 1

  if (right - left + 1) >= width:
    foundx = look_back(left, y, squares, innerwidth)
    if foundx is not None:
      print("Part2: %d" % (foundx * 10000 + y - innerwidth))
      squares[(foundx, y - innerwidth)] = "0"
      squares[(foundx + innerwidth, y)] = "0"
      for i in range(foundx, foundx + innerwidth):
        squares[(i, y)] = "0"
      break

"""
# Draw it
for y in range(width, width * 20):
  s = ""
  for x in range(0, 100):
    if (x, y) in squares:
      s += squares[(x, y)]
    else:
      s += " "
  print s
"""
print("Part1: Found %d affected points" % count)
