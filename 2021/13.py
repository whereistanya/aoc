# Created in pydroid on phone

with open("/storage/emulated/0/Download/13.txt") as f:
    lines = [x.strip() for x in f.readlines()]

def test():
    return """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".split("\n")


grid = {} # (x, y): char

#lines = test()
#print (lines[0])
dots = []
folds = []
for line in lines:
    if line == "":
        continue
    elif line.startswith("fold"):
        folds.append(line)
    else:
        dots.append(line)

for x in range(0, 2000):
    for y in range (0, 2000):
        grid[(x,y)] = "."

maxx = 0
maxy = 0

for dotline in dots:
    #print("(%s)" % dotline)
    xs, ys = dotline.split(",")
    x = int(xs)
    y = int(ys)
    grid[(x,y)] = "#"
    if x > maxx:
        maxx = x
    if y > maxy:
        maxy = y

#first = folds[0].split("fold along ")[1]
for f in folds:
    fold = f.split("fold along ")[1]
    #print(fold)
    axis, val = fold.split("=")
    val = int(val)
    if axis=="y":
        for i in range(0, maxx):
            grid[(i, val)] = "-"
        i = 1
        # horiz fold, fold up
        while True:
            try:
                for x in range(0, maxx + 1):
                    if grid[(x, val + i)] == "#":
                        grid[(x, val - i )] = "#"
                i += 1
            except KeyError:
                break
        maxy = val
    elif axis == "x":
        for i in range(0, maxy):
            grid[(val, i)] = "|"
        i = 1
        while True:
            try:
                for y in range(0, maxy + 1):
                    if grid[(val + i, y)] == "#":
                        grid[(val - i, y)] = "#"
                i += 1
            except KeyError:
                break
        maxx = val
    else:
        print("BUG", axis)
        exit(0)

for y in range(0, maxy + 1):
    s = ""
    for x in range(0, maxx + 1):
        s += grid[(x, y)]
    print( s)

count = 0
for x in range(0, maxx + 1):
    for y in range(0, maxy + 1):
        if grid[(x,y)] == "#":
            count += 1
#print(count)
