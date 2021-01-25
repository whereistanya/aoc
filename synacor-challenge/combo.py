#!/usr/bin/env python3

import itertools

x = [2, 9, 3, 7, 5]

for l in itertools.permutations(x):
  a, b, c, d, e = l
  total = a + b * pow(c, 2) + pow(d, 3) - e
  if total == 399:
    print (a, b, c, d, e, total)
