#!/usr/bin/env python3
# Advent of code Day 1.

with open("input1.txt", "r") as f:
  lines = f.readlines()

example = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

example2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

#lines = example2.strip().split("\n")

numbers = {"one": 1,
           "two": 2,
           "three": 3,
           "four": 4,
           "five": 5,
           "six": 6,
           "seven": 7,
           "eight": 8,
           "nine": 9}

total = 0

for line in lines:
  digits = []
  for i in range(0, len(line)):
    char = line[i]
    if char.isdigit():
        digits.append(int(char))
    for number in numbers:
      if line[i:].startswith(number):
        digits.append(numbers[number])
  print (line, digits)
  total += 10 * digits[0]
  total += digits[-1]

print (total)

