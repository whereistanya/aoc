#!/usr/bin/env python
# AoC 2020 day 25.

def transform(value, subject):
	value = value * subject
	value = value % 20201227
	return value

k1 = 3248366
k2 = 4738476

loop1 = 0
loop2 = 0
subject = 7

val = 1
while True:
	loop1 += 1
	val = transform(val, subject)
	if val == k1: break

val = 1
while True:
	loop2 += 1
	val = transform(val, subject)
	if val == k2: break

val = 1
for i in range(loop2):
	val = transform(val, k1)
print (val)

val = 1
for i in range(loop1):
	val = transform(val, k2)
print(val)

