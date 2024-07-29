package main

import (
 "crypto/md5"
 "encoding/hex"
 "fmt"
 "log"
 "os"

 //. "github.com/whereistanya/aoc2015/util"
)

func Hash(text []byte) string {
  hash := md5.Sum(text)
  return hex.EncodeToString(hash[:])
}

func main() {

/*
  var filename string
  if len(os.Args) > 1 {
    filename = os.Args[1]
  } else {
    filename = "input.txt"
  }

  s, err := ReadToRunes(filename)
  if err != nil {
    log.Fatal(err)
  } */


  // md5hash(inputdddddd) should start with 5 zeroes
  // find the lowest value of dddddd

  input := "iwrupvqb"
  i := 0
  part1Found := false

  for {
    toTry := fmt.Sprintf("%s%d", input, i)
    hash := Hash([]byte(toTry))
    if !part1Found && hash[:5] == "00000" {
      fmt.Printf("Part 1: %d\n", i)
      part1Found = true
    }
    if hash[:6] == "000000" {
      fmt.Printf("Part 2: %d\n", i)
      os.Exit(0)
    }
    if i > 100000000 {
      log.Fatal("Bug? Didn't expect to go this long")
    }
    i += 1
  }
}
