package main

import (
 "fmt"
 "log"
 "os"

 . "github.com/whereistanya/aoc2015/util"
)

func isNice(s string) (bool, bool) {
  chars := []rune(s)
  badStrings := map[string]bool { "ab": true, "cd": true, "pq": true, "xy": true }
  vowels := map[rune]bool { 'a': true, 'e': true, 'i': true, 'o': true, 'u': true }

  // total vowels in the word
  vowelCount := 0
  // letter appears twice in a row
  hasDupe := false
  // strings to avoid
  hasBad := false
  // a pair of any two letters that appears 2+ times without overlapping
  hasRepeatingPair := false
  // a letter that repeats with exactly one letter in between
  hasSeparatedDupe := false

  dupletPositions := map[string]int{}

  for i, c := range chars {
    backOne := ' '
    backTwo := ' '
    if i > 0 {
      backOne = chars[i - 1]
    }
    if i > 1 {
      backTwo = chars[i - 2]
    }

    // Part 1: Check for bad list
    duplet := fmt.Sprintf("%c%c", backOne, c)
    _, bad := badStrings[duplet]
    if bad {
      hasBad = true
    }

    // Part 2: Check for repeating pair
    position, ok := dupletPositions[duplet]
    if !ok {  // only add the first instance
      dupletPositions[duplet] = i
    } else if position < i - 1 {
        hasRepeatingPair = true
    }

    // Part 1: Check for vowel count
    _, ok = vowels[c]
    if ok {
      vowelCount += 1
    }

    // Part 1: Check for dupe
    if c == backOne {
      hasDupe = true
    }

    // Part 2: Check for separated dupe
    if c == backTwo {
      hasSeparatedDupe = true
    }
  }

  partOneNice := hasDupe && !hasBad && vowelCount >= 3
  partTwoNice := hasSeparatedDupe && hasRepeatingPair

  return partOneNice, partTwoNice
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
  part2NiceCount := 0
  for _, line := range(lines) {
    nice1, nice2 := isNice(line)
    fmt.Printf("%s : %v, %v\n", line, nice1, nice2)
    if nice1 {
      part1NiceCount += 1
    }
    if nice2 {
      part2NiceCount += 1
    }
  }
  fmt.Printf("Part 1: %d\n", part1NiceCount)
  fmt.Printf("Part 2: %d\n", part2NiceCount)
}


