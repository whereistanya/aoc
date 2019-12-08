#!/usr/bin/env python
# Advent of code Day 8.

import os
import time

class Layer(object):
  def __init__(self, data):
    self.data = data
    self.digits = {}
    for digit in data:
      try:
        self.digits[int(digit)] += 1
      except KeyError:
        self.digits[int(digit)] = 1

  def count(self, digit):
    try:
      return self.digits[digit]
    except KeyError:
      return 0

with open("input.txt", "r") as f:
  data = list(f.read().strip())

width = 25
height = 6
layersize = width * height

i = 0
zeroes = 99999999
solution = 0

layers = []
while i < len(data):
  layer = Layer(data[i:i+layersize])
  if layer.count(0) < zeroes:
    zeroes = layer.count(0)
    solution = layer.count(1) * layer.count(2)
  layers.append(layer)
  i += layersize

print solution

pixels = []  # 150
for i in range(0, layersize):
  pixels.append(-1)

for l in range(len(layers) -1, -1, -1):
  layer = layers[l]
  for i in range(0, layersize):
    pixel = layer.data[i]
    if pixel != "2":
      pixels[i] = pixel

s = ""
#os.system('clear')
for i in range(0, len(pixels)):
  if i % width == 0:
    s += "\n|"
  if pixels[i] == "0":
    s += "#"
  else:
    s += " "
print s
