#!/usr/bin/env python
# Day 25. This is a brute force / super slow solution.

import collections

class State(object):
  def __init__(self):
    pass

  def __repr__(self):
    return self.__class__.__name__

class StateA(State):
  def run(self, ribbon, position):
    value = ribbon.get(position, 0)
    if value == 0:
      ribbon[position] = 1
      position += 1
      return position, StateB()
    elif value == 1:
      ribbon[position] = 0
      position += 1
      return position, StateF()

class StateB(State):
   def run(self, ribbon, position):
    value = ribbon.get(position, 0)
    if value == 0:
      ribbon[position] = 0
      position -= 1
      return position, StateB()
    elif value == 1:
      ribbon[position] = 1
      position -= 1
      return position, StateC()

class StateC(State):
  def run(self, ribbon, position):
    value = ribbon.get(position, 0)
    if value == 0:
      ribbon[position] = 1
      position -= 1
      return position, StateD()
    elif value == 1:
      ribbon[position] = 0
      position += 1
      return position, StateC()

class StateD(State):
  def run(self, ribbon, position):
    value = ribbon.get(position, 0)
    if value == 0:
      ribbon[position] = 1
      position -= 1
      return position, StateE()
    elif value == 1:
      ribbon[position] = 1
      position += 1
      return position, StateA()

class StateE(State):
  def run(self, ribbon, position):
    value = ribbon.get(position, 0)
    if value == 0:
      ribbon[position] = 1
      position -= 1
      return position, StateF()
    elif value == 1:
      ribbon[position] = 0
      position -= 1
      return position, StateD()

class StateF(State):
   def run(self, ribbon, position):
    value = ribbon.get(position, 0)
    if value == 0:
      ribbon[position] = 1
      position += 1
      return position, StateA()
    elif value == 1:
      ribbon[position] = 0
      position -= 1
      return position, StateE()


class StateMachine(object):
  def __init__(self):
    self.state = StateA()
    self.ribbon = collections.defaultdict()
    self.position = 0

  def run(self):
    self.position, self.state = self.state.run(self.ribbon, self.position)
    s = ""
    count = 0
    for v in self.ribbon.values():
      if (v):
        count += 1
    return count

machine = StateMachine()
for i in range(0, 12964419):
  if i % 100000 == 0:
    print i
  out = machine.run()
print out
