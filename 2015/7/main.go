package main

import (
  "fmt"
  "log"
  "os"
  "strconv"
  "strings"

  . "github.com/whereistanya/aoc2015/util"
)

type Wireable interface {
  Signal() int
}

// RawSignal implements Wireable
type RawSignal struct {
  val int
}

func NewRawSignal(sval string) RawSignal {
  val, _ := strconv.Atoi(sval)
  // TODO a reasonable person would not hide the error here
  // but it's so nice to just call Signal() inline and not do error handling.
  return RawSignal{val: val}
}

func (r RawSignal) Signal() int {
  return r.val
}

// Wire implements Wireable
type Wire struct {
  in1, in2 Wireable
  cached_value int
  has_cached bool
  op string
  name string // for debugging
}

func (w *Wire) Signal() int {
  if w.has_cached {
    return w.cached_value
  }
  in1 := w.in1
  in2 := w.in2
  var val int

  switch w.op {
  case "EQUAL":
    val = in1.Signal()
  case "AND":
    val = in1.Signal() & w.in2.Signal()
  case "OR":
    val = in1.Signal() | in2.Signal()
  case "LSHIFT":
    val = in1.Signal() << in2.Signal()
  case "RSHIFT":
    val = in1.Signal() >> in2.Signal()
  case "NOT":
    val = ^in1.Signal() & 65535  // converting because signed int
  default:
    log.Fatal("Unexpected operator", w.op)
  }
  w.cached_value = val
  w.has_cached = true
  return val
}

type Circuit struct {
  wires map[string]*Wire
}

// Circuit constructor.
func NewCircuit() Circuit {
  return Circuit {
    wires: map[string]*Wire{},
  }
}

func (c *Circuit) FindOrAddWire(name string) *Wire {
  wire, found := c.wires[name]
  if !found {
    wire = &Wire{}
    wire.name = name
    wire.has_cached = false
    c.wires[name] = wire
  }
  return wire
}

func IsInt(s string) bool {
  if _, err := strconv.Atoi(s); err == nil {
    // it's a number!
    return true
  }
  return false
}

func (c *Circuit) AddConnection(out, op, in1, in2 string) {
  outwire := c.FindOrAddWire(out)
  outwire.op = op

  if IsInt(in1) {
    outwire.in1 = NewRawSignal(in1)
  } else {
    outwire.in1 = c.FindOrAddWire(in1)
  }

  if IsInt(in2) {
    outwire.in2 = NewRawSignal(in2)
  } else {
    outwire.in2 = c.FindOrAddWire(in2)
  }
}

func (c Circuit) GetWire(name string) int {
  wire := c.wires[name]
  return wire.Signal()
}

func (c Circuit) ZapCache() {
  for _, wire := range c.wires {
    wire.has_cached = false
  }
}

func (c Circuit) Print() {
  for k, v := range c.wires {
    sig := v.Signal()
    fmt.Printf("%s : %d \n", k, sig)
  }
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

  circuit := NewCircuit()
  for _, line := range lines {

    // First, parse into input and output sections
    split := strings.Split(line, " -> ")
    in := split[0]
    out := split[1]

    // Now get the inputs
    fields := strings.Fields(in)
    var op, in1, in2 string

    if len(fields) == 1 {
      op = "EQUAL"
      in1 = fields[0]
    } else if len(fields) == 2 {
      op = fields[0]
      in1 = fields[1]
    } else if len(fields) == 3 {
      in1 = fields[0]
      op = fields[1]
      in2 = fields[2]
    } else {
      log.Fatalf("Unexpected input %s", line)
    }
    circuit.AddConnection(out, op, in1, in2)
  }
  part1 := circuit.GetWire("a")
  fmt.Println("Part 1: ", part1)
  circuit.AddConnection("b", "EQUAL", fmt.Sprintf("%d", part1), "") 
  circuit.ZapCache()
  part2 := circuit.GetWire("a")
  fmt.Println("Part 2: ", part2)
}

