#!/usr/bin/env python3


def LookSay(start):
  outs = ""
  count = 1
  current = start[0]
  for i in range (1, len(start)):
    if start[i] == current:
      count += 1
    else:
      outs += "%d%s" % (count, current)
      current = start[i]
      count = 1
  outs += "%d%s" % (count, current)
  return outs


start = "1113122113"
for i in range (50):
  start = LookSay(start)
   # print(start)
  print("After %d:  %d" % (i + 1, len(start)))
