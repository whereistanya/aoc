#!/usr/bin/env python3

VERBOSE = False
TEST = False

with open("input6.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]

example = """
Time:      7  15   30
Distance:  9  40  200"""

if TEST:
  lines = [x.strip() for x in example.strip().split("\n")]

times = [int(x.strip()) for x in lines[0].split(":")[1].split()]
distances = [int(x.strip()) for x in lines[1].split(":")[1].split()]

part2_time = int("".join([x.strip() for x in lines[0].split(":")[1].split()]))
part2_distance = int("".join([x.strip() for x in lines[1].split(":")[1].split()]))

speed = 0
total_wins = 1
for i in range(len(times)):
  initial_losses = 0
  for j in range(times[i]):
    speed = j
    racetime = times[i] - j
    distance = speed * racetime
    if distance > distances[i]:
      break
    else:
      initial_losses += 1
  # Add one because we're going from 0 to <full time> inclusive
  wins = times[i] + 1 - (2 * initial_losses)
  total_wins *= wins
print("Part 1", total_wins)

initial_losses = 0
for j in range(part2_time + 1):
  speed = j
  racetime = part2_time - j
  distance = speed * racetime
  if distance > part2_distance:
    break
  else:
    initial_losses += 1

print ("Part 2", (part2_time + 1 - (2 * initial_losses)))
