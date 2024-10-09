package main

import (
 "fmt"
 "log"
 "math"
 "os"
 "strconv"

 . "github.com/whereistanya/aoc2015/util"
)

func generateFillCombinations(toFill int, containers []int,
                              counter *int, depth int, depths map[int]int) {
  if toFill == 0 {
    *counter += 1
    _, found := depths[depth]
    if found {
      depths[depth] += 1
    } else {
      depths[depth] = 1
    }
    return
  }

  for i := 0; i < len(containers); i++ {
    if containers[i] <= toFill {
      // subslicing containers for the second arg here. Compared it with passing
      // around an index and it's around the same time to run: looks like go
      // does the right thing without any copying overhead.
      generateFillCombinations (toFill - containers[i], containers[i + 1:], counter, depth + 1, depths)
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

  combinationCount := new(int)
  depths := map[int]int{} // for part 2

  total := 150 // 25 for testing; 150 for reals
  generateFillCombinations(total, containers, combinationCount, 0, depths)

  fmt.Println("Part 1", *combinationCount)

  lowest := math.MaxInt64
  for k, _ := range depths {
    if k < lowest {
      lowest = k
    }
  }
  fmt.Println("Part 2:", depths[lowest])
}


