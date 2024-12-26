#!/usr/bin/env python

# Make graphviz file with:
# ./24.py gv > wires.dot ; dot -Tpng -o wires.png wires.dot

from functools import partial
import sys

filename = "input.txt"
#filename = "test.txt"

# Note to me: the test code does a bitwise AND. The real code is doing
# addition. It's a different machine.

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

DEBUG = False


class Wire(object):
  def __init__(self, name, val=-1):
    self.name = name
    self.val = val
    self.valfn = partial(print, "nope, no function set for %s" % self.name)
    self.computer = None
    self.loopdetected = False

  def __repr__(self):
    return "Wire(%s)" % (self.name)

  def value(self): # input to this wire
    if self.val != -1:
      return self.val
    val = self.valfn() # a partial already loaded with 2 other wires. Magic!
    return val

  def AND(self, a, b):
    return a.value() and b.value()

  def OR(self, a, b):
    return a.value() or b.value()

  def XOR(self, a, b):
    return a.value() ^ b.value()

# Computer represents a bunch of wires with inputs and outputs
class Computer(object):
  def __init__(self):
    self.wires = {}
    self.needed = []
    self.maxz = 0

  def getWire(self, name, val=-1):
    """Fetch an existing wire or create a new one."""
    if name in self.wires:
      return self.wires[name]
    wire = Wire(name, val)
    wire.computer = self
    self.wires[name] = wire
    if name.startswith("z"):
      number = int(name[1:])
      if number > self.maxz:
        self.maxz = number
    return wire

  def swap(self, name1, name2):
    """Swap the "values" (actually the inputs) of two wires."""
    print("swap", name1, name2)
    w1 = self.wires[name1]
    w2 = self.wires[name2]
    tmp = w1.valfn
    w1.valfn = w2.valfn
    w2.valfn = tmp

  def testoutput(self):
    """ Calculate whether the output is correct."""
    dec1, _ = self.input1()
    dec2, _ = self.input2()
    out, _ = self.output()

    if dec1 & dec2 == out:
      print("Yes! %d & %d = %d" % (dec1, dec2, out))
      return True
    else:
      print("No! %d & %d != %d" % (dec1, dec2, out))
      return False

  def input1(self):
    """Assemble and return the x wire input. Returns both binary string and decimal."""
    xs = {}
    for k in self.wires:
      if k.startswith("x"):
        xs[k] = str(self.wires[k].value())
    xkeys = sorted(xs.keys(), reverse=True)
    input1 = ""
    for x in xkeys:
      input1 += xs[x]
    return int(input1, 2), input1

  def input2(self):
    """Assemble and return the y wire input. Returns both binary string and decimal."""
    ys = {}
    for k in self.wires:
      if k.startswith("y"):
        ys[k] = str(self.wires[k].value())
    ykeys = sorted(ys.keys(), reverse=True)
    input2 = ""
    for y in ykeys:
      input2 += ys[y]
    return int(input2, 2), input2

  def output(self):
    """Assemble and return the output from the z wires. Returs both binary string and decimal."""
    zs = {}
    for k in self.wires:
      if k.startswith("z"):
        zs[k] = str(self.wires[k].value())
    zkeys = sorted(zs.keys(), reverse=True)
    output = ""
    for z in zkeys:
      output += zs[z]
    return int(output, 2), output

  def get(self, wire):
    """Return the value of any wire. Just shorthand."""
    return(self.wires[wire].value())

  def set(self, wire, val, verbose=True):
    if verbose:
      print("Setting %s to %d" % (wire, val))
    self.wires[wire].val = val

  def flip(self, wire):
    print("Flipping %s" % (wire))
    val = self.get(wire)
    if val == 0:
      self.set(wire, 1)
    else:
      self.set(wire, 0)

  def ok_we_re_doing_this_manually(self, verbose):
    # we need to swap output wires for 4 pairs of the wires until this becomes true:
    # and we need to be able to switch the input values (x and y wires) and have it still
    # generate the right output (z wires).
    # finding the wires manually with this handy helper function.
    decimalx, binaryx = self.input1()
    decimaly, binaryy = self.input2()
    decimalz, binaryz = self.output() # What the computer calculated on the z wires

    #if decimalx & decimaly == decimalz: # for the test code
    if decimalx + decimaly == decimalz:
      print("Good wiring! %d & %d = %d" % (decimalx, decimaly, decimalz))
    else:
      print("Bad wiring! %d & %d != %d" % (decimalx, decimaly, decimalz))

    correct = "{0:b}".format(decimalx + decimaly) # add them and format as bbinary string
    # The test code machine is doing a bitwise AND instead. Different correct value.
    # correct = "{0:b}".format(decimalx + decimaly) # binary string
    if verbose:
      print("inputx  :", binaryx.zfill(46), decimalx)
      print("inputy  :", binaryy.zfill(46), decimaly)
      print("out want:", correct.zfill(46))
      print("out got :", binaryz.zfill(46), decimalz)

    # reverse the outputs we want and have because otherwise there's off-by-one
    # chaos when we carry a 1 and increase the size of the output
    outwant = correct[::-1]
    outgot = binaryz[::-1]
    wrongs = []
    # print out z from 00 to 45. Starts at the right hand side of binaryz!
    for i in range(len(binaryz)): # from z00 to Z45
      wirename = "z%0.2d" % i
      ok = "."
      try:
        got = outgot[i]
      except IndexError:
        got = "_"
      try:
        want = outwant[i]
      except IndexError:
        want = "0"

      if got != want:
        ok = "#"
        wrongs.append(wirename)
      try:
        wire = self.wires[wirename]
        fn = wire.valfn
      except KeyError:
        fn = "NO WIRE"
      if verbose:
        print(ok, wirename, "wanted", want, "got", got, "fn:", fn)
    print("Wrongs:", wrongs)
    return decimalx + decimaly == decimalz




