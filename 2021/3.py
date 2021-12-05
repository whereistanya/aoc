#!/usr/bin/env python

inputfile = "input.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]


#lines = """00100
#11110
#10110
#10111
#10101
#01111
#00111
#11100
#10000
#11001
#00010
#01010""".split()


def most_least(stringlist):
  line_length = len(stringlist[0])
  counts = [0] * len(stringlist[0])
  for line in stringlist:
    for i in range(line_length):
      counts[i] += int(line[i])

  most_common = [0] * line_length
  least_common = [0] * line_length

  for i in range (len(counts)):
    if counts[i] >= float(len(stringlist)) / 2:
      most_common[i] = 1
    else:
      most_common[i] = 0
    least_common[i] = 1 ^ most_common[i]
  return most_common, least_common


def to_decimal(intlist):
  i = len(intlist) - 1
  value = 1
  decimal = 0
  while i >= 0:
    if intlist[i] == 1:
      decimal += value
    i -= 1
    value *= 2
  return decimal

most_common, least_common = most_least(lines)
print (to_decimal(most_common) * to_decimal(least_common))

# part 2

to_check = list(lines)
next_list = list()

i = 0
while len(to_check) > 1:
  most_common, least_common = most_least(to_check)
  for number in to_check:
    if int(number[i]) == most_common[i]:
      next_list.append(number)
  i += 1
  to_check = next_list
  next_list = list()

oxygen = to_decimal([int(x) for x in to_check[0]])
print("oxygen rating", to_check[0], oxygen)

i = 0
to_check = list(lines)
next_list = list()
while len(to_check) > 1:
  most_common, least_common = most_least(to_check)
  for number in to_check:
    if int(number[i]) == least_common[i]:
      next_list.append(number)
  i += 1
  to_check = next_list
  next_list = list()

co2 = to_decimal([int(x) for x in to_check[0]])
print("co2 rating", to_check[0], co2)
print ("life support", oxygen * co2)
