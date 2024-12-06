#!/usr/bin/env python

filename = "input.txt"
#

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]


part1 = 0
part2 = 0



def isOrdered(numbers, rules):
  # assuming no duplicates in lines!
  # if X has to come before Y, then if we see Y, we fail if we ever see X
  notAllowed = set()
  for number in numbers:
    if number in rules:
      for value in rules[number]:
        notAllowed.add(value)
    if number in notAllowed:
      return False
  return True

def order(numbers, rules):
  while True:
    reset = False
    notAllowed = {}
    for number in numbers:
      if reset:
        break

      if number in rules:
        for value in rules[number]:
          notAllowed[value] = number # value should have come before number
      if number in notAllowed.keys():
        shouldBeBefore = notAllowed[number]
        index = numbers.index(shouldBeBefore)
        numbers.remove(number)
        numbers.insert(index, number)
        reset = True
        break # out of the for, back to the while
    if not reset:
      return numbers



# start here

lessThan = {}  # int: int where first has to come before second
updates = []
unordered = []

# Parse
for line in lines:
  if "|" in line:
    first, second = [int(x) for x in line.strip().split("|")]
    try:
      lessThan[second].add(first)
    except KeyError:
      lessThan[second] = set([first])
    continue

  if "," in line:
    numbers = [int(x) for x in line.strip().split(",")]
    updates.append(numbers)

# Part1
for update in updates:
  ordered = isOrdered(update, lessThan)
  if ordered:
    middle = int((len(update)- 1) / 2)
    part1 += update[middle]
  else:
    unordered.append(update)

print("Part 1:", part1)

print()

part2 = 0

for update in unordered:
  ordered = order(update, lessThan)
  if not (isOrdered(ordered, lessThan)):
    print("Well something went wrong.")
    print(update)
    print(ordered)
    exit()
  middle = int((len(ordered)- 1) / 2)
  part2 += ordered[middle]

print("Part 2:", part2)
