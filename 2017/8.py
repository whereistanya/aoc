#!/usr/bin/env python

with open("input8.txt", "r") as f:
  lines = f.readlines()

"""
lines = [
  "b inc 5 if a > 1",
  "a inc 1 if b < 5",
  "c dec -10 if a >= 1",
  "c inc -20 if c == 10",
]
"""

registers = {}
highest_register_ever = 99999

def gt(x, y):
  return x > y

def ge(x, y):
  return x >= y

def lt(x, y):
  return x < y

def le(x, y):
  return x <= y

def eq(x, y):
  return x == y

def ne(x, y):
  return x != y

for line in lines:
  reg1, op, val1, ifstatement, reg2, compare, val2 = line.strip().split()
  val1 = int(val1)
  val2 = int(val2)

  if reg1 not in registers:
    registers[reg1] = 0
  if reg2 not in registers:
    registers[reg2] = 0

  cmp_fns = {
    ">" : gt,
    ">=": ge,
    "<" : lt,
    "<=": le,
    "==": eq,
    "!=": ne,
  }
  assert ifstatement == "if"
  assert op in ["inc", "dec"]

  cmp_fn = cmp_fns[compare]
  if cmp_fn(registers[reg2], val2):
    if op == "inc":
      registers[reg1] += val1
    elif op == "dec":
      registers[reg1] -= val1

    if registers[reg1] > highest_register_ever:
      highest_register_ever = registers[reg1]


print("Part 1", sorted(registers.values())[len(registers) - 1])
print("Part 2", highest_register_ever)
