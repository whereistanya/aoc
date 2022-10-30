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
    self.find_pods()

  def move(self, move_from, move_to):
    from_x, from_y = move_from
    to_x, to_y = move_to
    pod = self.pods[move_from]
    self.grid[move_from].value = '.'
    self.grid[move_to].value = pod.pod_type
    self.pods.pop(move_from)
    self.pods[move_to] = pod

  def find_pods(self):
    pod_index = 0
    for point in self.grid.values():
      if point.value in ['A', 'B', 'C', 'D']:
        name = "%s%d" % (point.value, pod_index)
        pod_index += 1
        self.pods[(point.x, point.y)] = Pod(name)

  def sorted(self):
    for location, pod in self.pods.items():
      if location[0] != pod.validx:
        return False
    return True

  def valid_hallspace(self):
    return [(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1), (11, 1)]

  def in_hall(self, location):
    if location in self.valid_hallspace():
      return True
    return False

  def moves_in_hall_from_here(self, initialx, initial_cost, pod):
    home_move = self.moves_into_rooms_from_here(initialx, pod)

    if home_move: # Do it and nothing else
      destination, cost_from_here = home_move
      moves = [(destination, initial_cost + cost_from_here)]
      return moves

    y = 1
    moves = []
    cost = initial_cost
    for x in range(initialx - 1, 0, -1):
      if (x, y) in self.pods:
        break
      cost += pod.cost
      if (x, y) in self.valid_hallspace():
        moves.append(((x, y), cost))

    cost = initial_cost
    for x in range(initialx + 1, 12):
      if (x, y) in self.pods:
        break
      cost += pod.cost
      if (x, y) in self.valid_hallspace():
        moves.append(((x, y), cost))
    return moves

  def moves_into_rooms_from_here(self, x, pod):
    destinationx = pod.validx

    if (destinationx, 2) in self.pods: # blocked, can't get in
      return None

    # is there a path to destinationx?
    cost = 0
    for i in range(min(x, destinationx), max(x, destinationx) + 1):
      if i == x:
        continue # ignore if it's self; replace this
      cost += pod.cost
      if (i, 1) in self.pods:
        # path is blocked
        return None # no moves

    # if there's a different letter in (destinationx, 3), we can't move in

    if (destinationx, 3) not in self.pods: # it's available, move in
      return ((destinationx, 3), cost + (pod.cost * 2)) # two final steps

    # There's someone in 3, but we can try 2
    inhabitant = self.pods[(destinationx, 3)]
    if inhabitant.pod_type != pod.pod_type:
      return None # no moves
    # We're good to move in to 2
    return((destinationx, 2), cost + pod.cost) # One final step

  def in_room_and_unblocked(self, location):
    rooms = [(3, 2), (3, 3), (5, 2), (5, 3), (7, 2), (7, 3), (9, 2), (9, 3)]
    if location not in rooms:
      return False
    x = location[0]
    y = location[1]

    if y == 3: # the bottom of the room
      if (x, 2) in self.pods: # something is in the way
        return False

    return True

  def possible_moves(self):
# 1. Amphipods can move up, down, left, or right so long as
# they are moving into an unoccupied open space.
# 2. Amphipods will never stop on the space immediately outside
# any room.
# 3. Amphipods will never move from the hallway into a room unless
# that room is their destination room and that room contains no
# amphipods which do not also have that room as their own destination.
# 4. Once an amphipod stops moving in the hallway, it will stay in
# that spot until it can move into a room.
# Each amphipod gets to move at most twice: out of the
# burrow into the hall, into the new burrow, or just
# directly into the new burrow.
    moves = []
    for location, pod in self.pods.items():
      x, y = location

      # If it's in the right place, don't move it
      if x == pod.validx:
        if y == 3: # don't move
          continue
        if y == 2: # don't move if the upstairs neighbour is also ok
          neighbour = self.pods[(x, 3)]
          if x == neighbour.validx:
            continue

      moves_for_this_pod = []
      x = location[0]
      y = location[1]


      if self.in_room_and_unblocked(location):
        #print("In a room and unblocked")
        if y == 2: # add 1 or 2 moves to get to the hall
          initial_cost = pod.cost
        elif y == 3:
          initial_cost = pod.cost * 2
        moves_for_this_pod = self.moves_in_hall_from_here(
          x, initial_cost, pod)

      elif self.in_hall(location):
        valid_move = self.moves_into_rooms_from_here(x, pod)
        if valid_move:
          moves_for_this_pod = [valid_move]

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
burrow.find_pods()

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

