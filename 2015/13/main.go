package main

import (
 "fmt"
 "log"
 "os"
 "regexp"
 "strconv"

 . "github.com/whereistanya/aoc2015/util"
)

type Guest struct {
  name string
  opinions map[string]int
}

func NewGuest(name string) *Guest {
  return &Guest {
    name: name,
    opinions: map[string]int{},
  }
}

func FindMaximumHappiness(
  toSeat map[string]bool, seated []string, allGuests map[string]*Guest, soFar int) int {
  if len(toSeat) == 0 {
    // add the last/first relationships
    first := seated[0]
    last := seated[len(seated) - 1]
    delta := (allGuests[first].opinions[last] +
              allGuests[last].opinions[first])
    return soFar + delta
  }

  highest := 0
  for name, _ := range toSeat {
    delete(toSeat, name)
    position := len(seated)
    seated = append(seated, name)
    delta := 0
    if position >= 1 {
      prevName := seated[position - 1]
      delta = (allGuests[name].opinions[prevName] +
        allGuests[prevName].opinions[name])
    }
    happiness := FindMaximumHappiness(toSeat, seated, allGuests, soFar + delta)
    if happiness > highest {
      highest = happiness
    }
    seated = seated[:len(seated) - 1] // why doesn't go have a pop method what
                                      // is this language?
    toSeat[name] = true
  }
  return highest
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
  re := regexp.MustCompile(`(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).`)

  allGuests := map[string]*Guest{}

  var who, neighbor string
  var delta int
  for _, line := range lines {
    matches := re.FindStringSubmatch(line)
    who = matches[1]
    delta, err = strconv.Atoi(matches[3])
    if err != nil {
      log.Fatal(err)
    }
    neighbor = matches[4]
    if matches[2] == "lose" {
      delta *= -1
    } else if matches[2] != "gain" {
      log.Fatal("Unexpected verb: ", matches[2])
    }

    guest, found := allGuests[who]
    if !found {
      guest = NewGuest(who)
      allGuests[who] = guest
    }
    guest.opinions[neighbor] = delta
  }
  fmt.Println(allGuests)
  toSeat := map[string]bool{}
  for k, _ := range allGuests {
    toSeat[k] = true
  }
  seated := []string{}
  maximum := FindMaximumHappiness(toSeat, seated, allGuests, 0)
  fmt.Printf("Part1: %d\n", maximum)

  planner := NewGuest("thePlanner")
  for name, guest := range allGuests {
    guest.opinions["thePlanner"] = 0
    planner.opinions[name] = 0
  }
  allGuests["thePlanner"] = planner

  for k, _ := range allGuests {
    toSeat[k] = true
  }
  seated = []string{}
  maximum = FindMaximumHappiness(toSeat, seated, allGuests, 0)
  fmt.Printf("Part2: %d\n", maximum)
}


