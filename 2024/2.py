#!/usr/bin/env python

filename = "input.txt"
#filename = "test1"

with open(filename, "r") as f:
  lines = f.readlines()


def isSafe(numbers):
  sorted_asc = sorted(numbers)
  sorted_desc = sorted(numbers, reverse=True)
  if numbers != sorted_asc and numbers != sorted_desc:
    return False

  for i in range(1, len(numbers)):
    if abs(numbers[i] - numbers[i-1]) not in [1, 2, 3]:
      return False

  return True



# Part 1
count = 0
for line in lines:
  numbers = [int(x) for x in line.split()]
  if isSafe(numbers):
    count += 1
print("Part 1:", count)


# Part 2
count = 0
for line in lines:
  numbers = [int(x) for x in line.split()]
  if isSafe(numbers):
    count += 1
    continue

  for i in range(len(numbers)):
    if isSafe(numbers[:i] + numbers[i+1:]):
      count += 1
      break

print("Part 2:", count)
