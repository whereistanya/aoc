package main

import (
 "fmt"
 "log"
)

func IsValid(s string) bool {
  // 8 lowercase letters
  // one increasing straight of at least three letters
  // can't contain i, o or l
  // must contain at least two different non-overlapping pairs

  chars := []rune(s)

  pairs := map[string]bool{}
  foundRun := false

  for i, c := range chars {
    if c == 'i' || c == 'l' || c == 'o' {
      return false
    }
    spaceRemaining := len(chars) - i
    if spaceRemaining >= 2 {
      if chars[i + 1] == chars[i] {
        pairs[fmt.Sprintf("%c", chars[i])] = true
      }
    }
    if spaceRemaining >= 3 {
      if (chars[i+1] - chars[i] == 1) && (chars[i+2] - chars[i+1] == 1) {
        foundRun = true
      }
    }
  }

  if len(pairs) < 2 {
    return false
  }
  if !foundRun {
    return false
  }

  return true
}

func IncrementTerriblePassword(s string) string {
  chars := []rune(s)
  i := len(chars) - 1
  for {
    if chars[i] == 'z' {
      chars[i] = 'a'
      i -= 1
    } else {
      chars[i] += 1
      break
    }
    if i < 0 {
      return "Shouldn't ever get a string like this..."
    }
  }
  return string(chars)
}

func main() {

  if IsValid("hepxcrrq") {
    log.Fatal("hepxcrrq is supposed to be INVALID. Your code sucks.")
  }
  if !IsValid("xxyyabcx") {
    log.Fatal("xxyyabcx is totally valid wtf?")
  }

  pw := "hepxcrrq"
  for {
    pw = IncrementTerriblePassword(pw)
    if IsValid(pw) {
      fmt.Printf("Part 1: %s is the next valid password\n", pw)
      break
    }
  }
  for {
    pw = IncrementTerriblePassword(pw)
    if IsValid(pw) {
      fmt.Printf("Part 2: %s is the next valid password\n", pw)
      break
    }
  }


}



