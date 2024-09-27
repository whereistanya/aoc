package main

import (
 "fmt"
 "log"
 "os"
 "sort"

 . "github.com/whereistanya/aoc2015/util"
)


type Reindeer struct {
  name string
  // base stats; set at creation time
  speed, moveDuration, restDuration int
  // current status; changes throughout the race
  timeBeforeMoving, remainingRaceTime, score int
}
func NewReindeer(name string, speed, moveDuration, restDuration int) *Reindeer {
  return &Reindeer {
    name: name,
    speed: speed,
    moveDuration: moveDuration,
    restDuration: restDuration,
    timeBeforeMoving: 0,
    remainingRaceTime: 0,
    score: 0,
  }
}

type RaceStats struct {
  racers map[string]Reindeer
  scores map[string]int
}

func NewRaceStats() *RaceStats {
  return &RaceStats {
    racers: map[string]Reindeer{},
    scores: map[string]int{},
  }
}

func (r RaceStats) Score() int {
  keys := []string{}
  for k := range r.scores {
    keys = append(keys, k)
  }
  sort.Slice(keys, func(i, j int) bool {
    return r.scores[keys[i]] > r.scores[keys[j]] })
  return r.scores[keys[0]]
}

// For Part1
func DistanceCalc(speed, moveDuration, restDuration, raceTime int) int {
  distance := 0
  for (raceTime > (moveDuration + restDuration)) {
    distance += (speed * moveDuration)
    raceTime -= (moveDuration + restDuration)
  }
  if raceTime >= moveDuration {
    distance += (speed * moveDuration)
  } else {
    distance += (speed * raceTime)
  }
  return distance
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
  // Tests
  // fmt.Println(DistanceCalc(14, 10, 127, 1000))
  // fmt.Println(DistanceCalc(16, 11, 162, 1000))

  rs := NewRaceStats()

  var speed, moveDuration, restDuration int
  var name string
  for _, line := range(lines) {
    fmt.Sscanf(line, "%s can fly %d km/s for %d seconds, but then must rest for %d seconds.", &name, &speed, &moveDuration, &restDuration)

    reindeer := NewReindeer(name, speed, moveDuration, restDuration)
    fmt.Println(reindeer)

    // part1; move TODO
    fmt.Println(DistanceCalc(speed, moveDuration, restDuration, 2503))
  }
  fmt.Println(rs.Score())

  // Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
  // Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

  // Given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, what distance has the winning reindeer traveled?
}


