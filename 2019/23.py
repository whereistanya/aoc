#!/usr/bin/env python
# Advent of code Day 23

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
    if len(self.inputs) == 0:
      #print "NO INPUT for", self.name
      return -1
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
    #print "Read input: %d" % value
    out_register = self.read_output_position(index + 1, modes[0])
    self.write_value(out_register, value)
    return index + 2

  def outp(self, modes, index):
    x = self.read_value(index + 1, modes[0])
    #print "%s: Diagnostic code: %d" % (self.name, x)
    self.output = x
    if self.output_computer:
      #self.output_computer.set_inputs([x])
      self.output_computer.add_input(self.name, x)
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


class NoInputException(Exception):
  pass

class NetworkController(object):
  def __init__(self):
    #super(Robot, self).__init__()
    self.inputs = collections.deque([])
    self.name = "NetworkController"
    self.halted = False
    self.nodes = {}
    self.queues = {}
    self.nat = []

  def set_inputs(self, inputs):
    #print "Got inputs", inputs
    for n in inputs:
      self.inputs.append(n)

  def add_input(self, source, payload):
    if source not in self.queues:
      self.queues[source] = collections.deque([])
    self.queues[source].append(payload)
    if len(self.queues[source]) >= 3:
      packet = self.queues[source]
      self.set_inputs(
        [packet.popleft(), packet.popleft(), packet.popleft()])

  def next_inputs(self):
    if len(self.inputs) >= 3:
      return self.inputs.popleft(), self.inputs.popleft(), self.inputs.popleft()
    raise NoInputException

  def halt(self):
    #print self.name, ": halt called!"
    self.stop_event.set()
    self.halted = True

  def run(self):
    print "Bringing up a network with %d nodes." % (len(self.nodes))
    i = 0
    while True:
      try:
        dest, x, y = self.next_inputs()
      except NoInputException:
        #print "No network traffic. Waiting."
        time.sleep(0.05)
        i += 1
        if i > 40: # 2s
          idle = True
          for node in self.nodes:
            if len(self.nodes[node].inputs) > 0:  #HERE
              idle = False
              break
          if idle:
            self.nodes[0].set_inputs(self.nat)
            print "Sent", self.nat[1]
            i = 0
# 13748 too high
        continue
      if dest == 255:
        self.nat = [x, y]
        #print "255!", x, y
        continue
      i = 0
      out = self.nodes[dest]
      out.set_inputs([x, y])
      #print "Delivering %d %d to %s" % (x, y, out.name)
    for node in self.nodes.values():
      node.join()


# main
with open("input23.txt") as f:
  program = [int(x) for x in f.read().split(",")]
nc = NetworkController()

for i in range(0, 50):
  computer = Computer("COMPUTER%d" % i)
  computer.set_program(list(program))
  computer.set_output(nc)
  computer.set_inputs([i])
  nc.nodes[i] = computer
  computer.start()

nc.run()
