#!/usr/bin/env python
# Advent of code Day 6.

import math

def orbitcount(node, orbits, counts):
  if node in counts:
    return counts[node]
  if node not in orbits:
    print("%s doesn't orbit anything" % node)
    return 0
  counts[node] = orbitcount(orbits[node], orbits, counts) + 1
  print("%s orbits %d things" % (node, counts[node]))
  return counts[node]

def get_path(node, orbits, path):
  path.append(node)
  if node not in orbits:
    return
  get_path(orbits[node], orbits, path)

with open("input.txt", "r") as f:
  lines = f.readlines()

  """
  lines = [
  "COM)B",
	"B)C",
	"C)D",
	"D)E",
	"E)F",
	"B)G",
	"G)H",
	"D)I",
	"E)J",
	"J)K",
	"K)L",
  "K)YOU",
  "I)SAN",
  ]
  #"""
  orbits = {}   # key orbits value
  counts = {}
  for line in lines:
    nodes = line.strip().split(")")
    orbits[nodes[1]] = nodes[0]
    print(("%s orbits %s" % (nodes[1], nodes[0])))

  total = 0
  counts = {}
  for node in orbits:
    n = orbitcount(node, orbits, counts)
    total += n

  print("Total orbits is %d" % total)

  patha = []
  pathb = []
  get_path(orbits["YOU"], orbits, patha)
  get_path(orbits["SAN"], orbits, pathb)
  nodesa = set(patha)
  nodesb = set(pathb)

  print(patha)
  count = 0
  for node in patha:
    count += 1
    if node in nodesb:
      print(node)
      break

  for node in pathb:
    count += 1
    if node in nodesa:
      print(node)
      break

  print(count - 2)
