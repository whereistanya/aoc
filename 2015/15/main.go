package main

import (
 "fmt"
 "log"
 "os"
 "strings"

 . "github.com/whereistanya/aoc2015/util"
)

type Ingredient struct {
  name string
  capacity, durability, flavor, texture, calories int
}

func NewIngredient(line string) (*Ingredient, error) {
  var name string
  var cp, d, f, t, cl int
  _, err := fmt.Sscanf(line, "%s capacity %d, durability %d, flavor %d, texture %d, calories %d", &name, &cp, &d, &f, &t, &cl)
  if err != nil {
    return nil, err
  }

  // I dunno how to make Sscanf not consider the : part of the name
  // and I'm too lazy to break out a regex.
  name = strings.TrimSuffix(name, ":")

  return &Ingredient {
    name: name,
    capacity: cp,
    durability: d,
    flavor: f,
    texture: t,
    calories: cl,
  }, nil
}

func score(ingredients map[*Ingredient]int) int {
  capacity := 0
  durability := 0
  flavor := 0
  texture := 0
  calories := 0

  for ingredient, quantity := range ingredients {
    capacity += quantity * ingredient.capacity
    durability += quantity * ingredient.durability
    flavor += quantity * ingredient.flavor
    texture += quantity * ingredient.texture
    calories += quantity * ingredient.calories
  }

  if capacity <= 0 || durability <= 0 || flavor <= 0 || texture <= 0 {
    return 0
  }
  score := capacity * durability * flavor * texture
  return score
}


type fn func(map[*Ingredient]int) bool
// Finding quantities
// if any of the qualities are <= 0, the score will be zero
// so each quality needs to be > 0 or prune
func BestRecipeScore(list []*Ingredient, recipe map[*Ingredient]int,
                  validator fn) int {
  // divide 100 units between a, b, c, d
  var a, b, c, d int

  highScore := 0

  for a = 1; a < 100; a++ {
    for b = 1; b < (100 - a); b++ {
      for c = 1; c < (100 - (a + b)); c++ {
        d = 100 - (a + b + c)

        recipe[list[0]] = a
        recipe[list[1]] = b
        recipe[list[2]] = c
        recipe[list[3]] = d
        if !validator(recipe) {
          continue
        }
        val := score(recipe)
        if val > highScore {
          highScore = val
        }
      }
    }
  }
  return highScore
}

func main() {

  var filename string
  if len(os.Args) > 1 {
    filename = os.Args[1]
  } else {
    filename = "input.txt"
  }

  lines, err := ReadToStringSlice(filename)
  if err != nil {
    log.Fatal(err)
  }

  ingredients := map[string]*Ingredient{}
  recipe := map[*Ingredient]int{}
  // ingredient keys, so we don't need to keep parsing them
  // inside the loop. Probably there's a better way to do this.
  list := []*Ingredient{}

  for _, line := range lines {
    ingredient, err := NewIngredient(line)
    if err != nil {
      panic(err)
    }
    ingredients[ingredient.name] = ingredient
    list = append(list, ingredient)
    recipe[ingredient] = 0
  }

  part1Validator := func(x map[*Ingredient]int) bool {return true}
  part2Validator := func(x map[*Ingredient]int) bool {
    cals := 0
    for i, q := range x {
      cals += q * i.calories
    }
    if cals == 500 {
      return true
    }
    return false
  }

  fmt.Println("Part1", BestRecipeScore(list, recipe, part1Validator))
  fmt.Println("Part2", BestRecipeScore(list, recipe, part2Validator))
}


