#!/usr/bin/env python3

test = True
test = False

if test:
  filename = "test18.txt"
else:
  filename = "input18.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

# Part 1
cubes = set()
for line in lines:
  x, y, z= [int(x) for x in line.split(",")]
  cubes.add((x, y, z))

exposed_faces = 0
empty_space = set()
for cube in cubes:
  x, y, z = cube
  neighbours = [ (x - 1, y, z), (x + 1, y, z),
                 (x, y - 1, z), (x, y + 1, z),
                 (x, y, z - 1), (x, y, z + 1) ]
  for n in neighbours:
    if n not in cubes:
      exposed_faces += 1
      empty_space.add(n)

print("Part 1:", exposed_faces)

# Part 2, find the air pockets
# Volume of a sphere is 3 * surface area / radius so, even though this isn't
# a neat sphere, the volume's not going to be much more than the number of
# cubes in the surface area.
# So walk out from some of the empty spaces, exploring until we run out of space
# (i.e., it's a pocket) or have too much volume (it's just open air), then pick
# another empty space, repeat. Now we have all the cubes that are in a pocket.
# Use the part1 code to see which ones don't touch air; count those faces and
# subtract them from the total number of faces.

approximate_size_of_infinite_space = len(cubes) * 3 # ok, a little larger..
pockets = {}
to_explore = set(empty_space)
while to_explore:
  start = to_explore.pop()
  pocket = True
  found = set([start]) # empty space only
  to_check = [start]
  while to_check:
    current = to_check.pop()
    x, y, z = current
    neighbours = [ (x - 1, y, z), (x + 1, y, z),
                   (x, y - 1, z), (x, y + 1, z),
                   (x, y, z - 1), (x, y, z + 1) ]
    for n in neighbours:
      if n not in cubes:
        if n not in found:
          to_check.append(n)
        if n in to_explore:
          to_explore.remove(n)
        found.add(n)
    if len(found) > approximate_size_of_infinite_space:
      #print("Found %d empty spaces (from %s). This is air." % (len(found), start))
      pocket = False
      break
  if pocket:
    pockets[start] = found

internal_faces = 0

for pocket in pockets.values():
  for aircube in pocket:
    x, y, z = aircube
    neighbours = [ (x - 1, y, z), (x + 1, y, z),
                 (x, y - 1, z), (x, y + 1, z),
                 (x, y, z - 1), (x, y, z + 1) ]
    for n in neighbours:
      if n not in pocket:
        internal_faces += 1

#print("%d internal faces" % internal_faces)
print("Part 2:", exposed_faces - internal_faces)

