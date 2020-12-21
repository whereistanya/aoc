#!/usr/bin/env python

inputfile = "input21.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

ingredient_lists = {} # str: [str, str, str], [str, str, str], ...
definites = {}
all_ingredients = set()
recipes = []

for line in lines:
  ingredients, allergens = map(lambda x: x.split(" "), line.strip().strip(")").strip().split(" (contains "))
  recipes.append(ingredients)

  for ingredient in ingredients:
    all_ingredients.add(ingredient)

  for allergen in map(lambda x: x.strip(","), allergens):
    try:
      ingredient_lists[allergen].append(set(ingredients))
    except KeyError:
      ingredient_lists[allergen] = [set(ingredients)]

possibles = {} # str: [str,  str]
actuals = {}
seen = set()

for k in ingredient_lists.keys():
  v = ingredient_lists[k]
  possibles[k] = v[0].intersection(*v)

while True:
  if len(possibles) == 0:
    break

  newPossibles = {}
  for k, v in possibles.iteritems():
    print k, v
    if len(v) == 1:
      actuals[k] = v.pop()
      seen.add(actuals[k])
    else:
      newPossibles[k] = []
      for item in v:
        if item not in seen:
          newPossibles[k].append(item)
  possibles = newPossibles

unused = all_ingredients - set(actuals.values())

count = 0

for i in unused:
  for v in recipes:
    if i in v:
      count += 1

print("Part 1: %d" % count)
print("Part 2: %s" % ",".join([actuals[x] for x in sorted(actuals.keys())]))
