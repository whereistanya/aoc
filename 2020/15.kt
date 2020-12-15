// Advent of code 2020 day 15
import java.io.File

fun main() {
  var input = "9,6,0,10,18,2,1"
  val numbers: List<Int> = input.split(",").map { it.toInt() }

  val seenPos = mutableMapOf<Int, MutableList<Int>>()       // position
  var i = 0
  var last = 0
  var next: Int
  for (last in numbers) {
    i += 1
    seenPos[last] = mutableListOf(i)
  }
  println("After init: $i, last: $last")

  while (i < 30000000) {
    i += 1
    var previous = seenPos[last]!!
    if (previous.size == 1) {
      next = 0
    } else {
      next = previous[previous.size - 1] - previous[previous.size - 2]
    }
    if (! seenPos.contains(next)) {
      seenPos[next] = mutableListOf(i)
    } else {
      seenPos[next]!!.add(i)
    }
    last = next
  }
  println("$i: $last")
}
