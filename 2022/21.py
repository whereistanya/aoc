#!/usr/bin/env python3

import operator

test = True
test = False

if test:
  filename = "test21.txt"
else:
  filename = "input21.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]


to_find = {}
found = {}

for line in lines:
  name, stuff = line.split(":")
  stuff = stuff.strip()
  to_find[name] = stuff.split()

# Part 1
while len(found) < len(to_find):
  for k, v in to_find.items():
    if k in found:
      continue
    if len(v) == 1:
      found[k] = int(v[0])
      continue
    name1, op, name2 = v
    if name1 in found and name2 in found:
      val1 = found[name1]
      val2 = found[name2]
      ops = {
        "+": operator.add,
        "*": operator.mul,
        "-": operator.sub,
        "/": operator.floordiv,
      }
      val = ops[op](val1, val2)
      found[k] = val

print("Part 1:", found["root"])

# Part 2
def simplify(equation, to_find):
  new_equation = []
  ops = {
    "+": operator.add,
    "*": operator.mul,
    "-": operator.sub,
    "/": operator.floordiv,
  }

  i = 0
  while i < len(equation):
    piece = equation[i]
    if piece in to_find:
      if len(to_find[piece]) == 1:
        new_equation.extend(to_find[piece])
      else:
        new_equation.append("(")
        new_equation.extend(to_find[piece])
        new_equation.append(")")
    elif (piece == "(" and
          equation[i + 1].isdecimal() and
          equation[i + 2] in ["-", "+", "*", "/"] and
          equation[i + 3].isdecimal() and
          equation[i + 4] == ")"):
      op = ops[equation[i + 2]]
      val = op(int(equation[i + 1]), int(equation[i + 3]))
      if op == "/" and int(equation[i + 1]) % int(equation[i + 3]) != 0:
        print("BUG: trying to divide %d by %d" % (equation[i + 1], equation[i + 3]))
        exit(1)
      new_equation.append(str(val))
      i += 4
    elif ((len(equation) - i) > 2 and
          equation[i].isdecimal() and
          equation[i + 1] in ["-", "+", "*", "/"] and
          equation[i + 2].isdecimal()):
      op = ops[equation[i + 1]]
      val = op(int(equation[i]), int(equation[i + 2]))
      if op == "/" and int(equation[i]) % int(equation[i + 2]) != 0:
        print("BUG: trying to divide %d by %d" % (equation[i], equation[i + 2]))
        exit(1)
      new_equation.append(str(val))
      i += 2
    else:
      new_equation.append(piece)
    i += 1
  return new_equation

def flip(op, val):
  l = []
  if op == "+":
    l = (["-", val])
  elif op == "-":
    l = (["+", val])
  elif op == "*":
    l = (["/", val])
  elif op == "/":
    l = (["*", val])
  else:
    print("BUG: unexpected op", op)
    exit(1)
  return l

def balance(side1, side2, to_find):
  # Only works when the variable is on side1.
  if side1[0] == "(" and side1[-1] == ")":
    side1 = side1[1:-1] # strip parens
  elif side1[-1].isdecimal():
    side2.extend(flip(side1[-2], side1[-1]))
    side1 = side1[0:-2]
  elif side1[0].isdecimal():
    if side1[1] in ["+", "*"]:
      side2.extend(flip(side1[1], side1[0]))
      side1 = side1[2:]
    else:
      side2 = side1[0:2] + side2
      side1 = side1[2:]
  side1 = simplify(side1, to_find)
  side2 = simplify(side2, to_find)
  return side1, side2


# Remove 'humn' and change 'root' for part 2.
side1 = [to_find["root"][0]]
side2 = [to_find["root"][2]]
to_find.pop("root")
to_find.pop("humn")

# First, simplify both sides as much as possible.
while True:
  new_side1 = simplify(side1, to_find)
  new_side2 = simplify(side2, to_find)
  if new_side1 == side1 and new_side2 == side2:
    break
  side1 = new_side1
  side2 = new_side2

# Then balance the sides, simplifying as part of the balancing.
while True:
  new_side1, side2 = balance(side1, side2, to_find)
  if new_side1 == side1:
    break
  side1 = new_side1

print("Part 2: %s = %s" % (side1, side2))
