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

  lines, err := ReadToStringSlice(filename)
  if err != nil {
    log.Fatal(err)
  }

  reps := map[string][]string{}

  starter := ""
  var first, second string
  for _, line := range lines {
    if line == "" {
      continue
    }
    ok, _ := fmt.Sscanf(line, "%s => %s", &first, &second)
    if ok == 2 {
      _, found := reps[first]
      if found {
        reps[first] = append(reps[first], second)
      } else {
        reps[first] = []string{second}
      }
      continue
    }

    // If it didn't match the sscanf, it's the starter string
    if starter != "" {
      panic("More than one non-matching line")
    }
    starter = line
  }

  fmt.Println("Starter:", starter)
  fmt.Println(reps)
}


