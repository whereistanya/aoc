#!/usr/bin/env python
# Advent of code Day 5.

def jit(values, modes, index):
  print("jit", values[index], values[index + 1], values[index + 2], modes)
  if modes[0] == 0:
    x = values[values[index + 1]]
  else:
    x = values[index + 1]
  if modes[1] == 0:
    y = values[values[index + 2]]
  else:
    y = values[index + 2]

  if x != 0:
    return y
  else:
    return index + 3

def jif(values, modes, index):
  print("jif", values[index], values[index + 1], values[index + 2], modes)
  if modes[0] == 0:
    x = values[values[index + 1]]
  else:
    x = values[index + 1]
  if modes[1] == 0:
    y = values[values[index + 2]]
  else:
    y = values[index + 2]

  if x == 0:
      return y
  else:
    return index + 3

def lt(values, modes, index):
  print("lt", values[index], values[index + 1], values[index + 2], modes)
  if modes[0] == 0:
    x = values[values[index + 1]]
  else:
    x = values[index + 1]
  if modes[1] == 0:
    y = values[values[index + 2]]
  else:
    y = values[index + 2]

  if x < y:
    values[values[index + 3]] = 1
  else:
    values[values[index + 3]] = 0
  return index + 4

def eq(values, modes, index):
  print("lt", values[index], values[index + 1], values[index + 2], modes)
  if modes[0] == 0:
    x = values[values[index + 1]]
  else:
    x = values[index + 1]
  if modes[1] == 0:
    y = values[values[index + 2]]
  else:
    y = values[index + 2]

  if x == y:
    values[values[index + 3]] = 1
  else:
    values[values[index + 3]] = 0
  return index + 4

def inp(values, modes, index):
  print("inp:", values[index], values[index + 1], modes)
  print("Enter input! ")
  value = int(eval(input()))
  values[values[index + 1]] = value
  return index + 2

def outp(values, modes, index):
  if modes[0] == 0:
    n = values[values[index + 1]]
  else:
    n = values[index + 1]
  print("Diagnostic code:", n)
  return index + 2


def mul(values, modes, index):
  print("mul", values[index], values[index + 1], values[index + 2], modes)
  if modes[0] == 0:
    x = values[values[index + 1]]
  else:
    x = values[index + 1]
  if modes[1] == 0:
    y = values[values[index + 2]]
  else:
    y = values[index + 2]

  n = x * y
  values[values[index + 3]] = n
  return index + 4

def add(values, modes, index):
  print("add", values[index], values[index + 1], values[index + 2], modes)
  if modes[0] == 0:
    x = values[values[index + 1]]
  else:
    x = values[index + 1]
  if modes[1] == 0:
    y = values[values[index + 2]]
  else:
    y = values[index + 2]

  n = x + y
  values[values[index + 3]] = n
  return index + 4

def run(values):
  """Expects program as a comma separated string of integers"""
  print("Running for", len(values), " values.")

  opcodes = {
    1: add,
    2: mul,
    3: inp,
    4: outp,
    5: jit,
    6: jif,
    7: lt,
    8: eq,
  }
  index = 0

  while True:
    n = values[index]
    opcode, modes = parse(n)
    print("==> [", index, "]", n, opcode, modes)
    if opcode == 99:
      break

    opfunc = opcodes[opcode]
    index = opfunc(values, modes, index)
  return values

def parse(number):
  mode = [0, 0, 0]
  opcode = number % 100
  number /= 100

  for i in range(0, 3):
    m = number % 10
    if m == 1:
      mode[i] = 1
    number /= 10
  return opcode, mode

# Run tests
assert parse(1002) == (0o2, [0, 1, 0])
assert parse(1104) == (0o4, [1, 1, 0])
assert parse(104) == (0o4, [1, 0, 0])

############

# main

print("Tests passed.")

program = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,27,28,225,1,113,14,224,1001,224,-34,224,4,224,102,8,223,223,101,7,224,224,1,224,223,223,1102,52,34,224,101,-1768,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1002,187,14,224,1001,224,-126,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1102,54,74,225,1101,75,66,225,101,20,161,224,101,-54,224,224,4,224,1002,223,8,223,1001,224,7,224,1,224,223,223,1101,6,30,225,2,88,84,224,101,-4884,224,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,1001,214,55,224,1001,224,-89,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,1101,34,69,225,1101,45,67,224,101,-112,224,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1102,9,81,225,102,81,218,224,101,-7290,224,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,1101,84,34,225,1102,94,90,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1007,677,677,224,102,2,223,223,1005,224,329,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,1008,677,677,224,102,2,223,223,1005,224,359,101,1,223,223,8,226,677,224,1002,223,2,223,1006,224,374,101,1,223,223,108,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,404,1001,223,1,223,7,226,677,224,1002,223,2,223,1005,224,419,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,434,1001,223,1,223,1107,226,226,224,1002,223,2,223,1006,224,449,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,464,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,479,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,494,1001,223,1,223,1007,226,677,224,1002,223,2,223,1006,224,509,1001,223,1,223,108,226,226,224,1002,223,2,223,1006,224,524,1001,223,1,223,1108,677,226,224,102,2,223,223,1006,224,539,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,554,101,1,223,223,107,226,677,224,1002,223,2,223,1006,224,569,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,584,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,599,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,614,1001,223,1,223,107,226,226,224,1002,223,2,223,1005,224,629,101,1,223,223,7,226,226,224,102,2,223,223,1006,224,644,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,659,101,1,223,223,108,677,677,224,102,2,223,223,1005,224,674,1001,223,1,223,4,223,99,226]

run(program)
