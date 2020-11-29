#!/usr/bin/env python
# Advent of code Day 7

import collections
import itertools
import sys
import time
from threading import Thread

class Computer(Thread):
  def __init__(self, name):
    # Initialise thread.
    super(Computer, self).__init__()
    self.name = name
    print("Starting Computer", self.name)
    self.inputs = collections.deque([])
    self.program = []
    self.output = 0
    self.output_computer = None

    self.opcodes = {
      1: self.add,
      2: self.mul,
      3: self.inp,
      4: self.outp,
      5: self.jit,
      6: self.jif,
      7: self.lt,
      8: self.eq,
    }

  def set_program(self, program):
    self.program = program

  def set_inputs(self, inputs):
    print(self.name, ": setting inputs to", inputs)
    for n in inputs:
      self.inputs.append(n)

  def set_output(self, output_computer):
    self.output_computer = output_computer

  def next_input(self):
    while len(self.inputs) == 0:
      #print "NO INPUT for", self.name
      time.sleep(1)
    return self.inputs.popleft()

  def jit(self, modes, index):
    #print "jit", self.program[index], self.program[index + 1], self.program[index + 2], modes
    if modes[0] == 0:
      x = self.program[self.program[index + 1]]
    else:
      x = self.program[index + 1]
    if modes[1] == 0:
      y = self.program[self.program[index + 2]]
    else:
      y = self.program[index + 2]

    if x != 0:
      return y
    else:
      return index + 3

  def jif(self, modes, index):
    #print "jif", self.program[index], self.program[index + 1], self.program[index + 2], modes
    if modes[0] == 0:
      x = self.program[self.program[index + 1]]
    else:
      x = self.program[index + 1]
    if modes[1] == 0:
      y = self.program[self.program[index + 2]]
    else:
      y = self.program[index + 2]

    if x == 0:
        return y
    else:
      return index + 3

  def lt(self, modes, index):
    #print "lt", self.program[index], self.program[index + 1], self.program[index + 2], modes
    if modes[0] == 0:
      x = self.program[self.program[index + 1]]
    else:
      x = self.program[index + 1]
    if modes[1] == 0:
      y = self.program[self.program[index + 2]]
    else:
      y = self.program[index + 2]

    if x < y:
      self.program[self.program[index + 3]] = 1
    else:
      self.program[self.program[index + 3]] = 0
    return index + 4

  def eq(self, modes, index):
    #print "lt", self.program[index], self.program[index + 1], self.program[index + 2], modes
    if modes[0] == 0:
      x = self.program[self.program[index + 1]]
    else:
      x = self.program[index + 1]
    if modes[1] == 0:
      y = self.program[self.program[index + 2]]
    else:
      y = self.program[index + 2]

    if x == y:
      self.program[self.program[index + 3]] = 1
    else:
      self.program[self.program[index + 3]] = 0
    return index + 4

  def inp(self, modes, index):
    #print "inp:", self.program[index], self.program[index + 1], modes
    #print "Enter input! "
    #value = int(input())
    value = self.next_input()
    print("%s: INPUT: %d" % (self.name, value))
    #print "Accepting input %d" % value
    self.program[self.program[index + 1]] = value
    return index + 2

  def outp(self, modes, index):
    if modes[0] == 0:
      n = self.program[self.program[index + 1]]
    else:
      n = self.program[index + 1]
    print("%s: Diagnostic code: %d" % (self.name, n))
    self.output = n
    self.output_computer.set_inputs([n])
    return index + 2


  def mul(self, modes, index):
    #print "mul", self.program[index], self.program[index + 1], self.program[index + 2], modes
    if modes[0] == 0:
      x = self.program[self.program[index + 1]]
    else:
      x = self.program[index + 1]
    if modes[1] == 0:
      y = self.program[self.program[index + 2]]
    else:
      y = self.program[index + 2]

    n = x * y
    self.program[self.program[index + 3]] = n
    return index + 4

  def add(self, modes, index):
    #print "add", self.program[index], self.program[index + 1], self.program[index + 2], modes
    if modes[0] == 0:
      x = self.program[self.program[index + 1]]
    else:
      x = self.program[index + 1]
    if modes[1] == 0:
      y = self.program[self.program[index + 2]]
    else:
      y = self.program[index + 2]

    n = x + y
    self.program[self.program[index + 3]] = n
    print("%s %d + %d = %d" % (self.name, x, y, n))
    return index + 4

  def run(self):
    """Expects program as a comma separated string of integers"""
    #print "Running for", len(self.program), " values."
    index = 0

    while True:
      n = self.program[index]
      opcode, modes = self.parse(n)
      #print self.name, "==> [", index, "]", n, opcode, modes
      if opcode == 99:
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

computer.set_inputs([1,5,4])
computer.set_output(computer)
assert computer.next_input() == 1
assert computer.next_input() == 5
assert computer.next_input() == 4

"""
print "\nTest 1"
computer.set_program([1,9,10,3,2,3,11,0,99,30,40,50])
computer.add([0,0,0], 0)
assert(computer.program == [1,9,10,70,2,3,11,0,99,30,40,50])

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
"""
program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5] 


"""
highest = 0
for order in itertools.permutations([0, 1, 2, 3, 4]):
  print order
  run(program, list(order))
  if computer.output > highest:
    highest = computer.output
  print computer.output
print "Highest signal is", highest
"""

#program = [ 3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
#27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

highest = 0

#for order in itertools.permutations([9, 8, 7, 6, 5]):
computer1 = Computer("A")
computer2 = Computer("B")
computer3 = Computer("C")
computer4 = Computer("D")
computer5 = Computer("E")

order = [9, 8, 7, 6, 5]
print(order)


computer1.set_inputs([order[0], 0])
computer1.set_program(list(program))
computer1.set_output(computer2)

computer2.set_inputs([order[1]])
computer2.set_program(list(program))
computer2.set_output(computer1)

#computer3.set_inputs([order[2]])
#computer3.set_program(list(program))
#computer3.set_output(computer4)
#
#computer4.set_inputs([order[3]])
#computer4.set_program(list(program))
#computer4.set_output(computer5)
#
#computer5.set_inputs([order[4]])
#computer5.set_program(list(program))
#computer5.set_output(computer1)
#
computer1.start()
computer2.start()
#computer3.start()
#computer4.start()
#computer5.start()

computer1.join()
computer2.join()
#computer3.join()
#computer4.join()
#computer5.join()


"""
print computer5.output
  if computer5.output > highest:
    highest = computer5.output


print "Highest signal is", highest
"""
