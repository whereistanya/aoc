#!/usr/bin/env python3

import copy
import grid

class Move(object):
  def __init__(self, cost, pod, move_from, move_to):
    self.cost = cost
    self.pod = pod
    self.move_from = move_from
    self.move_to = move_to

  def __repr__(self):
    return "Move: %s from %s to %s(%d)" % (self.pod.name, self.move_from, self.move_to, self.cost)

class Pod(object):
  def __init__(self, name):
    costs = {
      "A": 1,
      "B": 10,
      "C": 100,
      "D": 1000,
    }
    home = { "A": 3, "B": 5, "C": 7, "D": 9 }
    self.name = name
    letter, number = self.name
    if letter not in ['A', 'B', 'C', 'D']:
      print ("BUG! Got pod name %s" % pod)
      exit(1)
    self.pod_type = letter
    self.validx = home[letter]
    self.cost = costs[self.pod_type]


class Burrow(grid.Grid): # grid is only used for drawing; it's a convenient hack
  def __init__(self, lines):
    super().__init__(lines)
    self.pods = {} # (x, y): Pod
    self.deepest = 0 # will be set by init_pods
    self.init_pods()

  def move(self, move_from, move_to):
    from_x, from_y = move_from
    to_x, to_y = move_to
    pod = self.pods[move_from]
    self.grid[move_from].value = '.'
    self.grid[move_to].value = pod.pod_type
    self.pods.pop(move_from)
    self.pods[move_to] = pod

  def init_pods(self):
    pod_index = 0
    for point in self.grid.values():
      if point.value in ['A', 'B', 'C', 'D']:
        name = "%s%d" % (point.value, pod_index)
        pod_index += 1
        self.pods[(point.x, point.y)] = Pod(name)
        if point.y > self.deepest:
          self.deepest = point.y

  def sorted(self):
    for location, pod in self.pods.items():
      if location[0] != pod.validx:
        return False
    return True

  def move_room_to_room(self, initialx, pod, initial_cost):
    home_move = self.move_into_a_room(initialx, pod)

    if home_move: # Do it and nothing else
      destination, cost_from_here = home_move
      return (destination, initial_cost + cost_from_here)

  def show_moves_into_hall(self, initialx, initial_cost, pod):
    y = 1
    moves = []
    cost = initial_cost
    for x in range(initialx - 1, 0, -1):
      if (x, y) in self.pods:
        break
      cost += pod.cost
      if self.in_valid_hallspace((x, y)):
        moves.append(((x, y), cost))

    cost = initial_cost
    for x in range(initialx + 1, 12):
      if (x, y) in self.pods:
        break
      cost += pod.cost
      if self.in_valid_hallspace((x, y)):
        moves.append(((x, y), cost))
    return moves

  def move_into_a_room(self, x, pod):
    # If there's a different letter anywhere in the space, we can't move in
    for i in range(2, self.deepest + 1):
      if (pod.validx, i) in self.pods:
        inhabitant = self.pods[(pod.validx, i)]
        if inhabitant.pod_type != pod.pod_type:
          return None

    # If we can't get to the room, we can't move in either
    cost = 0
    for i in range(min(x, pod.validx), max(x, pod.validx) + 1):
      if i == x:
        continue # ignore if it's itself; TODO: replace this
      cost += pod.cost
      if (i, 1) in self.pods: # path is blocked
        return None # can't get to the room

    # Otherwise go as deep as possible
    for i in range(self.deepest, 1, -1):
      if (pod.validx, i) not in self.pods:
        total_cost = cost + (pod.cost * (i - 1))
        return ((pod.validx, i), total_cost)

  def blocked_in_room(self, location):
    x, y = location
    for i in range(y - 1, 1, -1):
      if (x, i) in self.pods:
        return True # yes, blocked

  def in_valid_hallspace(self, location):
    valid_hallspace = [(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1), (11, 1)]
    if location in valid_hallspace:
      return True
    return False

  def in_room(self, location):
    rooms = [(3, 2), (3, 3), (5, 2), (5, 3), (7, 2), (7, 3), (9, 2), (9, 3)]
    if location not in rooms:
      return False
    return True

  def possible_moves(self):
    moves = []
    for location, pod in self.pods.items():
      x, y = location

      # If it's blocked, skip it
      if self.blocked_in_room(location):
        continue

      # If it's in the right place, don't move it
      if x == pod.validx:
        if y == 3: # don't move
          continue
        if y == 2: # don't move if the upstairs neighbour is also ok
          neighbour = self.pods[(x, 3)]
          if x == neighbour.validx:
            continue

      # If it can go into a room, don't collect possible moves, move it next
      if self.in_valid_hallspace(location):
        valid_move = self.move_into_a_room(x, pod)
        if valid_move:
          new_location, cost = valid_move
          # TODO: this return is too sneaky
          return([Move(cost, pod, location, new_location)])

      else:
        assert(self.in_room(location))
        initial_cost = (location[1] - 1) * pod.cost

        # If it can go from one room to another, move it
        valid_move = self.move_room_to_room(x, pod, initial_cost)
        if valid_move:
          new_location, cost = valid_move
          # TODO: this return is also too sneaky
          return([Move(cost, pod, location, new_location)])

        # Finally, collect all the moves that take something into a hall
        moves_for_this_pod = []
        x, y = location

        moves_for_this_pod = self.show_moves_into_hall(
          x, initial_cost, pod)

        for new_location, cost in moves_for_this_pod:
          moves.append(Move(cost, pod, location, new_location))

    return moves


restricted = {
  (3, 2): "A", (3, 3): "A",
  (5, 2): "B", (5, 3): "B",
  (7, 2): "C", (7, 3): "C",
  (9, 2): "D", (9, 3): "D",
}

def test():
  lines = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""".split("\n")
  return lines

def test2():
  lines = """#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########""".split("\n")
  return lines

def real():
  lines="""#############
#...........#
###B#B#D#A###
  #D#C#A#C#
  #########""".split("\n")
  return lines

lines = real()
pods = []

burrow = Burrow(lines)
burrow.printnocolor()

def sort_pods(burrow, energy_so_far, least_energy, path, costs):
  # Two base cases (maybe don't need the first?)
  #burrow.printnocolor()
  if energy_so_far >= least_energy:
    return 100000000
  if burrow.sorted():
    return energy_so_far
  possible_moves = burrow.possible_moves()

  for move in possible_moves:
    burrow.move(move.move_from, move.move_to)
    # TODO: memoize the state instead of the path :thinking_face:
    path.append(move.pod.name)
    s = ''.join(path)
    if s in costs:
      cost = costs[s]
    else:
      cost = sort_pods(burrow, energy_so_far + move.cost, least_energy, path, costs)
    if cost < least_energy:
      costs[s] = cost
      least_energy = cost
    path.pop()
    burrow.move(move.move_to, move.move_from)
  return least_energy

energy = sort_pods(burrow, 0, 100000000000, [], {})
print (energy)

