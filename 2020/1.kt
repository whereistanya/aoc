// Advent of code 2020 day 1
import java.io.File

fun main() {
  val fileName = "input1.txt"
  val lines: Set<Int> = File(fileName).readLines().map { it.toInt() }.toSet()

  for (i in lines) {
    for (j in lines) {
      val remainder = 2020 - (i + j)
      if (lines.contains(remainder)) {
        println("Result: " + i * j * remainder)
        return
      }
    }
  }
}
