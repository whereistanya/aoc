#!/usr/bin/env python

class Computer(object):
  def __init__(self):
    self.accumulator = 0
    self.code = []
    self.original_code = []

  def load_code(self, lines):
    self.accumulator = 0
    for line in lines:
      op, count = line.split()
      if count.startswith("+"):
        number = int(count[1:])
      else:
        number = int(count)
      self.code.append((op, number))
    self.original_code = list(self.code)

  def run(self):
    i = 0
    seen = set()
    while True:
      if i >= len(self.code):
        print("Normal completion! Accumulator is %d" % self.accumulator)
        return True
      if i in seen:
        print("Loop detected. Accumulator is %d" % self.accumulator)
        return False
      seen.add(i)
      op, arg = self.code[i]
      if op == "acc":
        self.accumulator += arg
        i += 1
      elif op == "jmp":
        i += arg
      elif op == "nop":
        i += 1

  def mutate_and_run(self):
    i = 0
    while True:
      self.accumulator = 0
      modified = False
      if self.code[i][0] == "jmp":
        self.code[i] = ("nop", self.code[i][1])
        modified = True
      elif self.code[i][0] == "nop":
        self.code[i] = ("jmp", self.code[i][1])
        modified = True
      i += 1

      if modified:
        ok = self.run()
        if ok:
          print "Yay we're done"
          exit()
        else:
          print "RESET"
          self.code = list(self.original_code)

lines = [
  "nop +0",
  "acc +1",
  "jmp +4",
  "acc +3",
  "jmp -3",
  "acc -99",
  "acc +1",
  "jmp -4",
  "acc +6",
]

inputfile = "input8.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

computer = Computer()
computer.load_code(lines)
result = computer.run()

computer.mutate_and_run()
