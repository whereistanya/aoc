package main

import (
 "fmt"
 "log"
 "os"

 . "github.com/whereistanya/aoc2015/util"
)

func main() {

  var filename string
  if len(os.Args) > 1 {
    filename = os.Args[1]
  } else {
    filename = "input.txt"
  }

  s, err := ReadToRunes(filename)
  if err != nil {
    log.Fatal(err)
  }

  floor := 0
  pos := -1
  for i := 0; i < len(s); i++ {
    if s[i] == '(' {
      floor += 1
    } else if s[i] == ')' {
      floor -= 1
    } else {
      fmt.Printf("%c ???", s[i])
    }
    if floor < 0 && pos == -1 {  // -1 means unset
      pos = i + 1 // positions are 1-indexed not 0-indexed
    }
  }
  fmt.Printf("Part 1: %d\n", floor)
  fmt.Printf("Part 2: %d\n", pos)
}


