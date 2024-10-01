package main

import (
 "fmt"
 "log"
 "os"
 //"regexp"
 "strings"

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

  gift := `children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1`

  requirements := map[string]int{}
  var att string
  var val int
  reqs := strings.Split(gift, "\n")
  for _, req := range reqs {
    _, err = fmt.Sscanf(req, "%s %d", &att, &val)
    if err != nil {
      panic(err)
    }
    requirements[att] = val
  }
  fmt.Println("Requirements:", requirements)

  // Sues are numbered 1 to 500;
  // we use a list with 0 to 499 so need to remember to add 1
  sues := []map[string]int{}

  // Sue 10: perfumes: 10, trees: 6, cars: 4

  var att1, att2, att3 string
  var val1, val2, val3 int
  var name string
  for _, line := range lines {
    // Kind of gross but attributes have ":" at the end because
    // of how Sscanf parses the line. It works but ugh a better
    // person would rewrite this.
    _, err = fmt.Sscanf(line, "Sue %s %s %d, %s %d, %s %d", &name, &att1, &val1,
      &att2, &val2, &att3, &val3)
    if err != nil {
      panic(err)
    }
    attributes := map[string]int{}
    attributes[att1] = val1
    attributes[att2] = val2
    attributes[att3] = val3
    sues = append(sues, attributes)
  }

  // Part 1
  for i, sue := range sues {
    possible := true
    for req, val := range requirements {
      _, found := sue[req]
      if found && sue[req] != val {
        possible = false
        break
      }
    }
    if !possible {
      continue
    }
    number := i + 1
    fmt.Printf("Part 1: Sue %d is possible\n", number)
  }
 // Part 2
  for i, sue := range sues {
    possible := true
    for req, val := range requirements {
      sueVal, found := sue[req]
      if found {
        if (req == "trees:" || req == "cats:") {
          if sueVal <= val {
            possible = false
            break
          }
        } else if (req == "pomeranians:" || req == "goldfish:") {
          if sueVal >= val {
            possible = false
            break
          }
        } else {
          if sueVal != val {
            possible = false
            break
          }
        }
      }
    }
    if !possible {
      continue
    }
    number := i + 1
    fmt.Printf("Part 2: Sue %d is possible\n", number)
  }
}


