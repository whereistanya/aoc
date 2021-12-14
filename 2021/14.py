#!/usr/bin/env python

from collections import defaultdict

inputfile = "input.txt"
with open(inputfile, "r") as f:
  code = f.readline().strip()
  _ = f.readline()
  lines = [x.strip() for x in f.readlines()]

print ("Initial code:", code)

matches = {}
for line in lines:
  match, add = line.split(" -> ")
  matches[match] = add

counts = defaultdict(int)
for i in range(0, len(code) - 1):
  pair = (code[i] + code[i+1])
  counts[pair] += 1

for step in range(1, 41):
  newcounts = defaultdict(int)
  for k, v in counts.iteritems():
    if k in matches:
      newchar = matches[k]
      newcounts[ "%s%s" % (k[0], newchar)] += v
      newcounts[ "%s%s" % (newchar, k[1])] += v
    else:
      newcounts[k] = v
  counts = newcounts
  print ("Step %d: %d pairs." % (step, sum(counts.values())))

charcounts = defaultdict(int)
for k, v in counts.iteritems():
  charcounts[k[0]] += v
  charcounts[k[1]] += v

# Add the beginning and end of the line, which are only represented in one pair.
charcounts[code[0]] += 1
charcounts[code[-1]] += 1

for k, v in charcounts.iteritems():
  print(k, v / 2)
  charcounts[k] = v / 2

scounts = sorted(charcounts.values(), reverse=True)

print (scounts[0] - scounts[-1])
