#!/usr/bin/env python

inputfile = "input.txt"
with open(inputfile, "r") as f:
  values = [int(x) for x in f.readline().split(",")]

#values = [3, 4, 3, 1, 2]
timers = [0, 0, 0, 0, 0, 0, 0]

for value in values:
  timers[value] += 1

birthday = 0
new_fish = 0
day_8_fish = 0
day_7_fish = 0

def print_fish(timers, cohort):
  s = " "
  for i in range(cohort, cohort + len(timers)):
    s += "%d, " % timers[i % 7]
  return s

print("Initial state:", print_fish(timers, 0))

for i in range(1, 257):
  #print("Starting day %d. Birthday for cohort %d!" % (i, birthday))

  # if there's anything in the birthday slot, create that many new fish
  # The new fish have an 8 day timer; just hold on to them for now
  new_fish = timers[birthday] # today has this many new baby fish with 8day timers

  # If we had any day 7 fish, they're day 6 fish now
  timers[birthday] += day_7_fish # for next time

  # If we had any day 8 fish, they're day 7 fish now
  day_7_fish = day_8_fish # a day has passed; move the day 8 fish forward

  # Reset new fish at 8.
  day_8_fish = new_fish

  print ("After day %d, we have %d fish" % (i, sum(timers) + day_7_fish +
  day_8_fish))
  birthday = (birthday + 1) % 7 # day 0 moves to the next day
