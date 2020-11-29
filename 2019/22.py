#!/usr/bin/env python
# Advent of code Day 22.

# I only tenuously understand any of this. I hated this puzzle.
import sys

########## Unused functions from early versions of this puzzle  ##########
def cut(n, deck):
  # This function is not used in the final version; it's superseded by the
  # fast shuffle. Left here for historical reasons.
  if n == 0: # Can't handle zero input.
    raise ValueError
  p1 = deck[n:]
  p1.extend(deck[0:n])
  return p1

def incr(n, deck):
  # This function is not used in the final version; it's superseded by the
  # fast shuffle. Left here for historical reasons.
  tmp = [0] * len(deck)
  for i in range(len(deck)):
    tmp[(i * n) % len(deck)] = deck[i]
  return tmp

def slow_shuffle(lines, deck):
  # Not actually used now, but leaving here as an explanation for future-me.
  # Part1 of this puzzle used the "Approach 1" approaches listed here. The
  # "Approach 2" approaches were educational steps on the path to understanding
  # the fast shuffle. Approach 3 became the fast way now used in fast_shuffle().
  # All three of these functions can be munged into two magic constants, a and
  # b, which fit the function "card x moves to position (ax + b) % m.
  # m: number of cards in the deck
  # x: position of any given card
  # n: what we're cutting or incrementing by
  #print "\n## Shuffling", len(deck)
  tmp = [0] * len(deck)
  m = len(deck)
  for line in lines:
    line.strip()
    if line == "deal into new stack":
      # moves cards from position x to position m - x - 1
      # Approach 1: just reverse the deck.
      # deck.reverse()
      # Approach 2: fancy modular arithmetic way.
      # Card x moves to position m - x - 1.
      # for x in range(m):
      #  tmp[m - x - 1] = deck[x]
      # deck = list(tmp)
      # Approach 3: even fancier linear congruential function way
      a = -1
      b = -1
      for x in range(m):
        tmp[(a * x + b) % m] = deck[x]
      deck = list(tmp)

    if line.startswith("deal with increment"):
      # moves cards from position x to position n * x mod m
      n = int(line.strip("deal with increment "))
      # Approach 1: use the incr function.
      # deck = incr(n, deck)
      # Approach 2: fancy modular arithmetic way
      # Card x moves to position n * x % m.
      # for x in range(m):
      #   tmp[n * x % m] = deck[x]
      # deck = list(tmp)
      # Approach 3: even fancier linear congruential function way
      a = n
      b = 0
      for x in range(m):
        tmp[(a * x + b) % m] = deck[x]
      deck = list(tmp)

    if line.startswith("cut"):
      # moves cards from position x to position x - n mod m
      n = int(line.strip("cut "))
      # Approach 1: use the cut function.
      # deck = cut(n, deck)
      # Approach 2: fancy modular arithmetic way
      # Card x moves to position x - n % m.
      # for x in range(m):
      #   tmp[(x - n) % m] = deck[x]
      # deck = list(tmp)
      # Approach 3: even fancier linear congruential function way
      a = 1
      b = -n
      for x in range(m):
        tmp[(a * x + b) % m] = deck[x]
      deck = list(tmp)

  return deck

def fast_shuffle(deck, a, b, m):
  # Do the shuffle which is represented by the lines of input. By generating the
  # magic constants a and b (see above), we can shortcut actually moving all of
  # the stuff around for each line, and just say where each card in the original
  # deck will have moved to by the end. m is the number of cards in the deck.
  # (fast_shuffle() is also not used any more! It was another step along the
  # learning path to understanding how to find the position of a given card
  # after a number of shuffles, without actually doing all the shuffles.
  tmp = [0] * len(deck)
  for x in range(m):
    tmp[(a * x + b) % m] = deck[x]
  return tmp


######### Code below here is actually used #########

def generate_magic_constants(lines, m):
  # Read the lines of input and generate constants, a and b, that can
  # be plugged into functions to make this fast. It's using the idea
  # of linear congruent functions, which are like:
  # F(x) = ax + b. Each deal, cut and increment is a linear congruent
  # function with its own a and b constants.
  # deal into new deck =>  m - x - 1  (a is -1, b is -1)
  # increment n        =>  n * x % m  (a us n,  b is 0)
  # cut n              =>  x - n % m  (a is 1,  b is -n)
  # So that's cool enough, but you can also stack them up, (e.g., cut then
  # deal then cut then increment, or whatever), and compress it all into one
  # a and b to rule them all, which will do all of these functions at once.
  # Amazing. So this function reads all of the lines of input one at a time
  # and returns those.
  finala = 1 # a is about multiplying so 1 is a no-op starting point
  finalb = 0 # b is about adding so 0 is a no-op starting point
  for line in lines:
    line.strip()
    if line == "deal into new stack":
      a = -1
      b = -1
    if line.startswith("deal with increment"):
      n = int(line.strip("deal with increment "))
      a = n
      b = 0
    if line.startswith("cut"):
      n = int(line.strip("cut "))
      a = 1
      b = -n

    # if our two functions are
    #    f(x) = ax + b %m and
    #    g(x) = cx + d %m
    # then we can do both at once with:
    # g(f(x)) = c(ax+b)+d % m
    # So as we run through every line in the file, we're munging it together
    # with the result of the previous functions, and making a new
    # "something x + something" function.
    finala = finala * a % m
    finalb = finalb * a + b % m
  print("The Linear Congruential Function for this shuffle is")
  print("%dx + %d mod %d" % (finala, finalb, m))
  return finala, finalb

