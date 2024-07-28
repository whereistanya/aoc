package main

import (
 "fmt"
 "log"
 "math" // for MaxInt64()
 "os"
 //"strconv"
 //"strings"

 . "github.com/whereistanya/aoc2015/util"
)

func getPaper(l, w, h int) int {
  // 2*l*w + 2*w*h + 2*h*l
  // plus the area of the smallest side
  smallest := math.MaxInt64
  needed := 0
  sides := []int{l * w, w * h, h * l}
  for _, side := range sides {
    needed += 2 * side
    if side < smallest {
      smallest = side
    }
  }
  needed += smallest
  return needed
}

func getRibbon(l, w, h int) int {
  smallest := math.MaxInt64
  volume := l * w * h
  sides := []int{l + l + w + w,
                 w + w + h + h,
                 h + h + l + l }
  for _, side := range sides {
    if side < smallest {
      smallest = side
    }
  }
  return smallest + volume
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
  paper := 0
  ribbon := 0
  for _, line := range lines {
    var l, w, h int
    _, err := fmt.Sscanf(line, "%dx%dx%d", &l, &w, &h)
    if err != nil {
      log.Fatal(err)
    }
    paper += getPaper(l, w, h)
    ribbon += getRibbon(l, w, h)
  }
  fmt.Printf("Part 1: %d\n", paper)
  fmt.Printf("Part 2: %d\n", ribbon)
}


