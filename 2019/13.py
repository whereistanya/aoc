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


program = [1,380,379,385,1008,2151,871073,381,1005,381,12,99,109,2152,1102,1,0,383,1101,0,0,382,21001,382,0,1,20102,1,383,2,21102,37,1,0,1106,0,578,4,382,4,383,204,1,1001,382,1,382,1007,382,36,381,1005,381,22,1001,383,1,383,1007,383,21,381,1005,381,18,1006,385,69,99,104,-1,104,0,4,386,3,384,1007,384,0,381,1005,381,94,107,0,384,381,1005,381,108,1106,0,161,107,1,392,381,1006,381,161,1102,1,-1,384,1106,0,119,1007,392,34,381,1006,381,161,1101,0,1,384,21002,392,1,1,21102,1,19,2,21102,0,1,3,21102,1,138,0,1106,0,549,1,392,384,392,20101,0,392,1,21102,19,1,2,21102,3,1,3,21101,161,0,0,1106,0,549,1101,0,0,384,20001,388,390,1,21001,389,0,2,21102,1,180,0,1105,1,578,1206,1,213,1208,1,2,381,1006,381,205,20001,388,390,1,20101,0,389,2,21102,205,1,0,1105,1,393,1002,390,-1,390,1101,1,0,384,20102,1,388,1,20001,389,391,2,21101,228,0,0,1105,1,578,1206,1,261,1208,1,2,381,1006,381,253,21002,388,1,1,20001,389,391,2,21101,0,253,0,1105,1,393,1002,391,-1,391,1101,1,0,384,1005,384,161,20001,388,390,1,20001,389,391,2,21102,1,279,0,1105,1,578,1206,1,316,1208,1,2,381,1006,381,304,20001,388,390,1,20001,389,391,2,21102,304,1,0,1105,1,393,1002,390,-1,390,1002,391,-1,391,1102,1,1,384,1005,384,161,21002,388,1,1,20101,0,389,2,21102,0,1,3,21101,338,0,0,1106,0,549,1,388,390,388,1,389,391,389,21001,388,0,1,20102,1,389,2,21101,0,4,3,21102,1,365,0,1105,1,549,1007,389,20,381,1005,381,75,104,-1,104,0,104,0,99,0,1,0,0,0,0,0,0,180,16,16,1,1,18,109,3,22101,0,-2,1,21201,-1,0,2,21102,1,0,3,21101,414,0,0,1105,1,549,22102,1,-2,1,21201,-1,0,2,21102,429,1,0,1106,0,601,1202,1,1,435,1,386,0,386,104,-1,104,0,4,386,1001,387,-1,387,1005,387,451,99,109,-3,2105,1,0,109,8,22202,-7,-6,-3,22201,-3,-5,-3,21202,-4,64,-2,2207,-3,-2,381,1005,381,492,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,481,21202,-4,8,-2,2207,-3,-2,381,1005,381,518,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,507,2207,-3,-4,381,1005,381,540,21202,-4,-1,-1,22201,-3,-1,-3,2207,-3,-4,381,1006,381,529,22101,0,-3,-7,109,-8,2106,0,0,109,4,1202,-2,36,566,201,-3,566,566,101,639,566,566,1201,-1,0,0,204,-3,204,-2,204,-1,109,-4,2106,0,0,109,3,1202,-1,36,593,201,-2,593,593,101,639,593,593,21001,0,0,-2,109,-3,2105,1,0,109,3,22102,21,-2,1,22201,1,-1,1,21101,383,0,2,21101,0,250,3,21101,756,0,4,21101,630,0,0,1106,0,456,21201,1,1395,-2,109,-3,2105,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,2,2,0,2,0,0,0,0,0,0,2,2,0,2,2,0,2,2,0,0,2,2,2,0,0,0,0,2,2,2,0,1,1,0,0,0,0,2,0,2,2,0,0,2,2,0,0,2,2,0,0,2,2,2,2,0,2,0,2,2,2,2,0,2,0,0,0,1,1,0,0,2,2,0,0,0,0,0,0,2,2,2,0,0,0,0,0,2,0,2,0,0,0,0,0,2,0,2,2,0,2,0,0,1,1,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,2,0,0,2,0,2,0,0,0,0,0,0,0,2,2,2,0,2,0,1,1,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,2,0,0,0,2,2,0,0,0,2,0,0,0,2,0,2,2,2,0,1,1,0,0,0,0,2,2,2,2,2,0,2,0,0,0,0,2,0,2,0,2,0,2,0,0,2,2,0,2,0,2,0,2,0,0,1,1,0,2,2,0,2,2,2,2,0,2,2,2,2,0,0,2,0,0,2,0,2,0,0,0,2,0,0,2,2,2,0,0,0,0,1,1,0,0,2,0,0,2,2,0,0,0,0,2,2,0,0,2,0,0,0,2,2,0,2,0,2,2,0,2,2,0,0,0,2,0,1,1,0,0,0,0,0,0,0,2,0,0,0,2,0,2,0,0,0,2,2,2,2,0,2,2,0,2,2,0,0,0,2,0,0,0,1,1,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,2,0,2,0,0,0,0,2,2,0,2,2,2,0,0,2,0,2,0,1,1,0,0,0,0,2,2,0,2,2,0,2,0,2,2,2,0,0,2,2,0,0,0,0,0,0,2,0,2,2,2,0,2,2,0,1,1,0,2,0,0,2,0,0,0,0,0,2,0,0,2,2,0,2,2,2,0,2,2,0,0,2,2,0,0,2,2,0,0,2,0,1,1,0,2,0,2,0,2,0,2,0,0,2,2,0,0,2,0,0,0,2,0,2,2,0,2,0,0,0,2,0,2,2,0,2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,52,20,53,45,54,10,5,35,28,96,68,78,29,94,94,57,42,27,61,91,60,22,54,59,33,71,63,62,97,30,76,40,87,10,30,83,68,41,63,55,24,65,56,57,21,91,17,7,60,94,34,54,75,10,16,88,32,34,41,36,57,39,14,89,23,47,7,94,89,60,56,36,44,77,29,17,93,55,58,62,61,18,50,54,22,75,45,1,29,64,32,97,98,50,37,64,39,61,23,39,61,85,85,10,37,56,84,13,43,91,20,73,77,34,87,33,36,42,48,3,39,6,18,58,38,63,48,38,96,32,72,51,22,37,76,4,95,17,3,79,89,19,12,22,71,98,95,22,82,31,70,98,48,46,6,80,95,98,1,81,27,91,14,98,13,46,21,6,75,59,73,9,52,6,44,92,9,11,65,71,19,52,84,71,38,60,43,10,78,25,22,27,90,4,23,96,19,42,54,80,63,64,26,29,58,75,35,95,38,48,1,47,61,20,74,39,85,33,10,70,90,39,93,61,9,65,19,56,84,59,57,30,76,19,52,66,89,93,19,86,4,67,59,37,28,71,1,21,40,18,92,72,57,63,88,42,17,92,42,88,93,17,19,26,63,31,1,8,76,62,31,49,36,18,19,63,50,50,13,77,22,45,11,92,7,92,69,66,49,34,2,58,61,4,18,26,20,7,51,84,81,38,72,22,83,92,16,97,20,81,25,74,13,84,71,2,81,35,83,6,73,93,60,47,2,98,27,55,68,59,67,63,61,48,65,28,71,56,39,30,93,96,3,47,93,77,11,28,86,79,90,83,39,21,68,2,49,50,78,68,81,97,49,9,44,79,31,69,81,76,93,17,31,66,46,26,18,1,17,72,1,28,47,15,85,50,95,75,52,86,5,35,59,51,41,88,33,9,7,77,1,46,6,40,39,36,52,10,12,34,87,64,13,23,96,15,89,13,64,65,29,27,28,50,57,91,68,97,5,38,57,28,45,6,10,90,7,26,79,89,93,74,77,58,51,86,75,49,80,80,28,94,11,56,36,69,88,50,10,22,77,51,83,47,53,2,46,33,45,44,23,4,28,62,21,88,61,58,72,16,4,6,47,25,37,46,72,65,74,9,69,60,62,39,82,63,17,4,79,43,68,80,17,20,20,49,59,70,5,3,69,44,95,38,90,11,98,76,36,59,80,74,85,1,46,19,97,14,89,96,14,65,68,13,90,13,46,24,39,63,73,84,46,66,92,84,56,86,44,33,23,6,91,13,25,75,76,31,68,4,40,83,51,85,70,84,27,71,40,53,75,59,77,79,98,90,33,94,63,19,65,44,90,18,71,17,72,40,32,16,43,16,55,28,93,76,68,40,25,1,11,79,42,49,46,80,14,41,75,10,84,67,94,91,83,51,41,78,57,75,10,71,33,47,69,34,5,81,26,82,39,51,55,38,23,2,87,54,45,3,34,44,65,54,5,74,3,51,18,42,37,52,20,57,80,66,91,66,62,38,56,36,77,18,27,55,97,43,53,25,92,14,55,87,91,81,33,65,12,18,76,21,77,90,40,35,36,30,87,32,12,86,10,93,49,12,25,44,15,37,11,57,2,2,16,21,58,35,77,26,15,86,49,62,57,90,8,10,81,35,85,25,76,76,61,40,69,9,34,59,29,16,71,41,61,87,62,17,37,51,14,59,67,66,65,87,4,85,82,98,48,17,9,92,12,71,871073]

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
