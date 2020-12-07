// Advent of code 2020 day 5
import java.io.File

fun main() {
  val fileName = "input6.txt"
  val lines: List<String> = File(fileName).readLines()

  var current = mutableMapOf<Char, Int>()
  var group_size:Int = 0
  var count:Int = 0

  for (line in lines) {
    if (line == "") {
      for (v in current.values) {
        if (v == group_size) {
          count = count + 1
        }
      }
      current.clear()
      group_size = 0
      continue
    }
    group_size += 1
    for (char in line) {
      if (current.containsKey(char)) {
        val charcount = current[char]
        if (charcount != null) {
          current[char] = charcount + 1
        }
      } else {
        current[char] = 1
      }
    }
  }
  for (v in current.values) {
    if (v == group_size) {
      count = count + 1
    }
  }
  println(count)
}