computer = Computer()

# Generate a graphviz graph. If the first arg is "gv", just do that and exit.
opi = 0
print ("digraph {")
print ("rankdir = LR")
for line in lines:
  if line == "":
    continue
  if ":" in line: # raw value
    w1, val = line.split(":")
    computer.getWire(w1, int(val))
  else:
    w1, op, w2, _, w3 = line.split()
    wire1 = computer.getWire(w1)
    wire2 = computer.getWire(w2)
    wire3 = computer.getWire(w3)
    opname = "%s%d" % (op, opi)
    print(w3, "->", opname)
    print(opname, "->", w1)
    print(opname, "->", w2)
    opi += 1

    fns = {
      "AND": partial(wire3.AND, wire1, wire2),
      "OR": partial(wire3.OR, wire1, wire2),
      "XOR": partial(wire3.XOR, wire1, wire2)
    }
    wire3.valfn = fns[op]
print ("}")

if len(sys.argv) > 1 and sys.argv[1] == "gv":
  exit()

print("### Part 1")
part1 = computer.output()
print("Part 1:", part1)

print()
print()
print("### Part 2")

# For test input, swapping these wires should make computer.testoutput() return True.
# not swapping them should make it say false. But for the test input change the checks in
# ok_we_re_doing_this_manually too.
#computer.ok_we_re_doing_this_manually(True)
#computer.swap("z00", "z05")
#computer.swap("z01", "z02")
#computer.ok_we_re_doing_this_manually(True)

# set all y to 0
for i in range(45):
  wirename = "y%0.2d" % i
  computer.set(wirename, 0, verbose=False)
# set all x to 0
  wirename = "x%0.2d" % i
  computer.set(wirename, 0, verbose=False)

#computer.set("x00", 1)
#computer.set("y01", 1)

# What needs to swap:
#computer.swap("z05", "bpf")
#
#computer.swap("z11", "hcc")
#computer.swap("qcw", "hqc")
#computer.swap("fdw", "z35")

wrong = []
for i in range(45):
  w = "x%02d" % i
  computer.set(w, 1)
  ok = computer.ok_we_re_doing_this_manually(False)
  print("wire", w, ok)
  if not ok:
    wrong.append(w)
  computer.set(w, 0)

computer.ok_we_re_doing_this_manually(True)
print(wrong)

# print any wires that were listed on the command line
if len(sys.argv) > 1:
  for wire in sys.argv[1:]:
    print("[%s]: %d  %s" % (wire, computer.get(wire), computer.wires[wire].valfn))
