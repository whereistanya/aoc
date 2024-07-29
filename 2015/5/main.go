package main

import (
 "fmt"
 "log"
 "os"

 . "github.com/whereistanya/aoc2015/util"
)

func isNice(s string, part int) bool {
  chars := []rune(s)
  badStrings := map[string]bool { "ab": true, "cd": true, "pq": true, "xy": true }
  vowels := map[rune]bool { 'a': true, 'e': true, 'i': true, 'o': true, 'u': true }

  vowelCount := 0
  hasDupe := false
  hasBad := false
  //hasPair := false
  //hasSeparatedDupe = false


  last := ' '
  for _, c := range chars {
    duplet := fmt.Sprintf("%c%c", last, c)
    _, bad := badStrings[duplet]
    if bad {
      hasBad = true
      break
    }
    _, ok := vowels[c]
    if ok {
      vowelCount += 1
    }
    if c == last {
      hasDupe = true
    }

    last = c
  }

  if hasDupe && !hasBad && vowelCount >= 3 {
    return true
  }
  return false
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

  part1NiceCount := 0
  //part2NiceCount := 0
  for _, line := range(lines) {
    if isNice(line, 1) {
      part1NiceCount += 1
    }
    //fmt.Println(line, isNice(line))
  }
  fmt.Printf("Part 1: %d/n", part1NiceCount)
}


