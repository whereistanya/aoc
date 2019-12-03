#!/usr/bin/env python
# Advent of code Day 1.


def mul(values, index):
  n = values[values[index + 1]] * values[values[index + 2]]
  values[values[index + 3]] = n
  return 4

def add(values, index):
  n = values[values[index + 1]] + values[values[index + 2]]
  values[values[index + 3]] = n
  return 4

def testrun(program):
  # Turn the program into an array of ints
  values = list(map(int, program.strip().split(",")))
  output = run(values)
  # Return the program solution as a string for easy testing.
  return ','.join(map(str, output))


def run(values):
  """Expects program as a comma separated string of integers"""

  opcodes = {
    1: add,
    2: mul,
  }
  index = 0

  while True:
    opcode = values[index]
    if opcode == 99:
      break

    opfunc = opcodes[opcode]
    move = opfunc(values, index)
    index += move
  return values

def reset(program, override=[]):
  # Converting this string a ton of times is stupid but whatevs.
  values = list(map(int, program.strip().split(",")))
  if override:
    if len(override) != 2:
      print("Weird override:", override)
    values[1] = override[0]
    values[2] = override[1]
  return values

# main

# Run tests
v = [1,9,10,3,2,3,11,0,99,30,40,50]
add(v, 0)
assert(v == [1,9,10,70,2,3,11,0,99,30,40,50])
mul(v, 4)
assert(v == [3500,9,10,70,2,3,11,0,99,30,40,50])
assert testrun("1,9,10,3,2,3,11,0,99,30,40,50") == "3500,9,10,70,2,3,11,0,99,30,40,50"
assert testrun("1,0,0,0,99") == "2,0,0,0,99"
assert testrun("2,3,0,3,99") == "2,3,0,6,99"
assert testrun("2,4,4,5,99,0") == "2,4,4,5,99,9801"
assert testrun("1,1,1,4,99,5,6,0,99") == "30,1,1,4,2,5,6,0,99"
print "Tests passed."

program = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,10,19,23,1,6,23,27,1,5,27,31,1,10,31,35,2,10,35,39,1,39,5,43,2,43,6,47,2,9,47,51,1,51,5,55,1,5,55,59,2,10,59,63,1,5,63,67,1,67,10,71,2,6,71,75,2,6,75,79,1,5,79,83,2,6,83,87,2,13,87,91,1,91,6,95,2,13,95,99,1,99,5,103,2,103,10,107,1,9,107,111,1,111,6,115,1,115,2,119,1,119,10,0,99,2,14,0,0"
values = reset(program, override=[12, 2])
print run(values)[0]

for i in range(1, 100):
  for j in range(1, 100):
    values = reset(program, override=[i, j])
    output = run(values)[0]
    if output == 19690720:
      print 100 * i + j
      break
