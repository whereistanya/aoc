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

  def neighbours(self, diagonal=True, default_value=""):
    return self.grid.neighbours(self, diagonal=diagonal,
                                default_value=default_value)

  def __repr__(self):
    s = "Point(%d,%d)[%s]" % (self.x, self.y, self.value)
    return s

class Grid(object):
  def __init__(self, lines):
    self.lines = lines # [str, str, ...]
    self.grid = {}  # (x, y): Point
    self.minx = 0
    self.miny = 0
    # max is actually one more than the max, for ease of ranges.
    self.maxx = 0
    self.maxy = 0
    self.populate()

  def neighbours(self, point, diagonal=True, default_value=""):
    #print("Getting neighbours for %d,%d" % (point.x,point.y))
    x = point.x
    y = point.y
    neighbours = []
    if diagonal:
      to_add = [(x - 1, y - 1), (x  , y - 1), (x + 1, y - 1),
                (x - 1, y    ), (x  , y    ), (x + 1, y    ),
                (x - 1, y + 1), (x  , y + 1), (x + 1, y + 1)]
    else:
      to_add = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    for neighbour in to_add:
      if neighbour in self.grid:
        neighbours.append(self.grid[neighbour])
        self.grid[neighbour].color = color.DARKCYAN
      else:
        neighbours.append(None)
      #  if default_value != "":
      #    print("Neighbour %d,%d doesn't exist yet. Creating it." %
      #          (neighbour[0], neighbour[1]))
      #    new_point = self.addpoint(neighbour[0], neighbour[1], default_value)
      #    neighbours.append(new_point)
      #    new_point = color.YELLOW
    return neighbours

  def addpoint(self, x, y, value):
    #print("Creating a new point at %d,%d" % (x, y))
    new_point = Point(x, y, value, self)
    new_point.color = color.YELLOW
    self.grid[(x, y)] = new_point
    if x >= self.maxx:
      self.maxx = x + 1
    if x < self.minx:
      self.minx = x
    if y >= self.maxy:
      self.maxy = y + 1
    if y < self.miny:
      self.miny = y
    return new_point

  def setvalue(self, x, y, value):
    #print("setvalue %d, %d, %s" % (x, y, value))
    if (x, y) in self.grid:
      self.grid[(x, y)].value = value
    else:
      self.addpoint(x, y, value)

  def getpoint(self, x, y, default_value=None):
    #print("getpoint  %d,%d" % (x, y))
    if (x, y) in self.grid:
      return self.grid[(x, y)]
    elif default_value:
      point = self.addpoint(x, y, default_value)
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
 
