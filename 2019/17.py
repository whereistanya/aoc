#!/usr/bin/env python
# Advent of code Day 17

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
    print("Starting Computer", self.name)
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
    print("INPUT!", inputs)
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
    print("Running for", len(self.program), "values.")
    index = 0

    while True:
      n = self.program[index]
      opcode, modes = self.parse(n)
      #print "==> [", index, "]", opcode, modes
      if self.stop_event.is_set():
        break
      if opcode == 99:
        #print "### Got 99 instruction. HALTING ###"
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
with open("input17.txt") as f:
  program = [int(x) for x in f.read().split(",")]

class NoInputException(Exception):
  pass

class Robot(Thread):
  def __init__(self, computer):
    super(Robot, self).__init__()
    self.inputs = collections.deque([])
    self.name = "ROBOT"
    self.output_computer = computer
    self.halted = False
    self.stop_event = Event()
    self.paths = []
    self.x = 0
    self.y = 0
    self.squares = {}

  def set_inputs(self, inputs):
    for n in inputs:
      self.inputs.append(n)

  def next_input(self):
    i = 0
    while len(self.inputs) == 0:
      i += 1
      if self.stop_event.set():
        return "-99"
      time.sleep(0.0001)
      if i > 2000:
        return "-88"
    return self.inputs.popleft()

  def halt(self):
    #print self.name, ": halt called!"
    self.stop_event.set()
    self.halted = True

  def move(self):
    pass

  def parse_input(self):
    # Reads input until a newline and returns it.
    output = []
    s = ""
    while True:
      n = self.next_input()
      if n == "-88":
        return s, True
      try:
        o = chr(n)
        if o == "X":
          s += o
          # we fell down
          self.halt()
          return s, True
      except ValueError:
        o = "[%d]" % n
      if n == 10: # newline
        return s, False
      else:
        s += o

  def count_parameters(self):
    total = 0
    count = 0
    for square in self.squares:
      if self.squares[square] != "#":
        continue
      x = square[0]
      y = square[1]
      try:
        if self.squares[(x, y - 1)] != "#":
          continue
        if self.squares[(x, y + 1)] != "#":
          continue
        if self.squares[(x +1, y)] != "#":
          continue
        if self.squares[(x -1, y)] != "#":
          continue
        self.squares[(x, y)] = "O"
        total += (x * y)
        count += 1
        print("%d * %d = %d" % (x, y, x * y))
      except KeyError:
        continue
    print("Found %d parameters" % count)

  def send_input(self, code):
    inputs = {
      "A": list(map(ord, "R,4,L,12,L,8,R,4\n")),
      "B": list(map(ord, "L,8,R,10,R,10,R,6\n")),
      "C": list(map(ord, "R,4,R,10,L,12\n")),
      "Main": list(map(ord, 'A,B,A,C,A,B,A,C,B,C\n')),
      "y": list(map(ord, 'y\n')),
    }

    computer.set_inputs(inputs[code])

  def run(self):
    while not self.stop_event.set():
      s, halt = self.parse_input()
      print(s)
      if halt:
        sys.exit(1)
      if s.startswith("Main:"):
        self.send_input("Main")
        self.send_input("A")
        self.send_input("B")
        self.send_input("C")
        self.send_input("y")
        print("All input sent.")


computer = Computer("COMPUTER")
computer.reset()
computer.set_program(program)
computer.program[0] = 2  # part 2

robot = Robot(computer)
computer.set_output(robot)
computer.start()
robot.start()

while True:
  try:
    robot.join(1)
    computer.join(1)
    break
  except KeyboardInterrupt:
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    robot.halt()
    computer.halt()
    break
