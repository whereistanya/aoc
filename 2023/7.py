#!/usr/bin/env python3

VERBOSE = False
TEST = False

with open("input7.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]

example = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

example = """
2345A 1
Q2KJJ 13
Q2Q2Q 19
T3T3J 17
T3Q33 11
2345J 3
J345A 2
32T3K 5
T55J5 29
KK677 7
KTJJT 34
QQQJA 31
JJJJJ 37
JAAAA 43
AAAAJ 59
AAAAA 61
2AAAA 23
2JJJJ 53
JJJJ2 41"""

if TEST:
  lines = [x.strip() for x in example.strip().split("\n")]


def value(card, part=1):
  if card.isdigit():
    return int(card)
  if card == 'T':
    return 10
  if card == 'J':
    if part == 2:
      return 1
    else:
      return 11
  if card == 'Q':
    return 12
  if card == 'K':
    return 13
  if card == 'A':
    return 14

def handscore(handstr, part=1):
  hand = list(handstr)
  place_value = [100000000, 1000000, 10000, 100, 1]
  score = 0
  for i in range(len(hand)):
    score += value(hand[i], part=part) * place_value[i]
  return score


def basescore(handstr):
  hand = list(handstr)
  base_score = {
    "five_of_a_kind": 10,
    "four_of_a_kind":  9,
    "full_house":      8,
    "three_of_a_kind": 7,
    "two_pair":        6,
    "one_pair":        5,
    "high_card":       0,
  }

  cardcount = {}
  for card in hand:
    try:
      cardcount[card] += 1
    except KeyError:
      cardcount[card] = 1

  handtype = "not set"
  if len(cardcount) == 1:
    # Five of a kind, where all five cards have the same label: AAAAA
    handtype = "five_of_a_kind"
  elif 4 in cardcount.values():
    # Four of a kind, where four cards have the same label and one card has a
    # different label: AA8AA
    handtype = "four_of_a_kind"
  elif len(cardcount) == 2:
    # Full house, where three cards have the same label, and the remaining two
    # cards share a different label: 23332
    assert(2 in cardcount.values())
    assert(3 in cardcount.values())
    handtype = "full_house"
  elif 3 in cardcount.values():
    # Three of a kind, where three cards have the same label, and the
    # remaining two cards are each different from any other card in the hand: TTT98
    assert len(cardcount) == 3
    handtype = "three_of_a_kind"
  elif len(cardcount) == 3:
    # Two pair, where two cards share one label, two other cards share a second
    # label, and the remaining card has a third label: 23432
    assert 2 in cardcount.values()
    assert 1 in cardcount.values()
    handtype = "two_pair"
  elif len(cardcount) == 4:
    # One pair, where two cards share one label, and the other three cards
    # have a different label from the pair and each other: A23A4
    assert 2 in cardcount.values()
    assert 1 in cardcount.values()
    handtype = "one_pair"
  else:
    # High card, where all cards' labels are distinct: 23456
    assert len(cardcount) == 5
    handtype = "high_card"

  if VERBOSE: print(handstr, handtype)
  return base_score[handtype]

def basescore_part2(handstr):
  hand = list(handstr.replace("J", ""))
  base_score = {
    "five_of_a_kind": 10,
    "four_of_a_kind":  9,
    "full_house":      8,
    "three_of_a_kind": 7,
    "two_pair":        6,
    "one_pair":        5,
    "high_card":       0,
  }

  handsize = len(hand)
  cardcount = {}
  for card in hand:
    try:
      cardcount[card] += 1
    except KeyError:
      cardcount[card] = 1

  handtype = "not set"
  if len(cardcount) <= 1:
    # Five of a kind, where all five cards have the same label: AAAAA
    handtype = "five_of_a_kind"
  elif (handsize - 1) in cardcount.values():
    # Four of a kind, where four cards have the same label and one card has a
    # different label: AA8AA
    handtype = "four_of_a_kind"
  elif len(cardcount) == 2:
    # Full house, where three cards have the same label, and the remaining two
    # cards share a different label: 23332
    #assert(2 in cardcount.values())
    #assert(3 in cardcount.values())
    handtype = "full_house"
  elif (handsize - 2) in cardcount.values():
    # Three of a kind, where three cards have the same label, and the
    # remaining two cards are each different from any other card in the hand: TTT98
    #assert len(cardcount) == 3
    handtype = "three_of_a_kind"
  elif len(cardcount) == 3:
    # Two pair, where two cards share one label, two other cards share a second
    # label, and the remaining card has a third label: 23432
    #assert 2 in cardcount.values()
    #assert 1 in cardcount.values()
    handtype = "two_pair"
  elif len(cardcount) == 4:
    # One pair, where two cards share one label, and the other three cards
    # have a different label from the pair and each other: A23A4
    #assert 2 in cardcount.values()
    #assert 1 in cardcount.values()
    handtype = "one_pair"
  else:
    # High card, where all cards' labels are distinct: 23456
    #assert len(cardcount) == 5
    handtype = "high_card"

  if VERBOSE: print(handstr, handtype)
  return base_score[handtype]


def score(hand, part=1):
  if part == 1:
    total = (10000000000 * basescore(hand)) + handscore(hand)
  else:
    # Sanity checking to (fail to) find my bug...
    score_for_1 = basescore(hand)
    score_for_2 = basescore_part2(hand)
    assert(score_for_2 >= score_for_1)
    if "J" in hand and hand != "JJJJJ":
      if score_for_1 >= score_for_2:
        print(hand, "unexpected")
      assert score_for_1 < score_for_2
    total = (10000000000 * basescore_part2(hand)) + handscore(hand, part=2)
  if VERBOSE: print(hand, total)
  return total


scores = {}
bids = {}

for line in lines:
  hand, bid = line.split()
  scores[hand] = score(hand, part=2)
  bids[hand] = int(bid)

total = 0
sorted_hands = sorted(scores, key=scores.get)
for i in range (len(sorted_hands)):
  hand = sorted_hands[i]
  bid = bids[hand]
  if VERBOSE: print(hand, scores[hand], bid)
  total += (i + 1) * bid

print(total)

# 252610187 too high
# 252283830 too high
