#!/usr/bin/env python3
# Advent of code Day 2

#with open("test2.txt", "r") as f:
with open("input2.txt", "r") as f:
  lines = f.readlines()

beats = {
  "rock": "scissors",
  "scissors": "paper",
  "paper": "rock",
}

# invert the map
loses_to = {v: k for k, v in beats.items()}

translate = {
  "X": "rock",
  "Y": "paper",
  "Z": "scissors",
  "A": "rock",
  "B": "paper",
  "C": "scissors",
}

scores = {
  "rock": 1,
  "paper": 2,
  "scissors": 3,
  "win": 6,
  "lose": 0,
  "draw": 3,
}


us_score = 0
them_score = 0

# Part 1
us_score = 0
them_score = 0

for line in [x.strip() for x in lines]:
  them, us = [translate[x] for x in line.split()]

  us_score += scores[us]
  them_score += scores[them]
  if us == them:
    us_score += scores["draw"]
    them_score += scores["draw"]
  elif beats[us] == them:
    us_score += scores["win"]
  elif beats[them] == us:
    them_score += scores["win"]
  else:
    print("BUG: %s, %s, %s" % (us, them, beats[us]))
    exit(1)

print("Part 1")
print("My score:", us_score)
print("Their score:", them_score)

# Part 2
us_score = 0
them_score = 0

for line in [x.strip() for x in lines]:
  them, plan = line.split()
  them = translate[them]
  if plan == "X": # need to lose
    us = beats[them]
  elif plan == "Y": # need to draw
    us = them
  elif plan == "Z": # need to win
    us = loses_to[them]
  else:
    print("BUG: %s, %s" % (plan, them))
    exit(1)

  us_score += scores[us]
  them_score += scores[them]
  if us == them:
    us_score += scores["draw"]
    them_score += scores["draw"]
  elif beats[us] == them:
    us_score += scores["win"]
  elif beats[them] == us:
    them_score += scores["win"]
  else:
    print("BUG: %s, %s, %s" % (us, them, beats[us]))
    exit(1)

print("Part 1")
print("My score:", us_score)
print("Their score:", them_score)
