package main

import (
 "fmt"
 "log"
 "os"
 "strconv"

 . "github.com/whereistanya/aoc2015/util"
)

func generateFillCombinations(toFill int, current int, containers []int, counter *int) {
// current is an index into the list of containers, rather than passing
// sub-slices around. But maybe that'd be fine? TODO: do both ways and see.
  if toFill == 0 {
    *counter += 1
    return
  }

  for i := current; i < len(containers); i++ {
    if containers[i] <= toFill {
      generateFillCombinations (toFill - containers[i], i + 1, containers, counter)
    }
  }
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

  containers := []int{}
  for _, line := range lines {
    val, err := strconv.Atoi(line)
    if err != nil {
      panic(err)
    } else {
      containers = append(containers, val)
    }
  }

  fmt.Println(containers)

  combinationCount := new(int)

  total := 150 // 25 for testing; 150 for reals
  generateFillCombinations(total, 0, containers, combinationCount)

  fmt.Println("Part 1", *combinationCount)
}


