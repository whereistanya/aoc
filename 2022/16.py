#!/usr/bin/env python3

import math
import re

test = True
test = False

class Valve(object):
  def __init__(self, name, rate):
    self.name = name
    self.rate = rate
    self.tunnels = []

if test:
  filename = "test16.txt"
else:
  filename = "input16.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

line_re = "Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)"


valves = {}
total_to_open = 0
for line in lines:
  matches = re.finditer(line_re, line)
  for match in matches:
    name, rate, out = match.groups()
    tunnels = [x.strip() for x in out.split(",")]
    if name in valves:
      valves[name].tunnels.extend(tunnels)
    else:
      valve = Valve(name, int(rate))
      valve.tunnels.extend(tunnels)
      valves[name] = valve
      if int(rate) > 0:
        total_to_open += 1

"""
# Part 1
start = "AA"
seen = set() # global in this code
seen = {}
possible = [("AA", set(), seen, 0)] # current, on, seen, rate
max_pressure = 0

print(total_to_open, "to open")
for i in range (29, 0, -1): # remaining minutes
  print (i, len(possible),)
  #print(possible)
  this_round = list(possible)
  possible.clear()
  for p, on, seen, rate in this_round:
    # on is always sorted
    #print(p, on, rate)
    current = valves[p]
    #print (current.name, current.tunnels, current.rate)
    seen[("%s-%s" % (p, on))] = rate
    if p not in on and current.rate > 0:
      next_on = set(on)
      next_on.add(p)
      if len(next_on) == total_to_open: # all open, drop this
        final_rate = rate + (current.rate * i)
        if final_rate > max_pressure:
          max_pressure = final_rate
          print("Max pressure is", max_pressure)
          continue
      else:
        # probably an off by one here; didn't even check
        next_rate = rate + (current.rate * i)
        if next_rate > max_pressure:
          max_pressure = next_rate
        seen["%s-%s" % (p, sorted(next_on))] = next_rate
        possible.append((p, sorted(next_on), seen, next_rate))

    for t in current.tunnels:
      next_hash = ("%s-%s" % (t, on))
      if next_hash not in seen:
        possible.append((t, on, seen, rate))
      elif seen[next_hash] < rate:
        possible.append((t, on, seen, rate))
        seen[next_hash] = rate


print("Part 1: max pressure was", max_pressure)

"""

#Part 2  Attempt 1, too slow

start = "AA"
seen = {} # global in this code
# my_pos, e_pos, valves_open, already_seen, rate_so_far
possible = [(start, start, set(), seen, 0)]
max_pressure = 0

print(total_to_open, "to open")
for i in range (25, -1, -1): # remaining minutes
  print (i, len(possible))
  this_round = list(possible)
  possible.clear()
  for my_pos, e_pos, on, seen, rate in this_round:
    my_valve = valves[my_pos]
    e_valve = valves[e_pos]

    if rate > max_pressure:
      max_pressure = rate
      print("Max pressure now %d (%s)" % (max_pressure, on))

    # Scenario 1: everything's already open; stop working.
    if len(on) == total_to_open: # all open
        print("All open: max pressure is", max_pressure)
        continue

    # Scenario 2: both people stop to open valves. Only possible if
    # both valves are closed and worth > 0.
    if (my_pos not in on and e_pos not in on and
        my_valve.rate > 0 and e_valve.rate > 0 and my_pos != e_pos):

        next_rate = rate + (my_valve.rate * i) + (e_valve.rate * i)
        #print("S2: opening %s(%d) and %s(%d) for another %d turns (%d, %s)" % (
        #  my_pos, my_valve.rate, e_pos, e_valve.rate, i, next_rate, on)) 
        next_on = set(on)
        next_on.add(my_pos)
        next_on.add(e_pos)
        next_on = sorted(next_on)
        next_hash = ("%s-%s" % (sorted([my_pos, e_pos]), next_on))
        if next_hash not in seen or seen[next_hash] < next_rate:
          possible.append((my_pos, e_pos, next_on, seen, next_rate))
          seen[next_hash] = next_rate

    # Scenario 3: I open a valve; the elephant takes one of its available
    # tunnels.
    if (my_pos not in on and my_valve.rate > 0):
        next_rate = rate + (my_valve.rate * i)
        #print("S3: opening %s(%d) for another %d turns (%d, %s)" % (
        #  my_pos, my_valve.rate, i, next_rate, on))
        next_on = set(on)
        next_on.add(my_pos)
        next_on = sorted(next_on)

        for e_t in e_valve.tunnels:
          next_hash = ("%s-%s" % (sorted([my_pos, e_t]), next_on))
          if next_hash not in seen or seen[next_hash] < next_rate:
            possible.append((my_pos, e_t, next_on, seen, next_rate))
            seen[next_hash] = next_rate

    # Scenario 4: the elephant opens a valve; I take a tunnel
    if (e_pos not in on and e_valve.rate > 0):
        next_rate = rate + (e_valve.rate * i)
        #print("S4: opening %s(%d) for another %d turns (%d, %s)" % (
        #  e_pos, e_valve.rate, i, next_rate, on))
        next_on = set(on)
        next_on.add(e_pos)
        next_on = sorted(next_on)

        for my_t in my_valve.tunnels:
          next_hash = ("%s-%s" % (sorted([my_t, e_pos]), next_on))
          if next_hash not in seen or seen[next_hash] < next_rate:
            possible.append((my_t, e_pos, next_on, seen, next_rate))
            seen[next_hash] = next_rate

    # Scenario 5: Finally, all the cases where nobody opens a valve
    trying = set()
    for my_t in my_valve.tunnels:
      for e_t in e_valve.tunnels:
        next_hash = ("%s-%s" % (
          (max(my_t, e_t) + min(my_t, e_t)), on))
        if next_hash not in seen or seen[next_hash] < rate:
          if next_hash not in trying:
            possible.append((my_t, e_t, on, seen, rate))
            trying.add(next_hash)
            seen[next_hash] = rate

print("Part 2: max pressure was", max_pressure)
