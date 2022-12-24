from collections import defaultdict
# TODO: rewrite with defaultdict

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Point(object):
  def __init__(self, x, y, value, grid):
    self.x = x
    self.y = y
    self.value = value
    self.color = color.GREEN
    self.grid = grid

  def neighbours(self, diagonal=True, default_value="", prune=False):
    nabes = self.grid.neighbours(self, diagonal=diagonal,
                                 default_value=default_value)
    if prune:
      nabes = [x for x in nabes if x]
    return nabes

  def neighbours_by_direction(self):
    return self.grid.neighbours_by_direction(self)

  def __repr__(self):
    s = "Point(%d,%d)[%s]" % (self.x, self.y, self.value)
    return s

class Grid(object):
  """x increases to the east/right, y increases to the south/down"""
  def __init__(self, lines):
    self.lines = lines # [str, str, ...]
    self.grid = {}  # (x, y): Point
    self.minx = 0
    self.miny = 0
    # max is actually one more than the max, for ease of ranges.
    self.maxx = 0
    self.maxy = 0
    self.populate()

  def nw_xy(self, point):
    return (point.x - 1, point.y - 1)

  def n_xy(self, point):
    return (point.x, point.y - 1)

  def ne_xy(self, point):
    return (point.x + 1, point.y - 1)

  def e_xy(self, point):
    return (point.x + 1, point.y)

  def w_xy(self, point):
    return (point.x - 1, point.y)

  def sw_xy(self, point):
    return(point.x - 1, point.y + 1)

  def s_xy(self, point):
    return (point.x, point.y + 1)

  def se_xy(self, point):
    return(point.x + 1, point.y + 1)

  def neighbours(self, point, diagonal=True, default_value=""):
    #print("Getting neighbours for %d,%d" % (point.x,point.y))
    neighbours = []
    if diagonal:
      # order is:
      # nw, n, ne, w, self, e, sw, s, se
      to_add = [self.nw_xy(point), self.n_xy(point),  self.ne_xy(point),
                self.w_xy(point),  (point.x, point.y),self.e_xy(point),
                self.sw_xy(point), self.s_xy(point),  self.s_xy(point)]
    else:
      to_add = [self.e_xy(point), self.w_xy(point),
                self.s_xy(point), self.n_xy(point)]
    for neighbour in to_add:
      if neighbour in self.grid:
        neighbours.append(self.grid[neighbour])
      else:
        neighbours.append(None)
      #  if default_value != "":
      #    print("Neighbour %d,%d doesn't exist yet. Creating it." %
      #          (neighbour[0], neighbour[1]))
      #    new_point = self.create_point(neighbour[0], neighbour[1], default_value)
      #    neighbours.append(new_point)
      #    new_point = color.YELLOW
    return neighbours

  def neighbours_by_direction(self, point, diagonal=True):
    fns = {
      "northwest": self.nw_xy,
      "north": self.n_xy,
      "northeast": self.ne_xy,
      "west": self.w_xy,
      "east": self.e_xy,
      "southwest": self.sw_xy,
      "south": self.s_xy,
      "southeast": self.se_xy,
    }
    neighbours = {}
    for direction, fn in fns.items():
      p = fn(point)
      if p in self.grid:
        neighbours[direction] = self.grid[p]
      else:
        neighbours[direction] = None
    return neighbours


    if diagonal:
      # order is:
      # nw, n, ne, w, self, e, sw, s, se
      to_add = [self.nw_xy(point), self.n_xy(point),  self.ne_xy(point),
                self.w_xy(point),  (point.x, point.y),self.e_xy(point),
                self.sw_xy(point), self.s_xy(point),  self.s_xy(point)]
    else:
      to_add = [self.e_xy(point), self.w_xy(point),
                self.s_xy(point), self.n_xy(point)]
    for neighbour in to_add:
      if neighbour in self.grid:
        neighbours.append(self.grid[neighbour])
      else:
        neighbours.append(None)
      #  if default_value != "":
      #    print("Neighbour %d,%d doesn't exist yet. Creating it." %
      #          (neighbour[0], neighbour[1]))
      #    new_point = self.create_point(neighbour[0], neighbour[1], default_value)
      #    neighbours.append(new_point)
      #    new_point = color.YELLOW
    return neighbours

  def create_point(self, x, y, value):
    #print("Creating a new point at %d,%d" % (x, y))
    new_point = Point(x, y, value, self)
    new_point.color = color.YELLOW
    return self.addpoint(new_point)

  def addpoint(self, point):
    x = point.x
    y = point.y
    self.grid[(x, y)] = point
    if x >= self.maxx:
      self.maxx = x + 1
    if x < self.minx:
      self.minx = x
    if y >= self.maxy:
      self.maxy = y + 1
    if y < self.miny:
      self.miny = y
    return point

  def setvalue(self, x, y, value):
    #print("setvalue %d, %d, %s" % (x, y, value))
    if (x, y) in self.grid:
      self.grid[(x, y)].value = value
    else:
      self.create_point(x, y, value)

  def get_by_char(self, char):
    return [v for k, v in self.grid.items() if v.value == char]

  def getpoint(self, x, y, default_value=None):
    #print("getpoint  %d,%d" % (x, y))
    if (x, y) in self.grid:
      return self.grid[(x, y)]
    elif default_value:
      point = self.create_point(x, y, default_value)
      return point
    return None

  def populate(self):
    self.minx = 0
    self.miny = 0
    self.maxx = len(self.lines[0])
    self.maxy = len(self.lines)
    for y in range(self.miny, self.maxy):
      for x in range(self.minx, self.maxx):
        try:
          self.grid[(x, y)] = Point(x, y, self.lines[y][x], self)
        except IndexError:
          # skip missing points
          pass

  def printgrid(self):
    for y in range(self.miny, self.maxy):
      s = "%2d " % y
      for x in range(self.minx, self.maxx):
        if (x, y) not in self.grid:
          s += "_"
          continue
        s += (self.grid[(x, y)].color + "%s" % self.grid[(x, y)].value +
              color.END)
      print(s)
    print("\n")
    print("x: min %d, max %d" % (self.minx, self.maxx))
    print("y: min %d, max %d" % (self.miny, self.maxy))

  def printnocolor(self):
    for y in range(self.miny, self.maxy):
      s = "%2d " % y
      for x in range(self.minx, self.maxx):
        if (x, y) not in self.grid:
          s += "_"
          continue
        s += "%s" % self.grid[(x, y)].value
      print(s)
 
