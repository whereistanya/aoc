#!/usr/bin/env python
# Advent of code Day 7.

import re
import sys

line_re = "Step (\w) must be finished before step (\w) can begin."

with open("day7input.txt", "r") as f:
  lines = f.readlines()

"""
lines = [
  "Step C must be finished before step A can begin.",
  "Step C must be finished before step F can begin.",
  "Step A must be finished before step B can begin.",
  "Step A must be finished before step D can begin.",
  "Step B must be finished before step E can begin.",
  "Step D must be finished before step E can begin.",
  "Step F must be finished before step E can begin.",
]
"""

depends = {}

for line in lines:
  letters = re.search(line_re, line).groups()
  if len(letters) != 2:
    print("Bad input")
    sys.exit(1)
  depender = letters[1]
  dependee = letters[0]

  try:
    depends[depender].append(dependee)
  except KeyError:
    depends[depender] = [dependee]

  if dependee not in depends:
    depends[dependee] = []

DELTA = 4
class Worker:
  def __init__(self):
    self.time = 0
    self.task = None

  def add_task(self, task):
    self.task = task
    self.time = ord(task) - DELTA

  def __repr__(self):
    return "W: %s (%d)" % (self.task, self.time)

workers = [Worker(), Worker(), Worker(), Worker(), Worker()] 

done = set()
ordered = ""
seconds = 0

# Each loop represents one second
while True:
  for worker in workers:
    if worker.time == 0: # available worker
      # record the end of the previous work
      if worker.task:
        done.add(worker.task)
        ordered += worker.task
        worker.task = None

    # find what's available now
    available = []
    for k, values in depends.items():
      if not values:
        available.append(k)
        continue
      if (all(v in done for v in values)):
        available.append(k)
        continue

    available = sorted(available)

  # assign a new task
  for worker in workers:
    if worker.time == 0: # available worker
      try:
        x = available.pop(0)
        worker.add_task(x)
        depends.pop(x)
      except IndexError:
        pass
    if worker.time > 0:
      worker.time -= 1

  #print seconds, [worker.task for worker in workers], ordered
  if not depends:
    # Nothing left to process, no churning workers
    if all(worker.task == None for worker in workers):
      break
  seconds += 1

print(ordered, len(ordered))
print("It took %d seconds" % seconds)
