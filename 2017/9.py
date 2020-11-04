#!/usr/bin/env python
# Advent of code Day 9

def remove_garbage(chars):
  """Return string without garbage, garbage count"""
  newst = ""
  garbage = False
  escaped = False
  garbage_count = 0
  for char in chars:
    if escaped:
      escaped = False
      continue
    if char == "!":
      escaped = True
      continue

    if char == '<':
      if garbage:
        garbage_count += 1
      garbage = True
      continue
    if char == '>':
      garbage = False
      continue
    if garbage:
      garbage_count += 1
      continue
    newst += char
  return newst, garbage_count

def score(chars):
  print chars
  chars = remove_garbage(chars)[0]
  print chars
  score = 0
  depth = 0
  for char in chars:
    if char == "{":
      depth += 1
    if char == "}":
      score += depth
      depth -= 1
    if depth < 0:
      print "Uh, UNEXPECTED"
      exit()
  return score


with open("input9.txt", "r") as f:
  chars = f.read().strip() #

assert remove_garbage("{{{},{},{{}}}}")[0].count("}") == 6
assert remove_garbage("{<a>,<a>,<a>,<a>}")[0].count("}") == 1
assert remove_garbage("{{<a>},{<a>},{<a>},{<a>}}")[0].count("}") == 5
assert remove_garbage("{{<!>},{<!>},{<!>},{<a>}}")[0].count("}") == 2

assert remove_garbage("<>")[1] == 0
assert remove_garbage("<random characters>")[1] == 17
assert remove_garbage("<<<<>")[1] == 3
assert remove_garbage("<{!>}>")[1] == 2
assert remove_garbage("<!!>")[1] == 0
assert remove_garbage("<!!!>>")[1] == 0
assert remove_garbage("<{o\"i!a,<{i<a>")[1] == 10


assert score("{}") == 1
assert score("{{{}}}") == 6
assert score("{{},{}}") == 5
assert score("{{{},{},{{}}}}") == 16
assert score("{<a>,<a>,<a>,<a>}") == 1
assert score("{{<ab>},{<ab>},{<ab>},{<ab>}}") == 9
assert score("{{<!!>},{<!!>},{<!!>},{<!!>}}") == 9
assert score("{{<a!>},{<a!>},{<a!>},{<ab>}}") == 3

print score(chars)

print remove_garbage(chars)[1]


