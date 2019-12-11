#!/usr/bin/env python
# Advent of code Day 11

import collections
import itertools
import sys
import time
from threading import Event, Thread

class Computer(Thread):
  def __init__(self, name):
    # Initialise thread.
    super(Computer, self).__init__()
    self.name = name
    print "Starting Computer", self.name
    self.inputs = collections.deque([])
    self.program = {}
    self.output = 0
    self.output_computer = None
    self.relative_base = 0
    self.halted = False

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
      #print "NO INPUT for", self.name
      time.sleep(0.0001)
    return self.inputs.popleft()

  def read_value(self, index, mode):
    #print "read_value %d [mode %d]" % (index, mode)
    #print "Program is", self.program.values()
    #if index < 0:
    #  print "It's invalid to access memory at a negative address:", index
    #  sys.exit(1)
    try:
      if mode == 0:  # position mode
        #print "Index %d, value %d" % (self.program[index], self.program[self.program[index]])
        position = self.program[index]
        value = self.program[position]
        return value
      elif mode == 1: # immediate mode
        #print "Index %d, value %d" % (index, self.program[index])
        value = self.program[index]
        return value
      elif mode == 2: # relative mode
        #print "Index %d, value %d" % (index + self.relative_base,
        #                              self.program[index + self.relative_base])
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
      if opcode == 99:
        print "### HALTING ###"
        if self.output_computer:
          print "Painted", self.output_computer.painted
          self.output_computer.halt() # TODO: remove this
        self.halted = True
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

print "\nRunning!"


program = [3,8,1005,8,336,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,28,1006,0,36,1,2,5,10,1006,0,57,1006,0,68,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,63,2,6,20,10,1,106,7,10,2,9,0,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,97,1006,0,71,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,122,2,105,20,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,148,2,1101,12,10,1006,0,65,2,1001,19,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,181,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1002,8,1,204,2,7,14,10,2,1005,20,10,1006,0,19,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,236,1006,0,76,1006,0,28,1,1003,10,10,1006,0,72,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,271,1006,0,70,2,107,20,10,1006,0,81,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,303,2,3,11,10,2,9,1,10,2,1107,1,10,101,1,9,9,1007,9,913,10,1005,10,15,99,109,658,104,0,104,1,21101,0,387508441896,1,21102,1,353,0,1106,0,457,21101,0,937151013780,1,21101,0,364,0,1105,1,457,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,179490040923,1,1,21102,411,1,0,1105,1,457,21101,46211964123,0,1,21102,422,1,0,1106,0,457,3,10,104,0,104,0,3,10,104,0,104,0,21101,838324716308,0,1,21101,0,445,0,1106,0,457,21102,1,868410610452,1,21102,1,456,0,1106,0,457,99,109,2,22101,0,-1,1,21101,40,0,2,21101,0,488,3,21101,478,0,0,1106,0,521,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,483,484,499,4,0,1001,483,1,483,108,4,483,10,1006,10,515,1101,0,0,483,109,-2,2105,1,0,0,109,4,2101,0,-1,520,1207,-3,0,10,1006,10,538,21101,0,0,-3,22102,1,-3,1,21202,-2,1,2,21101,0,1,3,21101,557,0,0,1105,1,562,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,585,2207,-4,-2,10,1006,10,585,22101,0,-4,-4,1106,0,653,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,604,1,0,1106,0,562,21202,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,623,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,645,21202,-1,1,1,21101,0,645,0,106,0,520,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0]

class Robot(Thread):
  def __init__(self, computer):
    super(Robot, self).__init__()
    self.inputs = collections.deque([])
    self.name = "ROBOT"
    self.output_computer = computer
    self.x = 0
    self.y = 0
    self.facing = 0  #  up, right, down, left
    self.colors = {} # (x,y): 1/0
    self.painted = 0
    self.halted = False
    self.stop_event = Event()

  def set_inputs(self, inputs):
    for n in inputs:
      self.inputs.append(n)

  def fire_camera(self):
    color = 0 # black
    if (self.x, self.y) in self.colors:
      color = self.colors[(self.x, self.y)]
    self.output_computer.set_inputs([color])

  def turn_right(self):
    self.facing = (self.facing + 1) % 4

  def turn_left(self):
    self.facing = (self.facing - 1) % 4

  def move(self):
    if self.facing == 0: # up
      self.y -= 1
    elif self.facing == 1: # right
      self.x += 1
    elif self.facing == 2: # down
      self.y += 1
    elif self.facing == 3:
      self.x -= 1
    else:
      print "Bad facing", self.facing
      raise ValueError

  def turn_and_move(self, direction):
    #print "Was facing", self.facing
    if direction == 0:
      self.turn_left()
    elif direction == 1:
      self.turn_right()
    else:
      print "Bad direction", direction
      raise ValueError
    self.move()
    self.fire_camera()

  def next_input(self):
    while len(self.inputs) == 0 and not self.stop_event.is_set():
      time.sleep(0.0001)
    return self.inputs.popleft()

  def paint(self, color):
    if (self.x, self.y) not in self.colors:
      self.painted += 1
    self.colors[(self.x, self.y)] = color

  def halt(self):
    print "Halt called!"
    self.stop_event.set()

  def display(self):
    for x in range(0, 40):
      s = ""
      for y in range (20, -1, -1):
        if (x, y) in self.colors:
          if self.colors[(x, y)] == 1:
            s += "#"
          else:
            s += " "
      print s

  def run(self):
    while not self.stop_event.is_set():
      color = robot.next_input()
      robot.paint(color)
      direction = robot.next_input()
      robot.turn_and_move(direction)


computer.reset()
computer.set_inputs([1])
computer.set_program(program)

robot = Robot(computer)
computer.set_output(robot)
computer.start()
robot.start()

robot.join()
print "Robot done"
computer.join()
print "Computer done"

robot.display()
