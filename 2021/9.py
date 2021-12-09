#!/usr/bin/env python

inputfile = "input.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]


def test_input(): 
  lines = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
  return [x.strip() for x in lines.split("\n")]


def map_patterns(patterns):
  found = {}
  available = set(patterns)

  # 1, 4, 7, 8
  for pattern in patterns:
    if len(pattern) == 2:
      found[1] = pattern
      available.remove(pattern)
    if len(pattern) == 3:
      found[7] = pattern
      available.remove(pattern)
    if len(pattern) == 4:
      found[4] = pattern
      available.remove(pattern)
    if len(pattern) == 7:
      found[8] = pattern
      available.remove(pattern)

  found['a'] = set(list(found[7])) - set(list(found[1]))

  # 3, 9
  for pattern in patterns:
    if pattern not in available:
      continue
    if len(pattern) == 5:
      if all(x in pattern for x in found[1]): 
        found[3] = pattern
        available.remove(pattern)

    if len(pattern) == 6:
      if all(x in pattern for x in found[4]): 
        found[9] = pattern
        available.remove(pattern)

  # 0, 6
  for pattern in patterns:
    if pattern not in available:
      continue
    if len(pattern) == 6:
      if all(x in pattern for x in found[1]): 
        found[0] = pattern
        available.remove(pattern)
      else:
        found[6] = pattern
        available.remove(pattern)

  found['d'] = set(list(found[9])) - set(list(found[0]))
  found['b'] = set(list(found[4])) - set(list(found[1])) - found['d']

  # 2 and 5 are left
  for pattern in patterns:
    if pattern not in available:
      continue
    if len(pattern) == 5:
      if all(x in pattern for x in found['b']):
        found[5] = pattern
        available.remove(pattern)
      else:
        found[2] = pattern
        available.remove(pattern)

  if available:
    print("BUG:", available)
    exit()

  return found


#lines = test_input()

sum = 0

for line in lines:
  p, o = line.split("|")
  patterns = [x.strip() for x in p.split()]

  found = map_patterns(patterns)
  codes = {}
  for k in found:
    v = str(sorted(found[k]))
    codes[v] = k

  output = [str(sorted(x.strip())) for x in o.split()]
  outstr = ""
  for digit in output:
    outstr += str(codes[digit])
  sum += int(outstr)

print sum
