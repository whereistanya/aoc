package main

import (
 "fmt"
 "log"
 "os"

 . "github.com/whereistanya/aoc2015/util"
)

  type Point struct {
    x, y int
  }

func updatePosition(location *Point, d rune) {
  // modifies the point passed to it
  if d == '>' {
    (*location).x += 1
  } else if d == '<' {
    (*location).x -= 1
  } else if d == '^' {
    (*location).y += 1
  } else if d == 'v' {
    (*location).y -= 1
  } else {
    log.Fatal("Unexpected direction: %c", d)
  }

}

func main() {

  var filename string
  if len(os.Args) > 1 {
    filename = os.Args[1]
  } else {
    filename = "input.txt"
  }

  directions, err := ReadToRunes(filename)
  if err != nil {
    log.Fatal(err)
  }

  // Part 1
  location := Point{0, 0}
  houses := map[Point]int{location: 1}
  for _, d := range directions {
    updatePosition(&location, d)
    _, ok := houses[location]
    if ok {
      houses[location] += 1
    } else {
      houses[location] = 1
    }
  }
  fmt.Printf("Part 1: %d\n", len(houses))

  // Part 2
  location1 := Point{0, 0}
  location2 := Point{0, 0}
  var toMove *Point
  houses = map[Point]int{location1: 2}
  for i, d := range directions {
    if i % 2 == 0 {
      toMove = &location1
    } else {
      toMove = &location2
    }
    updatePosition(toMove, d)
    _, ok := houses[*toMove]
    if ok {
      houses[*toMove] += 1
    } else {
      houses[*toMove] = 1
    }
  }
  fmt.Printf("Part 2: %d\n", len(houses))
}


