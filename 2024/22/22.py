#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib

from collections import defaultdict

filename = "input.txt"
#filename = "test1"
lines = ["1", "2", "3", "2024"]

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

def mixv(secret, value):
  return secret ^ value

def prunev(secret):
  return secret % 16777216

def evolvev(secret):
  value = secret * 64
  secret = mixv(secret, value)
  secret = prunev(secret)

  value = int(secret / 32)
  secret = mixv(secret, value)
  secret = prunev(secret)

  value = secret * 2048
  secret = mixv(secret, value)
  secret = prunev(secret)
  return secret

part1 = 0
part2 = 0

# sequesnce of four changes in price

seqs = defaultdict(int) # (n,n,n,n): int  tuple of sequence: totalprice

for line in lines:
  #print("###", line)
  secret = int(line)
  prices = []
  used = defaultdict(bool)
  for i in range(2000):
    secret = evolvev(secret)
    price = secret % 10
    prices.append(price)
    if i >= 4:
      seq = (prices[i-3] - prices[i-4],
             prices[i-2] - prices[i-3],
             prices[i-1] - prices[i-2],
             prices[i] - prices[i-1])
      if not used[seq]:
        seqs[seq] += price
        used[seq] = True
  part1 += secret

sseqs = sorted(seqs.items(), key=lambda x:x[1], reverse=True)

print("Best sequence is", sseqs[0])
part2 = sseqs[0][1]

print("Part 1:", part1)
print("Part 2:", part2)
