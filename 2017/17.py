#!/usr/bin/env python
# Advent of code Day 17.

inputvalue = 348

#inputvalue = 3

circular_buffer = [0]  # probably better as a linked list

position = 0

posone = set()

length = 1

i = 1
while i < 50000000:
  # For part two, don't actually need to insert it, just act as if we did.
  #position = ((position + inputvalue) % len(circular_buffer)) + 1
  #circular_buffer.insert(position, i)
  position = ((position + inputvalue) % length) + 1
  length += 1

  if position == 1:
    print "Inserting", i, "at position one"
    circular_buffer.insert(position, i)
  if circular_buffer[0] != 0:
    print "Value", circular_buffer[0], "for start"
    exit()
  if circular_buffer[1] not in posone:
    print circular_buffer[1]
    posone.add(circular_buffer[1])
  i += 1

print circular_buffer[position]
#print circular_buffer[position + 1]
print sorted(posone)
