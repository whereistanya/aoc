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

program = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,10,23,2,13,23,27,1,5,27,31,2,6,31,35,1,6,35,39,2,39,9,43,1,5,43,47,1,13,47,51,1,10,51,55,2,55,10,59,2,10,59,63,1,9,63,67,2,67,13,71,1,71,6,75,2,6,75,79,1,5,79,83,2,83,9,87,1,6,87,91,2,91,6,95,1,95,6,99,2,99,13,103,1,6,103,107,1,2,107,111,1,111,9,0,99,2,14,0,0"

for i in range(1, 100):
  for j in range(1, 100):
    values = reset(program, override=[i, j])
    output = run(values)[0]
    if output == 19690720:
      print 100 * i + j
      break
