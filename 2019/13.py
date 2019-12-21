#!/usr/bin/env python
# Advent of code Day 11

import collections
import itertools
import os
import sys
import time
from threading import Event, Thread
from signal import signal, SIGINT


class Computer(Thread):
  def __init__(self, name):
    # Initialise thread.
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
# Run tests.
"""
computer = Computer("TEST")

computer.set_program([1002,4,3,4,33])
computer.run()


print "\nTest 1"
computer.set_program([1,9,10,3,2,3,11,0,99,30,40,50])
computer.add([0,0,0], 0)
assert(computer.program.values() == [1,9,10,70,2,3,11,0,99,30,40,50])

computer.clear_inputs()
computer.relative_base = 2000
computer.set_program([109, 19, 99])
computer.run()
assert computer.relative_base == 2019
computer.set_program([204,-34, 99])
computer.program[1985] = -1234567
computer.run()
assert computer.output == -1234567

print "\nTest 2"
program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
run(program, [4,3,2,1,0])
assert computer.output == 43210

print "\nTest 3"
program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0]
phase_seq = [0, 1, 2, 3, 4]
run(program, phase_seq)
assert computer.output == 54321

print "\nTest 4"
program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
phase_seq = [1, 0, 4, 3, 2]
run(program, phase_seq)
assert computer.output == 65210
print "\nTests passed."

print "\nTest 5"
program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
computer.clear_inputs()
computer.set_inputs([5])
computer.set_program(program)
computer.run()
assert computer.output == 999
computer.clear_inputs()
computer.set_inputs([8])
computer.set_program(program)
computer.run()
assert computer.output == 1000
computer.clear_inputs()
computer.set_inputs([10])
computer.set_program(program)
computer.run()
assert computer.output == 1001

print "\nTest 6!"
program = [104,1125899906842624,99]
computer.clear_inputs()
computer.set_program(program)
computer.run()
assert computer.output == 1125899906842624

print "\nTest 7!"
program = [1102,34915192,34915192,7,4,7,99,0]
computer.clear_inputs()
computer.set_program(program)
computer.run()
assert computer.output == 1219070632396864

print "\n Test 8!"
program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
computer.reset()
computer.set_program(program)
computer.run()
print computer.output

print "\nTests passed\n"
"""


print "\nRunning!"

with open("input13.txt") as f:
  program = [int(x) for x in f.read().split(",")]

class NoInputException(Exception):
  pass

class Arcade(Thread):
  def __init__(self, computer):
    super(Arcade, self).__init__()
    self.inputs = collections.deque([])
    self.name = "ARCADE"
    self.output_computer = computer
    self.halted = False
    self.stop_event = Event()
    self.squares = {}
    self.ball_x = -99
    self.ball_y = -99
    self.ball_last_x = -99
    self.ball_last_y = -99
    self.paddle = -99
    self.paddle_dest = -99
    self.scope = 0

  def set_inputs(self, inputs):
    for n in inputs:
      self.inputs.append(n)

  def next_input(self):
    return self.inputs.popleft()

  def next_inputs(self):
    if len(self.inputs) < 3:
      raise NoInputException
    returns = self.inputs.popleft(), self.inputs.popleft(), self.inputs.popleft()
    return returns

  def halt(self):
    print self.name, ": halt called!"
    self.stop_event.set()
    self.halted = True

  def display(self):
    s = ""
    for y in range(0, 21):
      for x in range(0, 36):
        try:
          s += self.squares[x, y]
        except KeyError:
          s += " "
      s += "\n"
    return s

  def tiles(self, tileid):
    ids = {
      0: " ",
      1: "#",
      2: "@",
      3: "_",
      4: "o",
      99: "!",
    }
    return ids[tileid]

  def count_blocks(self):
    count = 0
    for v in self.squares.values():
      if v == "@":
        count += 1
    return count

  def move_paddle(self):
    if self.ball_last_y == self.ball_y:
      # nothing's happened since we were here last
      # This is unexpected behaviour.
      print "Ball hasn't moved. Returning"
      self.ball_last_y = self.ball_y
      self.ball_last_x = self.ball_x
      return

    if self.paddle == -99:
      # No paddle yet. Don't do anything.
      self.ball_last_y = self.ball_y
      self.ball_last_x = self.ball_x
      return

    # How many moves until we crash.
    moves_away = 19 - self.ball_y

    # If the ball is moving up, just keep pace with it. Otherwise predict where
    # it's going.
    if self.ball_last_y > self.ball_y:
      ball_moving_to = self.ball_x
    elif self.ball_last_x > self.ball_x: # ball moving left
      ball_moving_to = self.ball_x - moves_away
    elif self.ball_last_x < self.ball_x: # ball moving right
      ball_moving_to = self.ball_x + moves_away
    else: # ball moving straight down
      ball_moving_to = self.ball_x

    if self.ball_y == 18 and self.paddle == ball_moving_to: # it's about to bounce
      # move the opposite direction from the ball
      ball_moving_to = self.ball_last_y

    self.ball_last_x = self.ball_x
    self.ball_last_y = self.ball_y

    if self.paddle == ball_moving_to:
      # It's on its way to the right place. Leave it alone.
      self.output_computer.set_inputs([0])
    elif self.paddle < ball_moving_to:
      # Move right.
      self.output_computer.set_inputs([1])
    else:
      # Move left
      self.output_computer.set_inputs([-1])

  def run(self):
    display_on = False
    while not self.stop_event.is_set():
      try:
        x, y, tile = robot.next_inputs()
      except NoInputException:
        continue
      if x == -1 and y == 0:
        self.score = tile
        print "SCOOOOORE!", self.score
        continue
      if tile == 4:
        self.ball_x = x
        self.ball_y = y
        #print "==> Ball now at (%d, %d)" % (x, y)
        self.move_paddle()
      if tile == 3:
        self.paddle = x
        #print "==> Paddle now at (%d, %d)" % (self.paddle, y)
      self.squares[(x, y)] = self.tiles(tile)
    print "There were %d blocks" % robot.count_blocks()


computer = Computer("COMPUTER")
computer.reset()
computer.set_inputs([1])
computer.set_program(program)
computer.program[0] = 2  # TODO is this cool?

robot = Arcade(computer)
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
  time.sleep(1)
