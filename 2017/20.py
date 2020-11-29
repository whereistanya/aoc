#!/usr/bin/env python

# Advent of code 2017 day 20.
# This feels like an inelegant solution but it works fine?

import re

class Particle(object):
  def __init__(self, px, py, pz, vx, vy, vz, ax, ay, az):
    self.px = int(px)
    self.py = int(py)
    self.pz = int(pz)
    self.vx = int(vx)
    self.vy = int(vy)
    self.vz = int(vz)
    self.ax = int(ax)
    self.ay = int(ay)
    self.az = int(az)
    self.alive = True

  def distance(self):
    return abs(self.px) + abs(self.py) + abs(self.pz)

  def move(self):
    self.vx += self.ax
    self.vy += self.ay
    self.vz += self.az
    self.px += self.vx
    self.py += self.vy
    self.pz += self.vz

with open("input20.txt", "r") as f:
  lines = f.readlines()

line_re = "^p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>$"

"""
lines = [
  "p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>",
  "p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>"
]
"""

particles = []

for line in lines:
  groups = re.search(line_re, line).groups()
  px, py, pz, vx, vy, vz, ax, ay, az = groups
  particle = Particle(px, py, pz, vx, vy, vz, ax, ay, az)
  particles.append(particle)


for i in range (0, 1000): # Arbitrary max
  locations = {}

  for p in range (0, len(particles)):
    particle = particles[p]
    particle.move()
    if not particle.alive:
      continue
    location = (particle.px, particle.py, particle.pz)
    try:
      locations[location].append(p)
    except KeyError:
      locations[location] = [p]
  for k in locations:
    if len(locations[k]) > 1:
      for p in locations[k]:
        print("Alas, particle", p)
        particles[p].alive = False

smallest_p = -1
smallest_distance = 100000000000000

for p in range (0, len(particles)):
  distance = particles[p].distance()
  print("Particle", p, " has distance", particles[p].distance())
  if distance < smallest_distance:
    smallest_distance = distance
    smallest_p = p

print("Smallest was", smallest_p)

alive = 0
for particle in particles:
  if particle.alive:
    alive += 1
print(alive, "particles are still alive")