def power_mod(x, n, m):
  # Return x^n mod m. For small numbers this is equivalent to pow(x, n) % m.
  # However we're talking about numbers here like pow(2284, 119315717514047),
  # which becomes epically, ridiculously big before you mod it back down, so
  # we need a way of getting the answer which won't overflow all the buffers.
  # This uses exponentiation by squaring, using pseudocode from
  # https://codeforces.com/blog/entry/72527.
  if n == 0:
    return 1
  y = 1
  while n > 1:
    if n % 2 == 0:
      x = x * x % m
      n = n / 2
    else:
      y = x * y % m
      x = x * x % m
      n = (n - 1) / 2
  return x * y % m

def mod_inverse(a, m):
  # The modular multiplicative inverse of a number, a, is the number a^-1 such
  # that a * a^-1 mod m = 1. Is that the same as 1/a % m? I think so?
  # It has to be between 0 and m-1 anyway.
  # There are two ways to generate the modular multiplicative inverse. The other
  # way is to use the extended GCD algorithm. This way is using the adorably
  # named "Fermat's Little Theorem" which says so long as m is prime,
  # a^m mod m = a mod m. And, therefore clearly (i.e., I don't understand why
  # but I'll take other people's word for it), the thing we need is
  # a^(m - 2) mod m. We're using power_mod here because the numbers are too big
  # for python's built in pow().
  return power_mod(a, m - 2, m)

def x_after_k_shuffles(x, a, b, k, m):
  # Ok! So we want to shuffle lots of times, like trillions of times, but it
  # would take too long to run a shuffle() function all those times. But if you
  # want to run this function a lot of times, it forms a geometric series which
  # can be transformed into:
  # F^k(x) = ak^k + b((1 - a^k) / (1 - a)) mod m
  # x:position, k:how many shuffles, m:deck size, a and b: magic constants
  # In modular arithmetic land, if you want to divide by foo, you actually
  # multiple by the modular inverse of foo.
  # So, run this function and return where x will be after k shuffles.
  a_to_the_k = power_mod(a, k, m)
  mod_inv = mod_inverse(1 - a, m)
  new_x = (b * (1 - a_to_the_k)) * mod_inv
  new_x += (a_to_the_k * x)
  new_x %= m
  return new_x


# Main

with open("input22.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]

######### Part 1 #########

len_deck = 10007
how_many_shuffles = 1

# Magic constants that let us shuffle efficiently. Using the method
# described at https://codeforces.com/blog/entry/72593. If we plug these into
# `ax + b mod m`, we get the new position of x.
a, b = generate_magic_constants(lines, len_deck)
print("Part 1 a,b are", a, b)

# Create a deck
deck = []
for i in range(0, len_deck):
  deck.append(i)

# Shuffling lots of times takes too long. For part 1, we only need to
# shuffle once, but we use the super fancy function that can shuffle lots of
# times just to convince ourselves it works.
tmp = [0] * len_deck
for x in range(len_deck):
  y = x_after_k_shuffles(x, a, b, how_many_shuffles, len_deck)
  tmp[y] = deck[x]
deck = tmp
print("Part 1: 2019 is at index", deck.index(2019))

######### Part 2 #########

len_deck = 119315717514047
how_many_shuffles = 101741582076661

# Find the magic constants for this bigger deck.
a, b = generate_magic_constants(lines, len_deck)
print("Part 2 a,b are", a, b)

# We're not making a deck this time. Too big! Instead, we want to just find out
# what will be in that one position, 2020.
# Previously we were asking "where will the card at position 2019 end up?".
# Now we're asking "what card will end up at position 2020?". So not "where will
# it go?" but "where will it come from?".
# According to https://codeforces.com/blog/entry/72593, this means
# we need to invert our magic function. One way to do that is to run the same
# x_after_k_shuffles() function, but change a and b:
# a becomes 1/a         (which is mod inverse a!)
# and b becomes -b / a  (which is -b * mod inverse a!)
# ...I don't know why these are the right a and b. If anyone is reading this and
# thought I knew what was happening here, haha nope.

inverted_a = mod_inverse(a, len_deck)
inverted_b = -b * inverted_a
card_position = 2020

y = x_after_k_shuffles(2020, inverted_a, inverted_b, how_many_shuffles, len_deck)
print("Part 2: the card at position 2020 will come from position", y)

"""
## Tests
assert cut(1, [45,67,89]) == [67, 89, 45]
assert cut(-3, [100,50,25,12,6,3,1]) == [6,3,1,100,50,25,12]
assert(incr(3, [0,1,2,3,4,5,6,7,8,9])) == [0,7,4,1,8,5,2,9,6,3]
assert(incr(7, [0,1,2,3,4,5,6,7,8,9])) == [0,3,6,9,2,5,8,1,4,7]

deck = []
for i in range(0, 10):
  deck.append(i)
assert shuffle([
  "deal with increment 7",
  "deal into new stack",
  "deal into new stack",
], deck) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]

deck = []
for i in range(0, 10):
  deck.append(i)
assert shuffle([
"cut 6",
"deal with increment 7",
"deal into new stack",
], deck) == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]

deck = []
for i in range(0, 10):
  deck.append(i)
assert shuffle([
"deal into new stack",
"cut -2",
"deal with increment 7",
"cut 8",
"cut -4",
"deal with increment 7",
"cut 3",
"deal with increment 9",
"deal with increment 3",
"cut -1",
], deck) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

deck = []
for i in range(0, 10):
  deck.append(i)
assert shuffle([
"deal with increment 7",
"deal with increment 9",
"cut -2",
], deck) == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]

"""

