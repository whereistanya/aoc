#!/usr/bin/env python
# Advent of code Day 15

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
    print "Starting Computer", self.name
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
    print self.name, ": halt called!"
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
        print "OMG UNKNOWN MODE"
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

  def base(self, modses, index):
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
    print "Running for", len(self.program), "values."
    index = 0

    while True:
      n = self.program[index]
      opcode, modes = self.parse(n)
      #print "==> [", index, "]", opcode, modes
      if self.stop_event.is_set():
        break
      if opcode == 99:
        print "### Got 99 instruction. HALTING ###"
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
with open("input15.txt") as f:
  program = [int(x) for x in f.read().split(",")]

class NoInputException(Exception):
  pass

class Robot(Thread):
  def __init__(self):
    super(Robot, self).__init__()
    self.inputs = collections.deque([])
    self.name = "ROBOT"
    self.output_computer = None
    self.halted = False
    self.stop_event = Event()
    self.paths = []
    self.x = 0
    self.y = 0
    self.squares = {}
    self.start_coords = (40, 20) # Arbitrary starting point to draw from
    self.system = None # the thing we're looking for

  def set_inputs(self, inputs):
    for n in inputs:
      self.inputs.append(n)

  def next_input(self):
    while len(self.inputs) == 0:
      time.sleep(0.0001)
    return self.inputs.popleft()

  def halt(self):
    print self.name, ": halt called!"
    self.stop_event.set()
    self.halted = True

  def display(self, robotx, roboty):
    #os.system('clear')
    print "---------------------------------------------------------------------------------"
    for y in range (0, 50):
      s = ""
      for x in range(0, 72):
        if x == robotx and y == roboty:
          s += "o"
          continue
        try:
          s += (self.squares[(x, y)])
        except KeyError:
          s += " "
      print s

  def unseen_neighbours(self, x, y, seen):
    # north (1), south (2), west (3), and east (4)
    possible = [(x + 1, y, 4), # east
               (x - 1, y, 3), # west
               (x, y + 1, 1), # north
               (x, y - 1, 2) # south
    ]
    neighbours = []
    for x, y, d in possible:
      if (x, y) in seen:
        continue
      if (x, y) in self.squares and self.squares[(x, y)] == "#":
        continue
      neighbours.append((x, y, d))
    return neighbours

  def reverse(self, direction):
    d = {1: 2, 2:1, 3:4, 4:3}
    return d[direction]

  def neighbours(self, x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

  def bfs(self, startx, starty, stop_at=None):
    to_check = collections.deque()
    steps = -1
    to_check.append((startx, starty))
    seen = set()
    if stop_at:
      stop_x, stop_y = stop_at
    else:
      stop_x, stop_y = None, None
    while to_check:
      steps += 1
      this_step = list(to_check)
      to_check.clear()
      for x, y in this_step:
        seen.add((x, y))
        self.squares[x, y] = ","
        if x == stop_x and y == stop_y:
          print "FOUND IT in %d steps" % steps
          return
        for neighbour in self.neighbours(x, y):
          nx, ny = neighbour
          if (nx, ny) in seen:
            continue
          if self.squares[(nx, ny)] == "#":
            continue
          to_check.append((nx, ny))
    print "Saw the whole map in %d steps" % steps



  def run(self):
    # DFS to draw a map by walking the robot around.
    x, y = self.start_coords
    self.squares[(x, y)] = "O"
    directions = [2, 3, 1, 4]
    i = 0
    seen = set() # Where we've been
    stack = collections.deque() # stack
    stack.append((x, y, None))  # x, y, direction_back

    steps = 0
    while stack:
      x, y, direction_back = stack[-1] # look, don't pop it
      steps += 1
      seen.add((x, y))
      # get all neighbours
      unseen_neighbours = self.unseen_neighbours(x, y, seen)
      found = False
      for neighbour in unseen_neighbours:
        # try neighbours until we get a good one
        nx, ny, direction = neighbour
        self.output_computer.set_inputs([direction])
        result = self.next_input()
        if result == 0:
          self.squares[(nx, ny)] = "#"
          continue  # not this way; no location change
        # otherwise it's a valid direction
        found = True
        if result == 2:
          print "WIN. Found it at %d, %d" % (x, y)
          self.squares[(nx, ny)] = "S"
          self.system = (nx, ny)
          self.display(nx, ny)
        elif result == 1:
          self.squares[(nx, ny)] = "."
        # stop trying neighbours; take this path
        return_direction = self.reverse(direction)
        stack.append((nx, ny, return_direction))
        break
      if found == False:
        # None of the neighbours worked. Backtrack.
        stack.pop()
        if not direction_back:
          # We're back.
          print "FINISHED!"
          break
        self.output_computer.set_inputs([direction_back])
        result = self.next_input()
        if result != 1:
          print "Unexpected result backtracking from %d,%d: %d" % (x, y, result)
          sys.exit(1)
    print "Finished mapping the world, hurray!"
    self.output_computer.halt()
    self.display(0, 0)
    # Now BFS the map we drew
    startx, starty = self.start_coords
    self.bfs(startx, starty, stop_at=self.system)

    # Now BFS again for the whole map from the system coords
    self.bfs(self.system[0], self.system[1])


computer = Computer("COMPUTER")
computer.reset()
computer.set_program(program)

robot = Robot()
computer.set_output(robot)
robot.output_computer = computer
computer.start()
robot.start()
robot.join()
computer.join()
