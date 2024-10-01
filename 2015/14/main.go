package main

import (
 "fmt"
 "log"
 "os"
 //"sort"

 . "github.com/whereistanya/aoc2015/util"
)

type Status int
const (
  MOVING Status = 1
  RESTING    = 2
)

type Reindeer struct {
  name string
  status Status
  // base stats; set at creation time
  speed, moveDuration, restDuration int
  // time to status change, distance and score change throughout the race
  nextStatusChange, distance, score int
}

func NewReindeer(name string, speed, moveDuration, restDuration int) *Reindeer {
  return &Reindeer {
    name: name,
    speed: speed,
    moveDuration: moveDuration,
    restDuration: restDuration,
    nextStatusChange: moveDuration,
    score: 0,
    distance: 0,
    status: MOVING,
  }
}

type RaceStats struct {
  racers map[string]*Reindeer
  // scores map[string]int
}

func NewRaceStats() *RaceStats {
  return &RaceStats {
    racers: map[string]*Reindeer{},
    //scores: map[string]int{},
  }
}

func (r *RaceStats) Reset() {
  for _, deer := range r.racers {
    deer.distance = 0
    deer.score = 0
  }
}
func (r *RaceStats) Tick() {
  // Move on one second.
  // First, add distances for moving deer.
  // Then update time to status change.
  // If applicable, change status.
  // Changed statuses don't apply until next time.
  for _, deer := range r.racers {

    // TODO: switch statement
    deer.nextStatusChange -= 1
    if deer.status == MOVING {
      deer.distance += deer.speed
      if deer.nextStatusChange == 0 {
        deer.status = RESTING
        deer.nextStatusChange = deer.restDuration
      }
    } else if deer.status == RESTING {
      if deer.nextStatusChange == 0 {
        deer.status = MOVING
        deer.nextStatusChange = deer.moveDuration
      }
    }
  }
  leaders := r.Leaders()
  for _, leader := range leaders{
    leader.score += 1
  }
}

func (r RaceStats) HighScore() []*Reindeer {
  highScore := 0
  var winners []*Reindeer
  for _, deer := range r.racers {
    if deer.score > highScore {
      highScore = deer.score
      winners = []*Reindeer{deer}
    } else if deer.score == highScore {
      winners = append(winners, deer)
    }
  }
  return winners
}

func (r RaceStats) Leaders() []*Reindeer {
  furthest := 0
  var winners []*Reindeer
  for _, deer := range r.racers {
    if deer.distance > furthest {
      furthest = deer.distance
      winners = []*Reindeer{deer}
    } else if deer.distance == furthest {
      winners = append(winners, deer)
    }
  }
  return winners
}

/*
func (r RaceStats) HighestScore() int {
  keys := []string{}
  for k := range r.scores {
    keys = append(keys, k)
  }
  sort.Slice(keys, func(i, j int) bool {
    return r.scores[keys[i]] > r.scores[keys[j]] })
  return r.scores[keys[0]]
}*/

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

  duration := 2503
  rs := NewRaceStats()

  var speed, moveDuration, restDuration int
  var name string
  for _, line := range(lines) {
    // Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    // Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
    fmt.Sscanf(line, "%s can fly %d km/s for %d seconds, but then must rest for %d seconds.", &name, &speed, &moveDuration, &restDuration)

    reindeer := NewReindeer(name, speed, moveDuration, restDuration)
    rs.racers[name] = reindeer

    // part1; move TODO
    distance := DistanceCalc(speed, moveDuration, restDuration, duration)
    rs.racers[name].distance = distance
  }
  fmt.Println("Part 1")
  winners := rs.Leaders()
  for _, w := range winners {
    fmt.Printf("%s is the winner with distance %d\n", w.name, w.distance)
  }

  // Part 2
  rs.Reset()
  // for testing
  // duration = 1000
  for i := 0; i < duration; i++ {
    rs.Tick()
  }

  fmt.Println("Part 2")
  winners = rs.HighScore()
  for _, w := range winners {
    fmt.Printf("%s is the winner with score %d\n", w.name, w.score)
  }

}


