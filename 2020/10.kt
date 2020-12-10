// Advent of code 2020 day 10
import java.io.File

fun main() {
  val fileName = "input10.txt"
  var lines: MutableList<Int> = File(fileName).readLines().map { it.toInt() }.sorted().toMutableList()

  // Test data
  //lines = mutableListOf<Int>(16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4).sorted().toMutableList()
  //lines = mutableListOf<Int>(28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24,
  //                           23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8,
  //                           17, 7, 9, 4, 2, 34, 10, 3).sorted().toMutableList()

  lines.add(0, 0) // Prepend a zero for the charging outlet.
  lines.add(lines.last() + 3) // Append the device adapter.

  // Part 1
  var count1 = 0
  var count3 = 0
  var prev = 0
  for (line in lines) {
    if (line == prev) {
      // Inelegantly handling the "wall outlet" zero case.
      continue
    }
    val gap = line - prev
    if (gap == 1) {
      count1 ++
    } else if (gap == 3) {
      count3 ++
    } else {
      println("ERROR: Unexpected gap between $prev and $line")
    }
    prev = line
  }
  val answer = count1 * count3
  println ("Part 1: $answer")

  // Part 2
  println("Part 2: " + countPermutations(0, lines, mutableMapOf<Int, Long>()))
}


fun countPermutations(pos: Int, ordered: List<Int>, found: MutableMap<Int, Long>): Long {
  // pos: index into the list. Points to the last thing we connected.
  // ordered: sorted list
  // found: for memoization: counts from places we've already been
  // Returns count from here
    if (found.containsKey(pos)) {
    // We've been here before!
    return found.get(pos)!!
  }
  // Base case: nothing else to add
  if (pos == ordered.size - 1) {
    return 1
  }
  // Otherwise, add the number of permutations on each path from here
  var count: Long = 0
  var i = pos + 1
  // Next link can be anything within three units.
  while ((i < ordered.size) && (ordered[i] - ordered[pos]) <= 3) {
    count += countPermutations(i, ordered, found)
    i += 1
  }
  found[pos] = count
  return count
}
