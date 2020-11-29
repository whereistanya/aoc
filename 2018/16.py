#!/usr/bin/env python
# Advent of code Day 16.

import re
import sys

line_re = "(\w+):\s*\[(\d+), (\d+), (\d+), (\d+)\]"

def read_file():
  with open("day16input.txt", "r") as f:
    lines = f.readlines()

  samples = []
  program = []

  sample_in = ""
  instruction = ""
  after = ""

  reading_samples = True
  for line in lines:
    if not reading_samples:
      instruction = []
      for i in line.strip().split():
        instruction.append(int(i))
      program.append(instruction)
      continue

    if line == "\n":
      continue
    if line.startswith("Before:"):
      if instruction:
        print("error: %s follows after:%s instruction:%s" % (line.strip(), after, instruction))
        sys.exit(1)
      # parse input
      groups = re.search(line_re, line.strip()).groups()
      if groups[0] != "Before":
        print("error in line", line)
        sys.exit()
      sample_in = [int(groups[1]), int(groups[2]), int(groups[3]), int(groups[4])]

    elif line.startswith("After"):
      if not sample_in or not instruction:
        print("error: %s follows sample_in:%s instruction:%s" % (line.strip(), sample_in, instruction))
        sys.exit(1)
      # parse output
      groups = re.search(line_re, line.strip()).groups()
      if groups[0] != "After":
        print("error in line", line)
        sys.exit()
      sample_out = [int(groups[1]), int(groups[2]), int(groups[3]), int(groups[4])]

      samples.append((sample_in, instruction, sample_out))
      sample_in = ""
      instruction = ""
    else:
      if not sample_in:
        # finished the samples. Reading the test program now.
        reading_samples = False
        instruction = []
        for i in line.strip().split():
          instruction.append(int(i))
        program.append(instruction)
        continue
      # parse numbers
      instruction = []
      for i in line.strip().split():
        instruction.append(int(i))
  return samples, program

class Computer(object):
  """A very tiny computer. Each returns a, b, c"""
  def __init__(self):
    self.registers = [0, 0, 0, 0]

  def addr(self, a, b, c):
    """stores into register C the result of adding register A and register B"""
    self.registers[c] = self.registers[a] + self.registers[b]

  def addi(self, a, b, c):
    """stores into register C the result of adding register A and value B"""
    self.registers[c] = self.registers[a] + b

  def mulr(self, a, b, c):
    """stores into register C the result of multiplying register A and register B"""
    self.registers[c] = self.registers[a] * self.registers[b]

  def muli(self, a, b, c):
    """stores into register C the result of multiplying register A and value B"""
    self.registers[c] = self.registers[a] * b

  def banr(self, a, b, c):
    """banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B."""
    self.registers[c] = self.registers[a] & self.registers[b]

  def bani(self, a, b, c):
    """bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B."""
    self.registers[c] = self.registers[a] & b

  def borr(self, a, b, c):
    """borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B"""
    self.registers[c] = self.registers[a] | self.registers[b]

  def bori(self, a, b, c):
    """bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B."""
    self.registers[c] = self.registers[a] | b

  def setr(self, a, b, c):
    """"copies the contents of register A into register C. (Input B is ignored.)"""
    self.registers[c] = self.registers[a]

  def seti(self, a, b, c):
    """seti (set immediate) stores value A into register C. (Input B is ignored.)"""
    self.registers[c] = a

  def gtir(self, a, b, c):
    """gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0."""
    if a > self.registers[b]:
      self.registers[c] = 1
    else:
      self.registers[c] = 0

  def gtri(self, a, b, c):
    """(greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0."""
    if self.registers[a] > b:
      self.registers[c] = 1
    else:
      self.registers[c] = 0

  def gtrr(self, a, b, c):
    """(greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0."""
    if self.registers[a] > self.registers[b]:
      self.registers[c] = 1
    else:
      self.registers[c] = 0

  def eqir(self, a, b, c):
    """eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0."""
    if a == self.registers[b]:
      self.registers[c] = 1
    else:
      self.registers[c] = 0

  def eqri(self, a, b, c):
    """(equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0."""
    if self.registers[a] == b:
      self.registers[c] = 1
    else:
      self.registers[c] = 0

  def eqrr(self, a, b, c):
    """equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0."""
    if self.registers[a] == self.registers[b]:
      self.registers[c] = 1
    else:
      self.registers[c] = 0


# main
samples, program = read_file()
assert len(samples) == 777
computer = Computer()

computer.registers = [0, 0, 0, 0]
computer.addi(0, 7, 3)
assert computer.registers == [0, 0, 0, 7]

#samples = [([3, 2, 1, 1], [9, 2, 1, 2], [3, 2, 2, 1]),]
#samples = [([2, 2, 1, 1], [13, 3, 3, 3], [2, 2, 1, 0])]

opfuncs = [computer.addr, computer.addi, computer.mulr, computer.muli,
           computer.banr, computer.bani, computer.borr, computer.bori,
           computer.setr, computer.seti, computer.gtir, computer.gtri,
           computer.gtrr, computer.eqir, computer.eqri, computer.eqrr]

############
# Part one #
############
threeormore = 0
for sample in samples:
  possibles = 0
  before = sample[0]
  after = sample[2]
  opcode, a, b, c = sample[1]

  for opfunc in opfuncs:
    computer.registers = [before[0], before[1], before[2], before[3]]
    opfunc(a, b, c)
    if computer.registers == after:
      possibles += 1
  if possibles >= 3:
    threeormore += 1

print("Part one:", threeormore)

############
# Part two #
############

possibles = {}  # opcode: set([possible opfuncs])
for sample in samples:
  before = sample[0]
  after = sample[2]
  opcode, a, b, c = sample[1]

  for opfunc in opfuncs:
    computer.registers = [before[0], before[1], before[2], before[3]]
    opfunc(a, b, c)
    if computer.registers == after:
      try:
        possibles[opcode].add(opfunc)
      except KeyError:
        possibles[opcode] = set([opfunc])

# Now we have a set of potentials for each opcode. First validate that none have
# no potentials. That would be a bug.
for v in list(possibles.values()):
  assert len(v) > 0

codes = {}  # opcode: opfunc
seen = set()
while len(codes) < len(possibles):
  for k, v in possibles.items():
    available = []
    for c in v:
      if c.__name__ not in seen:
        available.append(c)
    if len(available) == 1:
      codes[k] = available[0]
      #print "%d has to be %s" % (k, codes[k])
      seen.add(codes[k].__name__)

computer.registers = [0, 0, 0, 0]
for instruction in program:
  f, a, b, c = instruction
  opfunc = codes[f]
  #print "%s(%d, %d, %d)" % (opfunc.__name__, a, b, c)
  opfunc(a, b, c)

print("Part two:", computer.registers)
