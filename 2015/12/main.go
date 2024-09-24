package main

import (
 "fmt"
 "encoding/json"
 "os"
 "regexp"
 "strconv"
 "log"

  . "github.com/whereistanya/aoc2015/util"
)

func SumFromJson(js []byte, totalSoFar int, part2 bool) int {
  // if unsuccessful, try unmarshalling into a map
  //  if *that's successful* call SumFromJson on each value in the map
  // if neither array nor map unmarshalling worked, we hope it's a raw value
  //  try AToiing it and see if it's a number; if so, return it
  //    if not, print it out for debugging; should be a color...
  var items []interface{}
  var fields map[string]interface{}
  var n int
  var str string

  err := json.Unmarshal(js, &items)
  if err == nil { // it was an array
    for _, item := range items {
      recoded, err := json.Marshal(item)
      if err != nil {
        log.Fatal("Couldn't remarshal", item)
      }
      totalSoFar = SumFromJson(recoded, totalSoFar, part2)
    }
  } else { // not an array
    err = json.Unmarshal(js, &fields)
    if err == nil { // it was a map
      containsRed := false  // part 2 silliness
      for _, v := range fields {
        if v == "red" {
          containsRed = true
        }
      }
      if part2 && containsRed {
        // don't go deeper!
        return totalSoFar
      }
      for _, v := range fields {
        recoded, err := json.Marshal(v)
        if err != nil {
          log.Fatal("Couldn't remarshal", v)
        }
        totalSoFar = SumFromJson(recoded, totalSoFar, part2)
      }
    } else {  // not a map either!
      err := json.Unmarshal(js, &n)
      if err == nil {  // it was an int!
        return totalSoFar + n
      } else { // not an int
        err := json.Unmarshal(js, &str)
        if err != nil { // it was NOT a string!
          log.Fatal("couldn't parse", string(js))
        }
      }
    }
  }
  return totalSoFar
}

func main() {

  var filename string
  if len(os.Args) > 1 {
    filename = os.Args[1]
  } else {
    filename = "input.txt"
  }
  s, err := ReadToString(filename)
  if err != nil {
    fmt.Println(err)
  }

  // Part1: Regexp out the numbers
  numbersRE := regexp.MustCompile(`[-]?\d[\d]*`)
  numbers := numbersRE.FindAllString(s, -1)
  sum := 0
  for _, n := range numbers {
    val, err := strconv.Atoi(n)
    if err != nil {
      log.Fatal("Couldn't Atoi", err)
    } else {
      sum += val
    }
  }
  fmt.Println("Part 1:", sum)


  // Part1 again because apparently we meant it with the JSON
  part1 := SumFromJson([]byte(s), 0, false) // false=not part two
  fmt.Println("Part 1:", part1)

  // Part2, no we mean it with the JSON
  part2 := SumFromJson([]byte(s), 0, true)
  fmt.Println("Part 2:", part2)



}


