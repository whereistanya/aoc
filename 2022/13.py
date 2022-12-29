#!/usr/bin/env python3

from enum import Enum
from functools import cmp_to_key
import operator

test = False
test = True

if test:
  filename = "test13b.txt"
else:
  filename = "input13.txt"

with open(filename, "r") as f:
  pairs = [x.strip() for x in f.read().split("\n\n")]

class Order(Enum):
  CORRECT = 1
  INCORRECT = 2
  INCONCLUSIVE = 3

def match_paren_index(s):
  """Take a list starting at a ( and return the index of the matching )"""
  if s[0] != "[":
    print("BUG: expected [ got", s)
    exit(1)
  stack = [s[0]]
  i = 1
  while True:
    if i >= len(s):
      print("BUG: Unexpected end of string without parens match")
      print("String was", s)
      exit(1)
    if s[i] == "[":
      stack.append(s[i])
    if s[i] == "]":
      stack.pop()
    if not stack: # stack is empty
      return i
    i += 1

def evaluate(val1, val2):
  """val1 and val2 are both vectors of strings, mostly 1 char but some multi
  char numbers"""
  print("Compare %s vs %s" % (val1, val2))
  c1 = 0 # what we've consumed up to
  c2 = 0

  # Work through tokens, evaluating as you go
  while True:
    #print(c1, len(val1))
    if c1 >= len(val1) and c2 >= len(val2):
      return Order.INCONCLUSIVE

    if c1 >= len(val1):
      #print("       Left side ran out of items, so inputs are in the right order")
      return Order.CORRECT

    if c2 >= len(val2):
      #print("       Rightside ran out of items, so inputs are NOT in the right order")
      return Order.INCORRECT

    v1 = val1[c1]
    v2 = val2[c2]
    #print("   Compare %s vs %s" % (v1, v2))

    if v1 == "[" and v2 == "[": # both lists
      #print("Both are lists")
      close1 = match_paren_index(val1[c1:])
      close2 = match_paren_index(val2[c2:])
      order = evaluate(list(val1[c1 + 1:c1 + close1 ]),
                       list(val2[c1 + 1:c2 + close2 ]))
      if order == Order.INCONCLUSIVE:
        c1 += close1 + 1 # past the close paren
        c2 += close2 + 1 # past the close paren
        continue
      else:
        return order

    if v1 == "[" and v2.isdecimal():
      close = match_paren_index(val1[c1:])
      new_val2 = ["[", v2, "]"]
      order = evaluate(list(val1[c1:c1 + close + 1]), list(new_val2))
      if order == Order.INCONCLUSIVE:
        c1 += close + 1 # past the close paren
        c2 += 1 # past the current digit
        continue
      else:
        return order

    if v2 == "[" and v1.isdecimal():
      close = match_paren_index(val2[c2:])
      new_val1 = ["[", v1, "]"]
      order = evaluate(list(new_val1), list(val2[c2:c2 + close + 1]))
      if order == Order.INCONCLUSIVE:
        c1 += 1
        c2 += close + 1 # past the close paren
        continue
      else:
        return order

    if v1.isdecimal() and v2.isdecimal(): # both numbers
      if int(v1) < int(v2):
        #print("       Left side is smaller, so inputs are in the right order")
        return Order.CORRECT
      elif int(v1) > int(v2):
        #print("       Right side is smaller, so inputs are NOT in the right order")
        return Order.INCORRECT
      else:
        c1 += 1
        c2 += 1
        continue


def vectorify(to_convert):
  v = []
  s = ""
  for c in to_convert:
    if c == "[":
      v.append(c)
    elif c.isdecimal():
      s += c
    elif c == "]":
      if s:
        v.append(s)
        s = ""
      v.append(c)
    elif c == ",":
      if s:
        v.append(s)
        s = ""
  return v

def test():
  assert(evaluate(
    vectorify("[1,1,3,1,1]"),
    vectorify("[1,1,5,1,1]")) == Order.CORRECT)

  assert(evaluate(
    vectorify("[[],[8,2,[2]],[],[[7,10]]]"),
    vectorify("[[[[6,10,10,5],4,10,9,[8,7,2,9,1]]],[]]")) == Order.CORRECT)

#test()


i = 1
total = 0
all_packets = []
for pair in pairs:
  a, b = pair.split("\n")

  p1, p2 = [vectorify(x) for x in [a, b]]
  all_packets.append(p1)
  all_packets.append(p2)
  result = evaluate(p1, p2)
  print("Pair %d: %s" % (i, result))
  if result == Order.CORRECT:
    total += i
  if result == None:
    print("BUG")
    exit(1)
  i += 1

print("Part 1:", total)

# Part 2
#all_packets.append(vectorify("[[2]]"))
#all_packets.append(vectorify("[[6]]"))

print ("Part 2")

def compare(left, right):
  print("cmp", left, right)
  order = evaluate(left, right)
  print(order)
  if order == Order.CORRECT:
    return -1
  if order == Order.INCORRECT:
    return 1
  return 0

#print(all_packets)
#print()
#print()

print(sorted(all_packets, key=cmp_to_key(compare)))


