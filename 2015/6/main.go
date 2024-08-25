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

type Grid struct {
  lights map[Point]int
  // track light count to save a count at the end; not worth it really but I
  // added it already so...
  onCount int
  maxX, maxY int
}

func NewGrid(maxX, maxY int) Grid {
  grid := Grid{}
  grid.lights = map[Point]int{}
  for x := 0; x < maxX; x ++ {
    for y := 0; y < maxY; y ++ {
      grid.lights[Point{x, y}] = 0
    }
  }
  grid.onCount = 0
  grid.maxX = maxX
  grid.maxY = maxY
  return grid
}

func (g Grid) Print() {
  if g.maxX > 80 || g.maxY > 80 {
    fmt.Printf("%+v too big to print\n", g)
    return
  }
  for y := 0; y < g.maxY; y ++ {
    s := ""
    errs := []error{}
    for x := 0; x < g.maxX; x ++ {
      on, err := g.Get(x, y)
      if err != nil {
        s += "?"
        errs = append(errs, err)
      } else if on > 0 {
        s += "#"
      } else {
        s += "."
      }
    }
    fmt.Println(s)
  }
}

func (g Grid) Get(x, y int) (int, error) {
  p := Point{x, y}
  val, ok := g.lights[p]
  if !ok {
    return -1, fmt.Errorf("%v is outside range", p)
  }
  return val, nil
}

func (g *Grid) TurnOff(x, y int) error {
  p := Point{x, y}
  on, ok := g.lights[p]
  if !ok {
    return fmt.Errorf("%v is outside range", p)
  }
  g.lights[p] = 0
  if on > 0 { // if it was on, count that it's off now
    g.onCount -= 1
  }
  return nil
}

func (g *Grid) TurnOn(x, y int) error {
  p := Point{x, y}
  on, ok := g.lights[p]
  if !ok {
    return fmt.Errorf("%v is outside range", p)
  }
  g.lights[p] = 1
  if on <= 0 { // if it was off...
    g.onCount += 1
  }
  return nil
}


func (g *Grid) Add(x, y, delta int) error {
  p := Point{x, y}
  on, ok := g.lights[p]
  if !ok {
    return fmt.Errorf("%v is outside range", p)
  }
  g.lights[p] += delta
  if g.lights[p] < 0 {
    g.lights[p] = 0
  }
  if on <= 0 { // if it was off...
    g.onCount += 1
  }
  return nil
}

func (g *Grid) Toggle(x, y int) error {
  p := Point{x, y}
  on, ok := g.lights[p]
  if !ok {
    return fmt.Errorf("%v is outside range", p)
  }
  if on > 0 {
    g.lights[p] = 0
    g.onCount -= 1
  } else {
    g.lights[p] = 1
    g.onCount += 1
  }
  return nil
}

func (g *Grid) TurnOffRange(x1, y1, x2, y2 int) []error {
  // Ranges are inclusive.
  errs := []error{}
  for x := x1; x <= x2; x ++ {
    for y := y1; y <= y2; y ++ {
      err := g.TurnOff(x, y) //TODO: handle errors properly
      if err != nil {
        errs = append(errs, err)
      }
    }
  }
  return errs
}

func (g *Grid) TurnOnRange(x1, y1, x2, y2 int) []error {
  // Ranges are inclusive.
  errs := []error{}
  for x := x1; x <= x2; x ++ {
    for y := y1; y <= y2; y ++ {
      err := g.TurnOn(x, y)
      if err != nil {
        errs = append(errs, err)
      }
    }
  }
  return errs
}

func (g *Grid) AddRange(x1, y1, x2, y2, delta int) []error {
  // Ranges are inclusive.
  errs := []error{}
  for x := x1; x <= x2; x ++ {
    for y := y1; y <= y2; y ++ {
      err := g.Add(x, y, delta)
      if err != nil {
        errs = append(errs, err)
      }
    }
  }
  return errs
}

func (g *Grid) ToggleRange(x1, y1, x2, y2 int) []error {
  // Ranges are inclusive.
  errs := []error{}
  for x := x1; x <= x2; x ++ {
    for y := y1; y <= y2; y ++ {
      err := g.Toggle(x, y)
      if err != nil {
        errs = append(errs, err)
      }
    }
  }
  return errs
}

func (g Grid) Brightness() int {
  brightness := 0
  for x := 0; x < g.maxX; x ++ {
    for y := 0; y < g.maxY; y ++ {
      brightness += g.lights[Point{x, y}]
    }
  }
  return brightness
}

func (g Grid) String() string {
  return fmt.Sprintf("Grid(%d items, %d on, %d bright)", len(g.lights), g.onCount, g.Brightness())
}

type Instruction struct {
  action string
  x1, x2, y1, y2 int
}

func main() {
  gridSize := 1000

  var filename string
  if len(os.Args) > 1 {
    filename = os.Args[1]
  } else {
    filename = "input.txt"
  }

  s, err := ReadToStringSlice(filename)
  if err != nil {
    log.Fatal(err)
  }


  grid := NewGrid(gridSize, gridSize)
  grid.Print()

  // Parse instructions
  instructions := []Instruction{}
  for _, line := range s {
    var action string
    var x1, y1, x2, y2 int
    found := 0
    found, _ = fmt.Sscanf(line, "turn %s %d,%d through %d,%d", &action, &x1, &y1,
                           &x2, &y2)
    if found == 0 {
      found, _ = fmt.Sscanf(line, "%s %d,%d through %d,%d", &action, &x1, &y1,
                            &x2, &y2)
    }
    if found == 0 {
      log.Fatalf("Failed to parse %s", line)
    }
    instructions = append(instructions, Instruction{action, x1, x2, y1, y2})
  }

  // Part 1
  errs := []error{}
  for _, in := range instructions {
    if in.action == "on" {
      errs = grid.TurnOnRange(in.x1, in.y1, in.x2, in.y2)
    } else if in.action == "off" {
      errs = grid.TurnOffRange(in.x1, in.y1, in.x2, in.y2)
    } else if in.action == "toggle" {
      errs = grid.ToggleRange(in.x1, in.y1, in.x2, in.y2)
    } else {
      log.Fatalf("Unexpected instruction: %s", in.action)
    }
    if len(errs) != 0 {
      fmt.Println(errs)
    }
  }
  grid.Print()

  // Part 2
  fmt.Println("Resetting grid.")
  grid = NewGrid(gridSize, gridSize)
  grid.Print()
  errs = []error{}

  for _, in := range instructions {
    if in.action == "on" {
      errs = grid.AddRange(in.x1, in.y1, in.x2, in.y2, 1)
    } else if in.action == "off" {
      errs = grid.AddRange(in.x1, in.y1, in.x2, in.y2, -1)
    } else if in.action == "toggle" {
      errs = grid.AddRange(in.x1, in.y1, in.x2, in.y2, 2)
    } else {
      log.Fatalf("Unexpected instruction: %s", in.action)
    }
    if len(errs) != 0 {
      fmt.Println(errs)
    }
  }
  fmt.Println(grid)
}
