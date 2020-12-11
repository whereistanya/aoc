// Advent of code 2020
import java.io.File

class GameOfLife(state: List<String>) {
  var state: List<String> = state
  val height = state.size
  val width = state[0].length
  var occupied = 0

  fun countNeighboursPart1(x: Int, y: Int): Int {
    val directions: List<Pair<Int, Int>> = listOf(
      Pair(-1, -1), Pair(0, -1), Pair(1, -1),
      Pair(-1,  0),              Pair(1,  0),
      Pair(-1,  1), Pair(0,  1), Pair(1,  1))
    var count = 0
    for (direction in directions) {
      var newx = x
      var newy = y

      newx += direction.first
      newy += direction.second
      val row = this.state.getOrNull(newy)
      val seat = row?.getOrNull(newx)
      if (seat != null && seat == '#') {
        count += 1
      }
    }
    return count
  }

  fun countNeighboursPart2(x: Int, y: Int): Int {
    val directions: List<Pair<Int, Int>> = listOf(
      Pair(-1, -1), Pair(0, -1), Pair(1, -1),
      Pair(-1,  0),              Pair(1,  0),
      Pair(-1,  1), Pair(0,  1), Pair(1,  1))
    var count = 0
    for (direction in directions) {
      var newx = x
      var newy = y
      while (true) {
        newx += direction.first
        newy += direction.second
        val row = this.state.getOrNull(newy)
        //println("row ${row}")
        val seat = row?.getOrNull(newx)
        if (seat == '.') {
          // Look further for a seat
          continue
        }
        if (seat == null) {
          // Off the end of the world
          break
        }
        if (seat == 'L') {
          // Can't see further
          break
        }
        if (seat == '#') {
          count += 1
          break
        }
      }
    }
    return count
  }

  fun getNextSeat(current: Char, x: Int, y: Int, part: Int): Char {
    var count = 0
    var chairs = 4
    if (part == 1) {
      count = countNeighboursPart1(x, y)
      chairs = 4
    } else if (part == 2) {
      count = countNeighboursPart2(x, y)
      chairs = 5
    }

    if (current == 'L' && count == 0) {
      return '#'
    } else if (current == '#' && count >= chairs) {
      return 'L'
    } else {
      return current
    }
  }

  fun run(part: Int): Boolean {
    // Returns whether the state changed.
    // Create a new list
    // For each seat, check new position
    var newState = mutableListOf<String>()
    var changed = false
    var occupied = 0
    for (y in (0..this.height - 1)) {
      var s = ""
      for (x in (0..this.width - 1)) {
        val current = this.state[y][x]
        if (current == '.') {
          s += '.'
          continue
        }
        val nextChar = getNextSeat(current, x, y, part)
        s += nextChar
        if (current != nextChar) {
          changed = true
        }
        if (nextChar == '#') {
          occupied += 1
        }
      }
      newState.add(s)
      this.occupied = occupied
    }
    this.state = newState
    return changed
  }

  fun occupied(): Int{
    return this.occupied
  }

  fun draw() {
    for (y in (0..this.height - 1)) {
      var s:String = ""
      for (x in (0..this.width - 1)) {
        var line = this.state[y]
        s = s + line[x]
      }
      println("$s")
    }
    println()
  }
}

fun main() {
  val fileName = "input11.txt"
  var seats: List<String> = File(fileName).readLines().toMutableList()
/*
  seats = listOf<String>(
    "L.LL.LL.LL",
    "LLLLLLL.LL",
    "L.L.L..L..",
    "LLLL.LL.LL",
    "L.LL.LL.LL",
    "L.LLLLL.LL",
    "..L.L.....",
    "LLLLLLLLLL",
    "L.LLLLLL.L",
    "L.LLLLL.LL"
  )
*/

  // Part 1
  val game1 = GameOfLife(seats)
  var i = 0
  while (true) {
    i += 1
    //game1.draw()
    val changed = game1.run(1)
    if (! changed) {
      break
    }
  }
  println("Part 1: stopped after $i iterations")
  println("There are ${game1.occupied()} occupied seats")

  // Part 2
  val game2 = GameOfLife(seats)
  i = 0
  while (true) {
    i += 1
    //game2.draw()
    val changed = game2.run(2)
    if (! changed) {
      break
    }
  }
  println("Part 2: stopped after $i iterations")
  println("There are ${game2.occupied()} occupied seats")
}
