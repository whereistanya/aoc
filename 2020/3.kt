// Advent of code 2020 day 3
import java.io.File

fun count_trees(move_right: Int, move_down: Int, lines: List<String>): Int {
  var count: Int = 0
  var x: Int = 0
  var y: Int = 0
  var tree: Char = '#'
  val height: Int = lines.size
  val width: Int = lines[0].length
  while (y < height) {
    if (lines[y][x] == tree) {
      count += 1
    }
    x += move_right
    x = x % width
    y += move_down
  }

  return count
}

fun main() {
  val inputfile = "input3.txt"
  val lines: List<String> = File(inputfile).readLines()

  val slopes = listOf(Pair(1, 1), Pair(3, 1), Pair(5, 1), Pair(7, 1), Pair(1, 2))
  var product: Long = 1
  for (slope in slopes) {
    val count = count_trees(slope.first, slope.second, lines)
    product *= count
  }
  println(product)
}
