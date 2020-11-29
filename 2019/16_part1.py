#!/usr/bin/python

import math
import sys
import time


base = [0, 1, 0, -1]

#patterns = {}

#def value(i, o):
  #try:
  #  pattern = patterns[o]
  #except KeyError:
  #  pattern = []
  #  for b in base:
  #    pattern.extend([base[b]] * (o))
  #  patterns[o] = pattern
  #ret = pattern[i % len(pattern)]
#  return base[(int(i * 1.0 / o) % len(base))]

# phase.
# input: 5 digit list, [9, 8, 7, 6, 5]
# output: 5 digit list
s = "6931716349294"
b = "59777373021222668798567802133413782890274127408951008331683345339720122013163879481781852674593848286028433137581106040070180511336025315315369547131580038526194150218831127263644386363628622199185841104247623145887820143701071873153011065972442452025467973447978624444986367369085768018787980626750934504101482547056919570684842729787289242525006400060674651940042434098846610282467529145541099887483212980780487291529289272553959088376601234595002785156490486989001949079476624795253075315137318482050376680864528864825100553140541159684922903401852101186028076448661695003394491692419964366860565639600430440581147085634507417621986668549233797848"

s= ""
for i  in range(0, 10000):
  s += b
print("s starts at", len(s))
to_skip = int(s[0:7])
s = s[to_skip:]

print("Need ", len(s) * 10000 - to_skip, "from the end")
print("s at the end will be", len(s), "digits")

# Next: figure out if skipping len(s) gives the same result as startng at zero.
output_list = [int(x) for x in s]

i = 0
length = len(output_list)
print(length)
while True:
  i += 1
  array = output_list
  if to_skip == 0:
    output_list = []
  else:
    output_list = [0] * (to_skip - 1)

  print("from %d to %s" % (1, length +1))
  for out in range(1, length + 1): # each element of output list
    total = 0
    for inp in range(out - 1, length):   # input list
      pattern_value = base[(int((inp + 1) * 1.0 / out) % len(base))]
      if pattern_value == 0:
        continue
      result = array[inp] * pattern_value
      if out % 10 == 0 and inp == 900:
        print("** output", out, "p/r/t", pattern_value, result, total)
      total += result
    output_list.append(abs(total) % 10)
  if i == 100:
    o = "".join([str(x) for x in output_list])
    print("from zero", o[0:10])
    print("from", to_skip, o[to_skip:to_skip + 8])
    break

# 53296082
