package main

import (
 "fmt"
 "log"
 "os"
 "os/exec"

 . "github.com/whereistanya/aoc2015/util"
)

type Point struct {
  x, y int
}

type Grid struct {
  originalConfig map[Point]int
  lights map[Point]int
  pending map[Point]int
  maxX, maxY int
}

func NewGrid(lines []string) Grid {
  grid := Grid{}
  grid.maxX = len(lines[0])
  grid.maxY = len(lines)
  grid.lights = map[Point]int{}
  grid.pending = map[Point]int{}
  grid.Reset(lines, false)

  return grid
}

func (g *Grid) Reset(lines []string, resetCorners bool) {
  fmt.Printf("Reset with %d lines\n", len(lines))
  for y, line := range lines {
    for x, val := range line {
      if val == '#' {
        g.Set(x, y, 1)
      } else if val == '.' {
        g.Set(x, y, 0)
      } else {
        fmt.Println(val)
        panic("Bad val")
      }
    }
  }
  if resetCorners {
    g.SetCornersOn()
  }
}

func (g *Grid) SetCornersOn() {
  g.Set(0, 0, 1)
  g.Set(0, g.maxY - 1, 1)
  g.Set(g.maxX - 1, 0, 1)
  g.Set(g.maxX - 1, g.maxY - 1, 1)
}


func (g *Grid) Tick(resetCorners bool) {
  g.lights = g.pending
  g.pending = map[Point]int{}
  if resetCorners {
    g.SetCornersOn()
  }
}

func (g Grid) Print() {
  if g.maxX > 100 || g.maxY > 100 {
    fmt.Printf("%+v too big to print\n", g)
    return
  }

  cmd := exec.Command("clear")
  cmd.Stdout = os.Stdout
  cmd.Run()

  for y := 0; y < g.maxY; y ++ {
    s := ""
    //errs := []error{}
    for x := 0; x < g.maxX; x ++ {
      on, err := g.Get(x, y)
      if err != nil {
        s += "?"
        panic(err)
      } else if on > 0 {
        s += "#"
      } else if on == 0 {
        s += "."
      } else {
        s += "!"
      }
    }
    fmt.Println(s)
  }
  fmt.Println()
}

func (g *Grid) Set(x, y int, val int) {
  p := Point{x, y}
  g.lights[p] = val
}

func (g Grid) Get(x, y int) (int, error) {
  p := Point{x, y}
  val, ok := g.lights[p]
  if !ok {
    return -1, fmt.Errorf("%v is outside range", p)
  }
  return val, nil
}

func (g Grid) String() string {
  return fmt.Sprintf("Grid(%d items)", len(g.lights))
}

func (g Grid) Neighbors(x, y int) []Point {
  vals := []int{ -1, 0, 1 }
  neighbors := []Point{}
  for _, dx := range vals {
    newX := x + dx
    if newX < 0 || newX >= g.maxY {
      continue
    }
    for _, dy := range vals {
      if dx == 0 && dy == 0 {
        continue  // not a neighbor, it's the original point
      }
      newY := y + dy
      if newY < 0 || newY >= g.maxY {
        continue
      }
      neighbors = append(neighbors, Point{newX, newY})
    }
  }
    return neighbors
}

func (g Grid) OnCount() int {
  count := 0
  for _, val := range g.lights {
    if val == 1 {
      count += 1
    }
  }
  return count
}

func (g Grid) CountNeighborsOn(x, y int) (int, error) {
  if x < 0 || x > g.maxX || y < 0 || y > g.maxY {
    return -1, fmt.Errorf("%d, %d is out of range")
  }
  neighbors := g.Neighbors(x, y)
  count := 0
  for _, n := range neighbors {
    lit, err := g.Get(n.x, n.y)
    if err != nil {
      return -1, err
    }

    if lit == 1 {
      count += 1
    } else if lit != 0 {
      fmt.Println(lit)
      panic("unexpected value")
    }
  }
  return count, nil
}

func (g *Grid) GenerateNextPattern() error {
  for point, litness := range g.lights {
    count, err := g.CountNeighborsOn(point.x, point.y)
    if err != nil {
      return err
    }
    if litness == 1 && (count == 2 || count == 3) {
      g.pending[point] = 1
    } else if litness == 0 && count == 3 {
      g.pending[point] = 1
    } else {
      g.pending[point] = 0
    }
  }
  return nil
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

  grid := NewGrid(lines)
  grid.Print()

  resetCorners := false
  grid.Reset(lines, resetCorners)
  grid.Print()
  steps := 100
  for step := 0; step < steps; step++ {
    grid.GenerateNextPattern()
    grid.Tick(resetCorners)
  }
  part1 := grid.OnCount()

  resetCorners = true
  grid.Reset(lines, resetCorners)
  grid.Print()

  for step := 0; step < steps; step++ {
    grid.GenerateNextPattern()
    grid.Tick(resetCorners)
    grid.Print()
  }

  part2 := grid.OnCount()

  fmt.Printf("Part 1: %d\n", part1)
  fmt.Printf("Part 2: %d\n", part2)
}
