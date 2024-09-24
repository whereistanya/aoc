package main

import (
 "fmt"
 "log"
// "math"
 "os"

 . "github.com/whereistanya/aoc2015/util"
)

type City struct {
  dists map[string]int
}

func (c City) Distances() map[string]int {
  return c.dists
}

func (c *City) AddDistance(name string, distance int) {
  c.dists[name] = distance
}

type Grid struct {
  cities map[string]*City
}
func NewGrid() *Grid {
  return &Grid {
    cities: map[string]*City{},
  }
}

func (g *Grid) FindOrAddCity(name string) *City {
  city, found := g.cities[name]
  if !found {
    city = &City{
      dists: map[string]int{},
    }
    g.cities[name] = city
  }
  return city
}

func (g Grid) PossibleFromHere(current string) map[string]int {
  city, found := g.cities[current]
  if !found {
    fmt.Printf("Didn't find %s in %v\n", current, g.cities)
    log.Fatal("Unexpected data error")
  }
  return city.Distances()
}

func (g Grid) CitySet() map[string]bool {
  set := map[string]bool {}
  for c := range g.cities {
    set[c] = true
  }
  return set
}

func FindShortest(grid *Grid, current string, toFind map[string]bool, costSoFar int) int {
  //fmt.Printf("FindShortest(grid, %s, %v, %d)\n", current, toFind, costSoFar)
  delete(toFind, current)
  if len(toFind) == 0 {
    toFind[current] = true
    return costSoFar
  }

  possibleFromHere := grid.PossibleFromHere(current)
  shortestFromHere  := 999999999999 // until I get syntax for infinity
  //pathFromHere := []string
  for city, dist := range possibleFromHere {
    _, ok := toFind[city]
    if ok {
      cost := FindShortest(grid, city, toFind, costSoFar + dist)
      if cost < shortestFromHere {
        shortestFromHere = cost
      }
    }
  }
  toFind[current] = true
  return shortestFromHere
}

func FindLongest(grid *Grid, current string, toFind map[string]bool, costSoFar int) int {
  delete(toFind, current)
  if len(toFind) == 0 {
    toFind[current] = true
    return costSoFar
  }

  possibleFromHere := grid.PossibleFromHere(current)
  longestFromHere  := 0
  for city, dist := range possibleFromHere {
    _, ok := toFind[city]
    if ok {
      cost := FindLongest(grid, city, toFind, costSoFar + dist)
      if cost > longestFromHere {
        longestFromHere = cost
      }
    }
  }
  toFind[current] = true
  return longestFromHere
}



// must visit each location exactly once
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
  grid := NewGrid()

  for _, line := range lines {
    var from, to string
    var distance int
    found, err := fmt.Sscanf(line, "%s to %s = %d", &from, &to, &distance)
    if err != nil {
      log.Fatal(err)
    }
    if found == 0 {
      log.Fatal(line, found)
    }
    fromCity := grid.FindOrAddCity(from)
    toCity := grid.FindOrAddCity(to)
    fromCity.AddDistance(to, distance)
    toCity.AddDistance(from, distance)
  }

  fmt.Println("***** Finding shortest path *****")
  for starting_point, _ := range grid.cities {
    to_find := grid.CitySet()
    fmt.Printf("From %s: %d\n", starting_point, FindShortest(grid, starting_point, to_find, 0))
  }

  fmt.Println()
  fmt.Println("***** Finding longest path *****")
  for starting_point, _ := range grid.cities {
    to_find := grid.CitySet()
    fmt.Printf("From %s: %d\n", starting_point, FindLongest(grid, starting_point, to_find, 0))
  }
}


