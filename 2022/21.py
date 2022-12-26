#!/usr/bin/env python3

import operator

test = False
test = True

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
def translate(root, to_find):
  new_root = []
  i = 0
  print(root)
  #if len(root) > 5 and root[0] == "(" and root[-1] == ")":
  #  root = root[1:-1]
  #  print("trimmed")
  while i < len(root):
    piece = root[i]
    if piece in to_find:
      if len(to_find[piece]) == 1:
        new_root.extend(to_find[piece])
      else:
        new_root.append("(")
        new_root.extend(to_find[piece])
        new_root.append(")")
    elif (piece == "(" and
          root[i + 1].isdecimal() and
          root[i + 2] in ["-", "+", "*", "/"] and
          root[i + 3].isdecimal() and
          root[i + 4] == ")"):
      ops = {
        "+": operator.add,
        "*": operator.mul,
        "-": operator.sub,
        "/": operator.floordiv,
      }
      val = ops[root[i + 2]](int(root[i + 1]), int(root[i + 3]))
      new_root.append(str(val))
      i += 4
    else:
      new_root.append(piece)
    i += 1
  return new_root

found = {}
#to_find["root"][1] = "=" 
sidea = to_find["root"][0]
sideb = to_find["root"][2]
to_find.pop("humn")
#to_find["humn"] = ["301"]
root = []
#new_root = to_find["root"]
#to_find.pop("root")

before = []
after = [sidea]
while(before != after):
  before = after
  after = translate(before, to_find)
  print(after)
sidea = after

before = []
after = [sideb]
while(before != after):
  before = after
  after = translate(before, to_find)
  print(after)
sideb = after

print(" ".join((sidea)))
print(" ".join((sideb)))
