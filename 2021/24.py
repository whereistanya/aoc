#!/usr/bin/env python

import math

inputfile = "input24.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

def test():
  lines = """inp z
inp x
mul z 3
eql z x""".split("\n")
  return lines


class ALU(object):
  def __init__(self, lines):
    self.lines = lines
    self.reset()
    self.model = 0
    self.instructions = []
    for line in lines:
      tokens = line.split()
      self.instructions.append((tokens[0], tokens[1:]))

  def reset(self):
    self.index = 0
    self.registers = {"w":0, "x": 0, "y": 0, "z":0}

  def read_input(self):
    value = int(self.model[self.index])
    self.index += 1
    return value

  def get_value(self, x):
    if x in self.registers:
      return self.registers[x]
    else:
      return int(x)

  def inp(self, args):
    a = args[0]
    print("inp %s" % a)
    self.registers[a] = self.read_input()  # read an input value
    #print("=> Read %d into %s" % (self.registers[a], a))
    print


  def add(self, args):
    a, b = args
    print("add %s %s" % (a, b))
    self.registers[a] = self.registers[a] + self.get_value(b)

  def mul(self, args):
    a, b = args
    print("mul %s %s" % (a, b))
    self.registers[a] = self.registers[a] * self.get_value(b)

  def div(self, args):
    a, b = args
    print("div %s %s" % (a, b))
    self.registers[a] = int(math.floor((1.0 * self.registers[a]) / self.get_value(b)))

  def mod(self, args):
    a, b = args
    print("mod %s %s" % (a, b))
    self.registers[a] = self.registers[a] % self.get_value(b)

  def eql(self, args):
    a, b = args
    print("eql %s %s?" % (a, b))
    if self.get_value(a) == self.get_value(b):
      self.registers[a] = 1
    else:
      self.registers[a] = 0

  def run_decompiled(self, model):
    vals = [int(x) for x in model]

    z = vals[0] + 7
    z = (z * 26) + 4 + vals[1]
    z = (z * 26) + 8 + vals[2]
    if vals[3] == (z % 26) - 4:
      z = z / 26
    else:
      z = (z / 26) * 26 + 1 + vals[3]
    z = z * 26 + vals[4] + 5
    z = z * 26 + vals[5] + 14
    z = z * 26 + vals[6] + 12

    if vals[7] == (z % 26) - 9:
      z = z / 26
    else:
      z = (z / 26) * 26 + 10 + vals[7]

    if vals[8] == (z % 26) - 9:
      z = z / 26
    else:
      z = (z / 26) * 26 + 5 + vals[8]
    z = z * 26 + vals[9] + 7

    # TODO: If there's a bug, it's here.
    if vals[10] == (z % 26) - 15:
      z = z / 26
    else:
      z = (z / 26) * 26 + 6 + vals[10]


    if vals[11] == (z % 26) - 7:
      z = z / 26
    else:
      z = (z / 26) * 26 + 8 + vals[11]


    if vals[12] == (z % 26) - 10:
      z = z / 26
    else:
      z = (z / 26) * 26 + 4 + vals[12]

    if z < 26 and vals[13] == z % 26:
      print "Yay!"
      return 0
    else:
      return -1

  def find_valid_numbers(self):
    for i in range(9, 0, -1):
      for j in range(9, 0, -1):
        for k in range(9, 0, -1):
          # steps 1 - 3
          z = i + 7
          z = z * 26 + 4 + j
          z = z * 26 + 8 + k

          # digit 4 has to decrease the size of z, so it has to match the
          # if statement "if w == (z % 26) - 4"
          v1 = z % 26 - 4
          if v1 > 9:
            continue
          if v1 <= 0:
            continue
          z = z / 26

          for l in range(9, 0, -1):
            for m in range(9, 0, -1):
              for n in range(9, 0, -1):
                z1 = 26 * (26 * ((z * 26) + l + 5) + m + 14) + n + 12

                v2 = (z1 % 26) - 9
                if v2 > 9:
                  continue
                if v2 <= 0:
                  continue
                z1 = z1 / 26

                v3 = (z1 % 26) - 9
                if v3 > 9:
                  continue
                if v3 <= 0:
                  continue
                z1 = z1 / 26

                for o in range(9, 0, -1):
                  z2 = z1 * 26 + o + 7

                  v4 = z2 % 26 - 15
                  if v4 > 9:
                    continue
                  if v4 <= 0:
                    continue
                  z2 /= 26

                  v5 = (z2 % 26) - 7
                  if v5 > 9:
                    continue
                  if v5 <= 0:
                    continue
                  z2 /= 26

                  v6 = (z2 % 26) - 10
                  if v6 > 9:
                    continue
                  if v6 <= 0:
                    continue
                  z2 /= 26

                  if z2 > 26:
                    continue
                  v7 = z2 % 26

                  if v7 > 9:
                    continue
                  if v7 <= 0:
                    continue
                  print ''.join([str(x) for x in i,j,k,v1,l,m,n,v2,v3,o,v4,v5,v6,v7])




  def run(self, model):
    # model is a 14 digit number
    fns = {
      "inp": self.inp,
      "add": self.add,
      "mul": self.mul,
      "div": self.div,
      "mod": self.mod,
      "eql": self.eql,
    }

    self.model = model
    for instruction, args in self.instructions:
      fn = fns[instruction]
      fn(args)
      print self.registers
    self.run_decompiled(model)
    return self.registers["z"]

#lines = test()
alu = ALU(lines)

alu.find_valid_numbers()
exit()

i = 99999999999999
i = 99979469999999
i = 9997926979196
i = 29939469991739
i = 29599469991739

alu.run(str(i))

exit()

#i = 99979469910

while True:
  s = str(i)
  if "0" in s:
    if i % 1000000 == 0:
      print i
    i -= 1
    continue
  output = alu.run_decompiled(s)
  if output == 0:
    break
  i -= 1

exit()

while True:
  alu.reset()
  output = alu.run(s)
  if s == "0":
    print (s)
    break
  i -= 1

