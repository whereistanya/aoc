# from pydroid on my phone. Formatting will be weird.

with open("/storage/emulated/0/Download/5.txt") as f:
	lines = f.readlines()
	
def test():
	lines = """0,9 -> 5,9
	8,0 -> 0,8
	9,4 -> 3,4
	2,2 -> 2,1
	7,0 -> 7,4
	6,4 -> 2,0
	0,9 -> 2,9
	3,4 -> 1,4
	0,0 -> 8,8
	5,5 -> 8,2""".split("\n")
	return lines

#lines = test()	
points = {}

for line in lines:
	f, t = line.strip().split(" -> ")
	fx, fy = [int(x) for x in f.split(",")]
	tx, ty = [int(x) for x in t.split(",")]
	if fx == tx: #it's horizontal
		pass # part1 code, skipped for part2
		small = min(fy, ty)
		big = max(fy, ty)
		for i in range(small, big + 1):
			try:
				points[(fx, i)] += 1
			except KeyError:
				points[(fx, i)] = 1
	elif fy == ty: # it's vertical
		pass # part1 code, skipped for part2
		small = min(fx, tx)
		big = max(fx, tx)
		for i in range(small, big + 1):
			try:
				points[(i, ty)] += 1
			except KeyError:
				points[(i, ty)] = 1
	else: # it's diagonal, part2 only
		try:
			points[(fx,fy)] += 1
		except KeyError:
			points[(fx, fy)] = 1
		if fx > tx:
			xmovement = -1
		elif fx < tx:
			xmovement = 1
		else:
			xmovement = 0
		if fy > ty:
			ymovement = -1
		elif fy < ty:
			ymovement = 1
		else:
			ymovement = 0
		while fx != tx: # guaranteed 45 deg angles
								# so this should be ok
			fx += xmovement
			fy += ymovement
			try:
				points[(fx,fy)] += 1
			except KeyError:
				points[(fx, fy)] = 1
	

count = 0
for k in points:
	if points[k] > 1:
		count += 1

print (count)
				

