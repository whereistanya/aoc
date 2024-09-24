package main

import (
 "fmt"
 "log"
 "strings"
)

func LookSayV1(input string) string {
  outString := ""
  count := 1
  current := input[0]
  for i := 1; i < len(input); i++ {
    if input[i] == current {
      count += 1
    } else {
      outString += fmt.Sprintf("%d%c", count, current)
      current = input[i]
      count = 1
    }
  }
  outString += fmt.Sprintf("%d%c", count, current)
  return outString
}


func LookSayV3(input string) string {
  var outString strings.Builder
  count := 1
  current := input[0]
  for i := 1; i < len(input); i++ {
    if input[i] == current {
      count += 1
    } else {
      outString.WriteString(fmt.Sprintf("%d%c", count, current))
      current = input[i]
      count = 1
    }
  }
  outString.WriteString(fmt.Sprintf("%d%c", count, current))
  return outString.String()
}

func LookSayV2(input []string) []string {
  fmt.Println(input)
  outStrings := []string{}
  memo := map[string]int{}
  for i := 0; i < len(input); i++ {
    group := input[i]
    if (i + 1) < len(input) {
      followingGroup := input[i + 1]
      if group[len(group) - 1] == followingGroup[0] {
        fmt.Println("Groups should merge")
        log.Fatal("Unimplemented")
      }
    }
    _, found := memo[group]
    if found {
      memo[group] += 1
    } else {
      memo[group] = 1
    }
    outString := LookSayV1(group)
    outStrings = append(outStrings, outString)
  }
  fmt.Println(memo)
  return outStrings
}

func main() {
  input := "1113122113"

  for i := 1; i <= 50; i++ {
    input = LookSayV3(input)
    fmt.Printf("After %d: %d\n", i, len(input))
  }
}
