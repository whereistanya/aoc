#!/usr/bin/env python3

import copy
import grid

class Move(object):
  def __init__(self, cost, state, name, location):
    self.cost = cost
    self.new_state = state
    self.name = name
    self.location = location

  def __repr__(self):
    return "Move: %s to %s(%d => %s)" % (self.name, self.location, self.cost, self.new_state)

class Burrow(grid.Grid):
  def __init__(self, lines):
    super().__init__(lines)
    self.pods = {} # location: name
    self.costs = {
      "A": 1,
      "B": 10,
      "C": 100,
      "D": 1000,
    }
    self.find_pods()
    print(self.pods)

  def set_state(self, state):
    # reset the display grid
    for location in self.grid:
      if self.grid[location].value == '#':
        continue
      self.grid[location].value = '.'

    self.pods = state
    for location, name in state.items():
      x, y = location
      self.setvalue(x, y, name[0])

  def move_cost(self, pod_type):
    # raises a KeyError if it's not a valid type
    return self.costs[pod_type]

  def find_pods(self):
    pod_index = 0
    for point in self.grid.values():
      if point.value in self.costs:
        name = "%s%d" % (point.value, pod_index)
        pod_index += 1
        self.pods[(point.x, point.y)] = name # TODO: make pod name a tuple


  def pod_type(self, name):
    letter, number = name
    if letter not in ['A', 'B', 'C', 'D']:
      print ("BUG! Got pod name %s" % pod)
      exit(1)
    return letter

  def home(self):
    return {
      "A": [(3, 2), (3, 3)],
      "B": [(5, 2), (5, 3)],
      "C": [(7, 2), (7, 3)],
      "D": [(9, 2), (9, 3)],
    }

  def sorted(self):
    endpoints = self.home()
    for location, name in self.pods.items():
      letter = self.pod_type(name)
      if location not in endpoints[letter]:
        return False
    return True

  def valid_hallspace(self):
    return [(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1), (11, 1)]

  def in_hall(self, location):
    if location in self.valid_hallspace():
      return True
    return False

  def moves_in_hall_from_here(self, initialx, initial_cost, cost_per_step, name):

    home_move = self.moves_into_rooms_from_here(initialx, name, cost_per_step)
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
      cost += cost_per_step
      if (x, y) in self.valid_hallspace():
        moves.append(((x, y), cost))

    cost = initial_cost
    for x in range(initialx + 1, 12):
      if (x, y) in self.pods:
        break
      cost += cost_per_step
      if (x, y) in self.valid_hallspace():
        moves.append(((x, y), cost))
    return moves

  def moves_into_rooms_from_here(self, x, name, cost_per_step):
    letter = self.pod_type(name)
    endpoints = self.home()
    valid = endpoints[letter]
    assert (valid[0][0] == valid[1][0]) # lazy test that both valid endpoints
                                        # have the same x
    destinationx = valid[0][0]

    if (destinationx, 2) in self.pods: # blocked, can't get 
      return None

    # is there a path to destinationx?
    cost = 0
    for i in range(min(x, destinationx), max(x, destinationx)):
      if i == x:
        continue # ignore if it's self; replace this
      cost += cost_per_step
      if (i, 1) in self.pods:
        # path is blocked
        return None # no moves

    # if there's a different letter in (destinationx, 3), we can't move in

    if (destinationx, 3) not in self.pods: # it's available, move in
      return ((destinationx, 3), cost + (cost_per_step * 2)) # two final steps

    # There's someone in 3, but we can try 2
    inhabitant = self.pods[(destinationx, 3)]
    if self.pod_type(inhabitant) != letter:
      return None # no moves
    # We're good to move in to 2
    return((destinationx, 2), cost + cost_per_step) # One final step



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

  def valid_location(self, name, location):
    endpoints = self.home()
    letter = self.pod_type(name)
    valid = endpoints[letter]
    assert (valid[0][0] == valid[1][0]) # lazy test that both valid endpoints
                                        # have the same x
    destinationx = valid[0][0]
    x, y = location
    if x == destinationx:
      return True
    else:
      return False

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
    for location, name in self.pods.items():
      x, y = location
      #print("Can I move %s/%s?" % (name, location))

      # If it's in the right place, don't move it
      if self.valid_location(name, location):
        if y == 3: # don't move
          continue
        if y == 2: # don't move if the upstairs neighbour is also ok
          neighbour = self.pods[(x, 3)]
          if self.valid_location(neighbour, (x, 3)):
            continue


      cost_per_move = self.move_cost(self.pod_type(name))
      #print("Cost would be %d" % cost_per_move)
      moves_for_this_pod = []
      x = location[0]
      y = location[1]


      if self.in_room_and_unblocked(location):
        #print("In a room and unblocked")
        if y == 2: # add 1 or 2 moves to get to the hall
          initial_cost = cost_per_move
        elif y == 3:
          initial_cost = cost_per_move * 2
        moves_for_this_pod = self.moves_in_hall_from_here(x, initial_cost, cost_per_move, name)

      elif self.in_hall(location):
        #print("In a hall")
        valid_move = self.moves_into_rooms_from_here(x, name, cost_per_move)
        if valid_move:
          moves_for_this_pod = [valid_move]
      else:
        #print("In a room, blocked in")
        pass

      for new_location, cost in moves_for_this_pod:
        new_state = dict(self.pods) # this is unnecessarily expensive
        new_state.pop(location)
        new_state[new_location] = name
        moves.append(Move(cost, new_state, name, new_location))

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


lines = test()
pods = []

burrow = Burrow(lines)
burrow.find_pods()

burrow.printnocolor()

# TODO: memoization by path

def sort_pods(burrow, energy_so_far, least_energy, path):
  # Two base cases (maybe don't need the first?)
  burrow.printnocolor()
  if energy_so_far >= least_energy:
    print("Too high:", energy_so_far)
    return 100000000
  if burrow.sorted():
    print("Sorted!", path, energy_so_far)
    return energy_so_far
  possible_moves = burrow.possible_moves()
  #print (len(possible_moves), "possible moves")

  #shortest_from_here = least_energy
  for move in possible_moves:
    print ("Trying", move)
    state_before_moving = burrow.pods
    burrow.set_state(move.new_state)
    
    path.append(move.name)
    cost = sort_pods(burrow, energy_so_far + move.cost, least_energy, path)
    if cost < least_energy:
      print("Improvement", least_energy)
      least_energy = cost
    path.pop()
    burrow.pods = state_before_moving
  print ("Tried them all, best was", least_energy)
  return least_energy

energy = sort_pods(burrow, 0, 100000000000, [])
print (energy)

