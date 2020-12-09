#!/usr/bin/env python

with open("input1.txt", "r") as f:
  lines = [int(x.strip()) for x in f.readlines()]

for i in lines:
  for j in lines:
    if i + j == 2020:
      print i * j

for i in lines:
  for j in lines:
    for k in lines:
      if i + j + k == 2020:
        print i, j, k
        print i * j * k


