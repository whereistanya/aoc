#!/usr/bin/env python3

from collections import defaultdict
from collections import deque

inputfile = "input19.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

def test():
  lines = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""".split("\n")
  return lines

def test2():
  lines = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390""".split("\n")
  return lines

def test3():
  lines="""--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""".split("\n")
  return lines

class Beacon(object):
  def __init__(self, name, s, scanner):
    self.name = name
    self.originally_seen_by = scanner
    self.x, self.y, self.z = [int(x) for x in s.split(",")]
    self.seen_by = {}  # scanner: coords
    self.seen_by[scanner] = (self.x, self.y, self.z)
    self.distances = {}
    self.distance_set = set()

  def __repr__(self):
    s = "B%d(%s,%s,%s)" % (self.name, self.x, self.y, self.z)
    return s

  def record_distance_from(self, other):
    # tuple of the three distances away (x/y/z), sorted by length
    distance = tuple(sorted([abs(self.x - other.x), abs(self.y - other.y), abs(self.z - other.z)]))
    self.distances[other] = distance
    self.distance_set.add(distance) # TODO create it at the end from distances instead

class Scanner(object):
  def __init__(self, name):
    self.name = name
    self.beacons = [] # Beacon, ...
    self.distances = set()

  def __repr__(self):
    return ("Scanner%s(%d beacons)" % (self.name, len(self.beacons)))

#lines = test3()

scanners = []  # [Scanner, ...]
beacons = []   # [Beacon, ...]

beacon_index = 0

for line in lines:
  if line == "":
    continue
  if line.startswith("---"):
    scanner = Scanner(line.split("--- scanner ")[1].split(" ---")[0])
    scanners.append(scanner)
    continue
  beacon = Beacon(beacon_index, line, scanner)
  beacon_index += 1
  scanner.beacons.append(beacon)
  beacons.append(beacon)

distance_count = defaultdict(int)

# update beacons' distances from each other. Inefficient and clunky. Rewrite.
for s in scanners:
  for beacon_i in s.beacons:
    for beacon_j in s.beacons:
      if beacon_i == beacon_j:
        continue
      beacon_i.record_distance_from(beacon_j)


deduped = defaultdict(list)

# Now cycle through all the beacons, looking at their distances to other
# beacons. Two beacons that have an overlapping set of distances are probably
# the same beacon.
for i in beacons:
  found = False
  for j in deduped:
    if i == j:
      continue
    overlap = len(i.distance_set.intersection(j.distance_set))

    if overlap > 1:
      # i and j are the same beacon. Combine them, keeping j (the one already in
      # the deduped list) and forgetting i
      #print("%s and %s have %d in common" % (i, j, overlap))
      deduped[j].append(i)
      original_scanner = i.originally_seen_by
      # x/y/z are subjective and lies so sort for convenience
      j.seen_by[original_scanner] = (i.x, i.y, i.z)

      # Tell i's original scanner that it saw this one instead
      original_scanner.beacons.remove(i)
      # TODO: make sure not to use the x/y/z coords here though; they
      # 're from another scanner's pov
      original_scanner.beacons.append(j)
      found = True
      break
  if not found:
    deduped[i] = []

#print (deduped)
print ("Part1: %d" % len(deduped))

# So now we have the 367 beacons.
# Suppose we say scanner0 is at 0,0, and all its beacons' coords are absolute,
# and everything else is relative.
# Look at each of scanner1's beacons, and find their other names. We know their
# real positions, so update the scanners that found them accordingly.

# But some of the scanners are upside down, etc, so we need to triangulate

