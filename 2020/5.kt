// Advent of code 2020 day 5
import java.io.File

fun main() {
  val fileName = "input5.txt"
  val lines: List<String> = File(fileName).readLines()

  val rows: MutableMap<Int, MutableList<Int>> = mutableMapOf<Int, MutableList<Int>>()

  for (line in lines) {
    var row = Integer.parseInt(line.replace("B", "1").replace("F", "0").substring(0, 7), 2)
    var seat = Integer.parseInt(line.replace("R", "1").replace("L", "0").takeLast(3), 2)

    if (rows.containsKey(row)) {
      rows[row]?.add(seat)
    } else {
      rows[row] = mutableListOf<Int>(seat)
    }
  }

  for ((row, seats) in rows.toSortedMap()) {
    //println("${row.toString().padStart(5)}, ${seats.sorted()}")
    if (seats.size != 7) {
      continue
    }
    for (i in 0..7) {
      if (seats.contains(i) == false) {
        val value = 8 * row + i
        println( "$value")
      }
    }
  }
}
