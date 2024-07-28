package util

import (
 "bufio"
 "os"
 "strings"
)

// Strings are immutable slices of bytes
// Not slices of characters! len("A£") would be 3 not 2,
// because of the unicode character. I will definitely trip
// over this fact at some point.
func ReadToString(filename string) (string, error) {
  // ReadFile returns a slice of bytes
  b, err := os.ReadFile(filename)
  if err != nil {
    return "", err
  }
  // strip trailing and leading spaces if we got 'em
  return strings.TrimSpace(string(b)), nil
}

func ReadToRunes(filename string) ([]rune, error) {
  s, err := ReadToString(filename)
  if err != nil {
    return nil, err
  }
  return []rune(s), nil
}

func ReadToStringSlice(filename string) ([]string, error) {
  f, err := os.Open(filename)
  if err != nil {
    return nil, err
  }
  defer f.Close()

  var lines []string
  scanner := bufio.NewScanner(f)
  for scanner.Scan() {
    lines = append(lines, scanner.Text())
  }
  if err := scanner.Err(); err != nil {
    return nil, err
  }

  return lines, nil
}
