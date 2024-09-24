package main

import (
 "fmt"
 "log"
 "os"
 "strconv"

 . "github.com/whereistanya/aoc2015/util"
)

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
  ssum := 0
  msum := 0
  qsum := 0

  for _, line := range lines {

    fmt.Println("# ", line)
    uq, _ := strconv.Unquote(line)
    q := strconv.QuoteToASCII(line)
    fmt.Println(": ", uq, len(uq))
    fmt.Println(". ", q, len(q))
    ssum += len(uq)
    msum += len(line)
    qsum += len(q)
  }
  fmt.Printf("Part 1: %d - %d = %d\n", msum, ssum, msum - ssum)
  fmt.Printf("Part 2: %d - %d = %d\n", qsum, msum, qsum - msum)

}


