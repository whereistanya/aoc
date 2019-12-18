#!/usr/bin/python

import math
import sys
import time


base = [0, 1, 0, -1]

  #             0  1  2   3  4  5  6   7
  # pattern is [0, 1, 0, -1, 0, 1, 0, -1]
  #o=1: pattern is 0 1 0 -1 0 1 0 -1, shifted 1
    # i=1 : 1 pattern[1] i]
    # i=2 : 0 pattern[2] i]
    # i=3: -1 pattern[3] i]
  #o=2: pattern is 0 0 1 1 0 0 -1 -1 0 0 1 1 ...
    # i=1: 0 pattern[0] i
    # i=2: 1 pattern[1] i - 1
    # i=3: 1 pattern[1] i - 2
    # i=4: 0 pattern[2] i - 2
    # i=5: 0 pattern[2] i - 3
    # i=6: -1 pattern[3] i - 3
    # i=7: -1 pattern[3] i - 4
  #o=3: pattern is 0 0 0 1 1 1 0 0 0 -1 -1 -1 0 0 0...
    # i=1:0 0 pattern[0] i
    # i=2:0 0 pattern[0] i - 1
    # i=3:0 1 pattern[1] i - 1
    # i=4:1 1 pattern[1] i - 2
    # i=5:1 1 pattern[1] i - 3
    # i=6:1 0 pattern[2] i - 3
    # i=7:0 0 pattern[2] i - 4

    # i < 0 behaves like i=0 (unless o=0)
    # actual n is expected n + 1 (because of the shift)
    # and expected is moduluses?

patterns = {}

def value(i, o):
  try:
    pattern = patterns[o]
  except KeyError:
    pattern = []
    for b in base:
      pattern.extend([base[b]] * (o))
    patterns[o] = pattern
  ret = pattern[i % len(pattern)]
  assert ret == base[int(i * 1.0 / o)]
  return ret

# phase.
# input: 5 digit list, [9, 8, 7, 6, 5]
# output: 5 digit list
#s = "69317163492948606335995924319873"
s = "59777373021222668798567802133413782890274127408951008331683345339720122013163879481781852674593848286028433137581106040070180511336025315315369547131580038526194150218831127263644386363628622199185841104247623145887820143701071873153011065972442452025467973447978624444986367369085768018787980626750934504101482547056919570684842729787289242525006400060674651940042434098846610282467529145541099887483212980780487291529289272553959088376601234595002785156490486989001949079476624795253075315137318482050376680864528864825100553140541159684922903401852101186028076448661695003394491692419964366860565639600430440581147085634507417621986668549233797848"
output_list = [int(x) for x in s]
#print output_list


print value(0, 2)
print value(1, 2)
print value(2, 2)
print value(3, 2)
print value(4, 2)
print value(5, 2)
#The first o get base[0]
#The next o get base[1]
print base[int(0/2.0)]
print base[int(1/2.0)]
print base[int(2/2.0)]
print base[int(3/2.0)]
print base[int(4/2.0)]
print base[int(5/2.0)]
print "---------"
print value(0, 3)
print value(1, 3)
print value(2, 3)
print value(3, 3)
print value(4, 3)
print value(5, 3)
print "---------"
print value(0, 4)
print value(1, 4)
print value(2, 4)
print value(3, 4)
print value(4, 4)
print value(5, 4)
print "---------"

#sys.exit(0)
#output_list = [1, 2, 3, 4, 5, 6, 7, 8]
i = 0
while True:
  i += 1
  array = output_list
  output_list = []
  for out in range(1, len(array) + 1): # each element of output list
    total = 0
    for inp in range(0, len(array)):   # input list
      pattern_value = value(inp + 1, out)
      result = array[inp] * pattern_value
      total += result
    output_list.append(abs(total) % 10)
  if i == 100:
    print s
    o = "".join([str(x) for x in output_list])

    print
    print
    dupes = ""
    for i in range(0, len(output_list)):
      if s[i] == o[i]:
        dupes += s[i]
      else:
        dupes += "_"
    print dupes
    break

# 53296082
