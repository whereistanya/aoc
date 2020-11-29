#!/usr/bin/env python
# Advent of code Day 15.

import sys

class Dungeon(object):
  def __init__(self, lines, elf_attack_power=3, elf_saving = False):
    self.walls = set()  # set of (x, y) tuples
    self.creatures = {} # {(x, y): Creature,}; only used for drawing
    self.ranges = {} # {(x, y): Creature,}
    self.max_x = 0  # min_x is implicitly zero
    self.max_y = 0  # min_y is implicitly zero
    self.elf_power = elf_attack_power
    self.elf_saving = elf_saving
    self.populate(lines)

  def populate(self, lines):
    self.max_y = len(lines) - 1
    for y in range(0, len(lines)):
      line = lines[y]
      if len(line) > self.max_x:
        self.max_x = len(line) - 1
      for x in range(0, len(line)):
        if line[x] == "#":
          self.walls.add((x, y))
        elif line[x] == "G":
          goblin = Creature(x, y, "G")
          self.creatures[(x, y)] = goblin
        elif line[x] == "E":
          elf = Creature(x, y, "E")
          elf.power = self.elf_power
          elf.crash_on_death = self.elf_saving

          self.creatures[(x, y)] = elf
    self.rescan()

  def list_moves(self, point):
    x, y = point
    north = (x, y - 1)
    south = (x, y + 1)
    west = (x - 1, y)
    east = (x + 1, y)
    return [north, south, west, east]

  def alphabetically_earlier(self, a, b):
    ax, ay = a
    bx, by = b
    if ay < by:
      return True
    if by < ay:
      return False
    return ax < bx

  def find_move(self, creature):
    to_try = {} # current_point : initial_step
    seen = set()
    seen.add((creature.x, creature.y))
    for move in creature.moves():
      if self.open(move):
        to_try[move] = move
        seen.add(move)
    while to_try:
      next_seen = set()
      # take one step out from each to_try point in all directions
      next_to_try = {}
      found_on_this_step = {}
      for starting_point in to_try:
        if not self.open(starting_point, avoid_creatures=True):
          continue
        initial = to_try[starting_point]
        enemy = self.enemy_in_range(creature, starting_point)
        if enemy:
          if enemy in found_on_this_step:  # we already have a path to this thing
            existing_step = found_on_this_step[enemy]
            if self.alphabetically_earlier(initial, existing_step):
              found_on_this_step[enemy] = initial
          else: # no path to this thing
            found_on_this_step[enemy] = initial
        else: # didn't find a creature
          for next_move in self.list_moves(starting_point):
            if next_move not in seen:
              next_seen.add(next_move)
              if next_move in next_to_try:
                existing_step = next_to_try[next_move]
                if self.alphabetically_earlier(initial, existing_step):
                  next_to_try[next_move] = initial
              else:
                next_to_try[next_move] = initial

      if found_on_this_step:
        nearest_enemy = sorted(found_on_this_step.keys())[0]
        return found_on_this_step[nearest_enemy]
      else:
        to_try = next_to_try
        seen.update(next_seen)

  def play_a_round(self):
    for creature in sorted(self.creatures.values()):
      if not creature.alive:
        continue
        self.rescan()
      if not self.enemy_count(creature):
        print("No more enemies for", creature.symbol, "to fight")
        return False
      enemy = self.enemy_in_range(creature, lowest_hp=True)
      if enemy:
        enemy.damage(creature.power)
        self.rescan()
        continue
      # otherwise look at steps outwards until you reach enemies.
      next_move = self.find_move(creature)
      if next_move:
        creature.move(next_move)
        # TODO: Rebuilding this table every time is super inefficient
        enemy = self.enemy_in_range(creature, lowest_hp=True)
        if enemy:
          enemy.damage(creature.power)
      self.rescan()
    return True

  def open(self, move, avoid_creatures=True):
    if move in self.walls:
      return False
    x, y = move
    if x < 0 or y < y:
      return False
    if x > self.max_x or y > self.max_y:
      return False
    if avoid_creatures:
      if move in self.creatures and self.creatures[move].alive:  # someone else is there
        return False
    return True

  def enemy_count(self, creature):
    count = 0
    for found in list(self.creatures.values()):
      if found.alive and found.symbol != creature.symbol:
        count += 1
    return count

  def enemy_in_range(self, creature, point=None, lowest_hp=False):
    if not point:
      point = (creature.x, creature.y)
    if point not in self.ranges:
      return None
    enemies = []
    for found in self.ranges[point]:
      if found.symbol != creature.symbol:
        enemies.append(found)
    if not enemies:
      return None

    if lowest_hp: # hitpoint sort
      lowest = 9999999
      options = []
      for found in enemies:
        if found.hitpoints < lowest:
          lowest = found.hitpoints
          options = [found]
        elif found.hitpoints == lowest:
          options.append(found)
      return sorted(options)[0]
    else: # regular alpha sort
      return sorted(enemies)[0]

  def rescan(self):
    new_creature_map = {}
    new_ranges_map = {}
    for creature in list(self.creatures.values()):
      if not creature.alive:
        continue
      new_creature_map[(creature.x, creature.y)] = creature
      for move in self.list_moves((creature.x, creature.y)):
        if self.open(move, avoid_creatures=False):
          try:
            (new_ranges_map[move]).append(creature)
          except KeyError:
            new_ranges_map[move] = [creature]
    self.creatures = new_creature_map
    self.ranges = new_ranges_map

  def draw(self):
    for y in range(0, self.max_y + 1):
      s = "%02d:" % y
      suffix = "   "  # drawn at the end of this line
      for x in range(0, self.max_x + 1):
        if (x, y) in self.walls:
          s += "#"
        else:
          try:
            creature = self.creatures[(x, y)]
            if creature.alive:
              suffix += "%s, " % str(creature)
              s += creature.symbol
            else:
              s += "."
              suffix += "(rip), "
          except KeyError:
            s += "."

      print(s, suffix)