def all_angles(coords):
  # TODO: only 24 are possible, but I don't know which 24
  # TODO: ideally this would return functions/lambdas, not numbers
  #       Then try each function in turn and choose one
  a, b, c = coords
  possibilities = [
    (a, b, c),
    (a, c, b),
    (b, a, c),
    (b, c, a),
    (c, a, b),
    (c, b, a),
  ]
  negations = [
    (1, 1, 1),
    (1, 1, -1),
    (1, -1, 1),
    (1, -1, -1),
    (-1, 1, 1),
    (-1, 1, -1),
    (-1, -1, 1),
    (-1, -1, -1)
  ]
  to_return = []
  for p in possibilities:
    for n in negations:
      # sorry, future-me. Aiming to zip the two tuples
      # together so like (2, 4, 6) zipped with (1, 1, -1)
      # makes (2, 4, -6)
      to_return.append(tuple([a * b for a, b in zip(p, n)]))
  return to_return


# Find the real locations of the scanners and beacons
real_scannner_coords = {}
real_beacon_coords = {}

all_beacons = deque(deduped.keys())

scanner = scanners[0]
real_scannner_coords[scanner] =(0, 0, 0)
for beacon in scanner.beacons:
  real_beacon_coords[beacon] = beacon.seen_by[scanner]
  all_beacons.remove(beacon)

unmoored_scanners = deque(scanners[1:])
while(unmoored_scanners):
  print(len(unmoored_scanners), "left")
  scanner = unmoored_scanners.popleft()
  print("*** Finding a position for scanner:", scanner)
  # TODO: choose a data structure seriously
  situated_beacons = list(set(scanner.beacons).intersection(set(real_beacon_coords.keys())))
  if len(situated_beacons) < 2:
    unmoored_scanners.append(scanner)
    continue

  anchor_beacon = situated_beacons[0]
  anchor_real_location = real_beacon_coords[anchor_beacon]
  anchor_relative_coords = anchor_beacon.seen_by[scanner]
  anchor_relative_possibilities = all_angles(anchor_relative_coords)

  # TODO: I'm spinning the beacons; should I be spinning the anchor?
  scanner_orientation = -999

  for i in range(0, len(anchor_relative_possibilities)):
    new_beacon_real_locations = []
    #print(i, anchor_relative_possibilities[i])
    anchorx, anchory, anchorz = anchor_relative_possibilities[i]
    scanner_possible_real_location = (
      anchor_real_location[0] + anchorx,
      anchor_real_location[1] + anchory,
      anchor_real_location[2] + anchorz)
    # test whether this scanner location works for all other beacons
    works = True
    for test_beacon in situated_beacons[1:]:
      #print("Comparing against", test_beacon)
      test_beacon_real_location = real_beacon_coords[test_beacon]
      test_beacon_relative_coords = test_beacon.seen_by[scanner]
      test_beacon_relative_possibilities = all_angles(test_beacon_relative_coords)

      bx, by, bz = test_beacon_relative_possibilities[i]

      test_beacon_possible_real_location = (
        scanner_possible_real_location[0] - bx,
        scanner_possible_real_location[1] - by,
        scanner_possible_real_location[2] - bz)
      #print("Looking at", test_beacon_possible_real_location)
      if test_beacon_possible_real_location == test_beacon_real_location:
        #print("DING DING DING")
        pass
      else:
        #print ("BZZZT doesn't work")
        works = False
        break
    if works:
      scanner_orientation = i
      for beacon in scanner.beacons:
        if beacon not in situated_beacons:
          possible_locations = all_angles(beacon.seen_by[scanner])
          bx, by, bz = possible_locations[i]
          sx, sy, sz = scanner_possible_real_location
          real_beacon_coords[beacon] = (sx -bx, sy - by, sz - bz)

      real_scannner_coords[scanner] = scanner_possible_real_location
      break

  if scanner_orientation == -999:
    unmoored_scanners.append(scanner)
    continue

  print (real_scannner_coords)

biggest = 0
for i in real_scannner_coords:
  ix, iy, iz = real_scannner_coords[i]
  for j in real_scannner_coords:
    jx, jy, jz = real_scannner_coords[j]
    dist = abs(ix - jx) + abs(iy - jy) + abs(iz - jz)
    if dist > biggest:
      biggest = dist
print(biggest)
