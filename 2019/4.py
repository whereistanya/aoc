#!/usr/bin/python

def has_double(i):
  last = -1
  while i >= 1:
    m = i % 10
    if m == last:
      nexti = i/10
      nextm = nexti % 10
      if nextm != m:
        return True
      while nextm == m and nexti >= 1:
        nexti = nexti/10
        nextm = nexti % 10
      i = nexti
      m = nextm
    last = m
    i /= 10
  return False

def increasing_digits(i):
  last = 11
  while i >= 1:
    m = i % 10
    # Digits are in reverse order, so a bigger number is bad here.
    if m > last:
      return False
    last = m
    i /= 10
  return True

### Test data ###
assert has_double(122)
assert not has_double(456)
assert has_double(123325)
assert not has_double(357832576)
assert not has_double(6)

assert increasing_digits(12348)
assert increasing_digits(111111)
assert not increasing_digits(76543)

assert not has_double(222)
assert not has_double(444222)
assert not has_double(222)
assert has_double(22233)
#################

possible = set()
for i in range (265275, 781585):
  if has_double(i) and increasing_digits(i):
    possible.add(i)

print(len(possible))
