#!/usr/bin/env python

inputfile = "input2.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

"""
lines = [
  "1-3 a: abcde",
  "1-3 b: cdefg",
  "2-9 c: ccccccccc"
]
"""

valid1 = 0
valid2 = 0
for line in lines:
  rule, letter, password = line.split()
  lmin, lmax = [int(x) for x in rule.split("-")]
  letter = letter.strip(":")
  count = password.count(letter)
  print lmin, lmax, count, letter, password

  # Part 1
  if count >= lmin and count <= lmax:
    valid1 += 1

  # Part 2
  if (password[lmin - 1] == letter) ^ (password[lmax - 1] == letter):
    valid2 += 1

print valid1, valid2
