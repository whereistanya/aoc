// Advent of code 2020 day 13. Far far from optimal.
import java.io.File

fun main() {
  val arrival = 1006726
  val input = "23,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,647,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,13,19,x,x,x,x,x,x,x,x,x,29,x,557,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,17"

  val buses: List<Int> = input.trim().split(",").filter {
      it != "x" }.map { it.toInt() }

  val timeMap = mutableMapOf<Int, Int>()
  for (bus in buses) {
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

  // Part one.
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

  // Part two.
  val part2: List<String> = input.trim().split(",")
  val factors = mutableListOf<Int>()
  // 647, the 23rd bus, is the biggest number, so anchor on that.
  // This fact list is not used; it's just to print out for
  // understanding how far away from 23 everything else is.
  for (i in (0..(part2.size) - 1)) {
    if (part2[i] == "x") {
      factors.add(-1)
    } else {
      factors.add(part2[i].toInt())
    }
    println("${i - 23}, ${part2[i]}")
  }
  // println(factors)

  val zero: Long = 0  // This can't be the best way to compare a long against
                      // zero...
  var j: Long = 647   // Could shave some minutes by starting at the first
                      // multiple of 647 over 100000000000000 but whatevs.
  // This code would be clearer if I took the numbers in order, but it's an
  // order of magnitude fewer checks to test every 647th number rather than
  // every 23rd one.
  while (true) {
    j += 647
    if ((j + 31) % 557 != zero) {
      continue
    }
    if ((j - 10) % 41 != zero) {
      continue
    }
    if ((j + 37) % 37 != zero) {
      continue
    }
    if ((j + 29) % 29 != zero) {
      continue
    }
    if ((j - 23) % 23 != zero) {
      continue
    }
    if ((j + 19) % 19 != zero) {
      continue
    }
    if ((j + 48) % 17 != zero) {
      continue
    }
    if ((j + 18) % 13 != zero) {
      continue
    }
    println(j - 23) //      867295486378319, 29m later.
    break
    }
  }
  println("Part 2: $j - 23")

}
