#!/usr/bin/env python3

from collections import defaultdict
import functools

p1 = 10
p2 = 9

# override to test
#p1 = 4
#p2 = 8

score1 = 0
score2 = 0
total = 0

i = 1
rolls = 0
while True:
	roll1 = (i *3) + 3
	p1 = (p1 + roll1) % 10
	if p1 == 0:
		p1 = 10
	score1 += p1
	rolls += 3

	if score1 >= 1000:
		total = score2 * rolls
		break
	i += 3
	roll2 = (i * 3) + 3
	p2 = (p2 + roll2) % 10
	if p2 == 0:
		p2 = 10
	score2 += p2
	rolls += 3
	if score2 >= 1000:
		total = score1 * rolls
		break
	i += 3

print("Part 1", total)

"""
a quantum die: when you roll it, the universe splits into multiple copies, one
copy for each possible outcome of the die. In this case, rolling the die
always splits the universe into three copies: one where the outcome of the roll
was 1, one where it was 2, and one where it was 3.

The game is played the same as before, although to prevent things from getting
too far out of hand, the game now ends when either player's score reaches at
least 21.

Using the same starting positions as in the example above, player 1 wins in
444356092776315 universes, while player 2 merely wins in 341960390180808 universes.

Using your given starting positions, determine every possible outcome. Find the
player that wins in more universes; in how many universes does that player win?
"""

rolls = [
  (1, 1, 1),
  (1, 1, 2),
  (1, 1, 3),
  (1, 2, 1),
  (1, 2, 2),
  (1, 2, 3),
  (1, 3, 1),
  (1, 3, 2),
  (1, 3, 3),

  (2, 1, 1),
  (2, 1, 2),
  (2, 1, 3),
  (2, 2, 1),
  (2, 2, 2),
  (2, 2, 3),
  (2, 3, 1),
  (2, 3, 2),
  (2, 3, 3),

  (3, 1, 1),
  (3, 1, 2),
  (3, 1, 3),
  (3, 2, 1),
  (3, 2, 2),
  (3, 2, 3),
  (3, 3, 1),
  (3, 3, 2),
  (3, 3, 3),
]

rollcount = defaultdict(int)
for roll in rolls:
  rollcount[sum(roll)] += 1

@functools.lru_cache(maxsize=None)
def roll(p1pos, p2pos, p1score, p2score):
  if p1score >= 21:
    return (1, 0)
  if p2score >= 21:
    return (0, 1)

  p1_wins_from_here = 0
  p2_wins_from_here = 0

  for number, count in rollcount.items():
    new_p1pos = (p1pos + number) % 10
    if new_p1pos == 0:
      new_p1pos = 10
    new_p1score = p1score + new_p1pos

    # invert player order
    p2_later_wins, p1_later_wins = roll(p2pos, new_p1pos, p2score, new_p1score)
    p1_wins_from_here += (p1_later_wins * count)
    p2_wins_from_here += (p2_later_wins * count)

  return (p1_wins_from_here, p2_wins_from_here)

p1 = 10
p2 = 9

print("Part 2", roll(p1, p2, 0, 0)[0])
