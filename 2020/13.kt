// Advent of code 2020
import java.io.File

fun main() {
  val arrival = 1006726
  val input = "23,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,647,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,13,19,x,x,x,x,x,x,x,x,x,29,x,557,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,17"

  //val arrival = 939
  //val input ="7,13,x,x,59,x,31,19"

  val buses: List<Int> = input.trim().split(",").filter {
      it != "x" }.map { it.toInt() }

  val timeMap = mutableMapOf<Int, Int>()
  for (bus in buses) {
    println(bus)
    var i = 0
    while (true) {
      val minute = bus * i
      timeMap[minute] = bus
      if (minute > (arrival * 1.2)) {
        break
      }
      i += 1
    }
  }

  var i = arrival
  while (true) {
    if (timeMap.contains(i)) {
      val busId = timeMap[i]
      val minutes = i - arrival
      val answer = minutes * busId!!
      println("bus id: $busId")
      println("minutes: $minutes")
      println("puzzle answer: $answer")
      break
    }
    i += 1
  }
}
