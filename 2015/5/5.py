#!/usr/bin/env python3
# Code by Ms 11 (not finished yet)

def is_nice(s):
  if s == "":
    return False

  # contains at least one letter that appears twice in a row
  found_duplicate = False
  position = 0
  old_letter = s[0]
  for c in s:
    if position > 0:
      new_letter = s[position]
      if new_letter == old_letter:
        found_duplicate = True
        #print("I found a duplicate at position", position, "!")
      old_letter = new_letter
    position += 1
  if not found_duplicate:
    return False

  # contains at least three vowels
  vowels = 0
  good_vowels = False
  for c in s:
    if c in ["a", "e", "i", "o", "u"]:
      vowels += 1
      if vowels == 3:
        good_vowels = True
        break
  if not good_vowels:
    return False

  # does not contain ab, cd, pq, or xy.
  baddies = ["ab", "cd", "pq", "xy"]
  for baddy in baddies:
    if baddy in s:
      return False

  return True


# main
with open("input.txt", "r") as f:
  lines = f.readlines()

nice_count = 0
tests = ["ugknbfddgicrmopn", "aaa", "jchzalrnumimnmhp", "haegwjzuvuyypxyu",
         "dvszwmarrgswjxmb"]

for test in tests:
  print(test, is_nice(test))