class Creature(object):
  def __init__(self, x, y, symbol, crash_on_death=False):
    self.x = x
    self.y = y
    self.hitpoints = 200
    self.power = 3
    self.alive = True
    self.crash_on_death = crash_on_death
    self.symbol = symbol  # "E"=elf or "G"=goblin.

  def __repr__(self):
    return "%s(%d/%d,%d)" % (self.symbol, self.hitpoints, self.x, self.y)
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
  def __lt__(self, other):
    if self.y < other.y:
      return True
    if other.y < self.y:
      return False
    return self.x < other.x

  def moves(self):
    north = (self.x, self.y - 1)
    south = (self.x, self.y + 1)
    west = (self.x - 1, self.y)
    east = (self.x + 1, self.y)
    return [north, south, west, east]

  def move(self, point):
    self.x = point[0]
    self.y = point[1]

  def damage(self, amount):
    self.hitpoints -= amount
    if self.hitpoints < 0:
      self.alive = False
      if self.symbol == "E" and self.crash_on_death:
        print("UNACCEPTABLE DEATH OF", self.symbol)
        sys.exit(0)

def run(lines, draw_all = False, elf_attack_power=3, elf_saving=False):
  game = Dungeon(lines, elf_attack_power, elf_saving)
  if draw_all:
    game.draw()
  i = 0
  while game.play_a_round():
    if draw_all:
      print("***** round %d *****" % i)
      game.draw()
    i += 1

  hp = 0
  for creature in list(game.creatures.values()):
    if creature.alive:
      hp += creature.hitpoints

  print(i)
  print(hp)
  print(i * hp)
  return i * hp

# Tests

lines1 = [
  "#########",
  "#G..G..G#",
  "#.......#",
  "#.......#",
  "#G..E..G#",
  "#.......#",
  "#.......#",
  "#G..G..G#",
  "#########",
 ]

#run(lines1, draw_all=True)

lines2 = [
  "#######",
  "#.G...#",
  "#...EG#",
  "#.#.#G#",
  "#..G#E#",
  "#.....#",
  "#######",
]
#assert run(lines2) == 27730

lines3 = [
  "#######",
  "#G..#E#",
  "#E#E.E#",
  "#G.##.#",
  "#...#E#",
  "#...E.#",
  "#######",
] # expect 36334 <-- fails
#assert run(lines3) == 36334

lines4 = [
  "#######",
  "#E..EG#",
  "#.#G.E#",
  "#E.##E#",
  "#G..#.#",
  "#..E#.#",
  "#######",
]
#assert run(lines4) == 39514

# main

lines = [
  "################################",
  "##############..######....######",
  "###########GG.G.#######.########",
  "############....######..#..#####",
  "############...#######.....#####",
  "##############..#G.####....#####",
  "#############..G#..####...######",
  "######.#####.G...G..###.#.######",
  "######...###..........#.########",
  "######G.................#.######",
  "######....G.#............G.#####",
  "######G......G............######",
  "######.......E#####E.G.....#####",
  "#####...G....#######.......#####",
  "#####.......#########......#####",
  "########....#########.....######",
  "########G.G.#########...########",
  "#########...#########.......#.##",
  "########.G..#########..........#",
  "#######.E....#######........#..#",
  "#...........G.#####...E...######",
  "####.....##................#####",
  "#####..#.####.#.............####",
  "########...##EE..G....E.#..E.###",
  "##########..#................###",
  "##########.............#.....###",
  "###########.E.G..........##.####",
  "###########.........###..##.####",
  "############.##........E.#######",
  "################.###.###########",
  "################.###############",
  "################################",
]

# Part 1
run(lines)

# Part 2... manually changing and binary searching
run(lines, elf_attack_power=19, elf_saving=True)
