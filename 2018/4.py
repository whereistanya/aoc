#!/usr/bin/env python
# Advent of code Day 2.

import re
import sys

# Fragile regexp alert wooo woooooo.
line_re = "\[\d{4}-\d\d-\d\d (\d\d):(\d\d)\] ([\w\s]+#?(\d*)?[\w\s]+)"

class Guard:
  def __init__(self, guard_id):
    self.id = guard_id
    self.minutes_count = 0
    self.minutes = {}

  def __repr__(self):
    return "Guard %s: %s minutes" % (self.id, self.minutes_count)

  def _add_minute(self, minute):
    try:
      self.minutes[minute] += 1
    except KeyError:
      self.minutes[minute] = 1

  def sleepiest_minute(self):
    most = -1
    value = -1
    for minute in self.minutes:
      if self.minutes[minute] > value:
        most = minute
        value = self.minutes[minute]
    return (most, value)

  def add_sleep(self, beginning, end):
    """Add sleep minutes."""
    minutes = 0
    if beginning < end:
      self.minutes_count += (end - beginning)
      for i in range (beginning, end):
        self._add_minute(i)
    else:  # wrap an hour
      self.minutes_count += (end + (60 - beginning))
      for i in range (0, end):
        self._add_minute(i)
      for i in range (beginning, 60):
        self._add_minute(i)


with open("day4input.txt", "r") as f:
  lines = sorted(f.readlines())

"""
lines = [
  "[1518-11-01 00:00] Guard #10 begins shift",
  "[1518-11-01 00:05] falls asleep",
  "[1518-11-01 00:25] wakes up",
  "[1518-11-01 00:30] falls asleep",
  "[1518-11-01 00:55] wakes up",
  "[1518-11-01 23:58] Guard #99 begins shift",
  "[1518-11-02 00:40] falls asleep",
  "[1518-11-02 00:50] wakes up",
  "[1518-11-03 00:05] Guard #10 begins shift",
  "[1518-11-03 00:24] falls asleep",
  "[1518-11-03 00:29] wakes up",
  "[1518-11-04 00:02] Guard #99 begins shift",
  "[1518-11-04 00:36] falls asleep",
  "[1518-11-04 00:46] wakes up",
  "[1518-11-05 00:03] Guard #99 begins shift",
  "[1518-11-05 00:45] falls asleep",
  "[1518-11-05 00:55] wakes up",
]
"""

guards = {}  # (id_str:Guard)
guard = None

#######################################################
# Part one
#######################################################

beginning = -1

for line in lines:
  line = line.strip()
  groups = re.search(line_re, line.strip()).groups()
  hour = groups[0]
  minute = groups[1]
  log = groups[2]
  guard_id = groups[3]

  if guard_id:
    # New guard. All new logs are associated with this guard.
    try:
      guard = guards[guard_id]
    except KeyError:
      guard = Guard(guard_id)
      guards[guard_id] = guard
  elif "falls asleep" in log:
    beginning = minute
  elif "wakes up" in log and beginning >= 0:
    guard.add_sleep(int(beginning), int(minute))
    beginning = -1
  else:
    print("Weird log: %s" % log)
    sys.exit(1)

sleepiest = -1
minutes_asleep = -1
for k in guards:
  guard = guards[k]
  print(guard)
  if guard.minutes_count > minutes_asleep:
    minutes_asleep = guard.minutes_count
    sleepiest = guard.id

(sleepiest_minute, count) = guards[sleepiest].sleepiest_minute()
print("Sleepiest is %s with %d x %d = %d" % (
  sleepiest, minutes_asleep, int(sleepiest_minute),
  int(sleepiest) * int(sleepiest_minute)))

#######################################################
# Part two
#######################################################

global_sleepiest_minute = -1
global_sleepiest_count = -1
global_sleepiest_guard = -1

for guard_id in guards:
  guard = guards[guard_id]
  (sleepiest_minute, count) = guard.sleepiest_minute()
  if count > global_sleepiest_count:
    global_sleepiest_count = count
    global_sleepiest_minute = sleepiest_minute
    global_sleepiest_guard = guard.id

print(int(global_sleepiest_guard) * int (global_sleepiest_minute))
