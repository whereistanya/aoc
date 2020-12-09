#!/usr/bin/env python

inputfile = "input9.txt"
with open(inputfile, "r") as f:
  numbers = [int(x.strip()) for x in f.readlines()]

preamble = 25
"""
numbers = [
  35,
  20,
  15,
  25,
  47,
  40,
  62,
  55,
  65,
  95,
  102,
  117,
  150,
  182,
  127,
  219,
  299,
  277,
  309,
  576,
]

preamble = 5
"""

active = set()
i = 0
for i in range(preamble):
  active.add(numbers[i])
  i += 1


# Part 1: find the invalid number

invalid = -1

while True:
  next_number = numbers[i]
  found = False
  for j in range (i - preamble, i):
    required = next_number - numbers[j]
    if required in active:
      found = True
      break
  if not found:
    invalid = next_number
    break
  active.add(next_number)
  # TODO this can't handle duplicates?
  active.remove(numbers[i - preamble])
  i += 1

print("%d didn't work" % invalid)

# Part 2: find contiguous numbers that add to the invalid number
i = 0 # the start of the string of numbers

found = False
smallest = -1
biggest = -1
while not found:
  print "i is", i
  j = i + 1 # the index inside the string of numbers
  total = numbers[i] + numbers[j]

  while total <= invalid:
    print "j is", j, "(", numbers[j], ")"
    if total == invalid:
      print("Got it! %s\n" % numbers[i: j + 1])
      smallest = i
      biggest = j
      found = True
      break
    j += 1
    total += numbers[j]
  # if we get to here, we went over the number we're looking for
  i += 1

contiguous = sorted(list(numbers[smallest: biggest + 1]))
print contiguous[0] + contiguous[-1]
