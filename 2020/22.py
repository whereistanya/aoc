#!/usr/bin/env python


lines = [
  "Player 1:",
  "9",
  "2",
  "6",
  "3",
  "1",
  "",
  "Player 2:",
  "5",
  "8",
  "4",
  "7",
  "10",
]

inputfile = "input22.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

hands = []
hand = None
for line in lines:
  if line == "":
    continue
  if line.startswith("Player"):
    if hand is not None:
      hands.append(hand)
    hand = []
    continue
  hand.append(int(line))
hands.append(hand)
hand1 = hands[0]
hand2 = hands[1]
handsize = len(hands[0])

print ("HAND1: %s" % hand1)
print ("HAND2: %s" % hand2)

index = 0
winning_hand = []
while True:
  if index >= len(hand1):
    print("Player 2 wins")
    winning_hand = hand2[index:]
    break
  if index >= len(hand2):
    print("Player 1 wins")
    winning_hand = hand1[index:]
    break

  if hand1[index] > hand2[index]:
    hand1.extend([ hand1[index], hand2[index] ])
  elif hand2[index] > hand1[index]:
    hand2.extend([ hand2[index], hand1[index] ])
  else:
    print("ERROR: unexpected draw")
    exit()
  index += 1

product = 0
i = 1
print winning_hand
for card in winning_hand[::-1]:
  product += (card * i)
  print ("%d * %d" % (card, i))
  i += 1
print ("Part 1: %d" % product)

# Part 2

def play_game(hand1, hand2, game=1):
  seen = set()  # Player1_Player2
  index = 0
  game_round = 0

  while(True):
    if len(hand1[index:]) == 0:
      print("The winner of game %d is player 2" % game)
      return 2, hand2[index:]
    if len(hand2[index:]) == 0:
      print("The winner of game %d is player 1" % game)
      return 1, hand1[index:]

    # print
    print ("Round %d (Game %d)" % (game_round, game))
    # If there was a previous round with exactly the same cards, player 1 wins
    hs1 = ','.join([str(x) for x in hand1[index:]])
    hs2 = ','.join([str(x) for x in hand2[index:]])
    #print ("Player1's deck: %s" % hs1)
    #print ("Player2's deck: %s" % hs2)

    save = "%s_%s" % (hs1, hs2)

    if save in seen:
      #print "We're looping! Player 1 wins!"
      return 1, hand1[index:]
    seen.add(save)

    winner = None  # we don't know yet!
    #print ("Player 1 plays %s" % hand1[index])
    #print ("Player 2 plays %s" % hand2[index])

    # If any player doesn't haveenough cards to recuse, the winner is the player
    # with the higher value card.
    if ((hand1[index] >= len(hand1[index:])) or (hand2[index] >= len(hand2[index:]))):
      #print "Not enough cards to recurse!"
      if hand1[index] > hand2[index]:
        winner = 1
      else:
        winner = 2
    else:
      # Otherwise, play a sub-game.
      #print("\nWe must go deeper!")
      subhand1 = list(hand1[index + 1:index + 1 + hand1[index]])
      subhand2 = list(hand2[index + 1 :index + 1 + hand2[index]])
      #print "Recursing with %s, %s" % (subhand1, subhand2)
      winner, _unused_hand = play_game(subhand1, subhand2, game + 1)

    print ("Player %d wins round %d of game %d!" % (winner, i, game))
    if winner == 1:
      hand1.extend([ hand1[index], hand2[index] ])
    elif winner == 2:
      hand2.extend([ hand2[index], hand1[index] ])
    else:
      print("ERROR: unexpected draw")
      exit()
    index += 1
    game_round += 1

print ( "PART 2")

# Reset hands
hand1 = list(hand1[:handsize])
hand2 = list(hand2[:handsize])

winner, winning_hand = play_game(hand1, hand2, game=1)
i = 1
product = 0
print winning_hand
for card in winning_hand[::-1]:
  product += (card * i)
  print ("%d * %d" % (card, i))
  i += 1
print ("Part 2: %d" % product)
