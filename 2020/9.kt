// Advent of code 2020 day 9
import java.io.File

fun main() {
  //println(Int.MAX_VALUE)
  val fileName = "input9.txt"
  val numbers: List<Long> = File(fileName).readLines().map { it.toLong() }

  val preamble = 25

  val active = mutableSetOf<Long>()
  var i = 0
  while (i < preamble) {
    active.add(numbers[i])
    i += 1
  }

  // Part 1: find the invalid number
  var invalid: Long

  while (true) {
    val next_number: Long = numbers[i]
    var found = false
    for (number: Long in numbers.subList(i - preamble, i)) {
      val required: Long = next_number - number
      if (active.contains(required)) {
        found = true
        break
      }
    }
    if (!found) {
      invalid = next_number
      break
    }
    active.add(next_number)
    active.remove(numbers[i - preamble])
    i += 1
  }

  println("Part 1: $invalid")

  // Part 2: find contiguous numbers that add to the invalid number
  i = 0 // the start of the string of numbers

  var found = false
  var smallest = -1
  var biggest = -1
  while (!found) {
    var j = i + 1 // the index inside the string of numbers
    var total = numbers[i] + numbers[j]

    while (total <= invalid) {
      if (total == invalid) {
        println("Got it! ${ numbers.subList(i, j + 1)}")
        smallest = i
        biggest = j
        found = true
        break
      }
      j += 1
      total += numbers[j]
    }
    // if we get to here, we went over the number we're looking for
    i += 1
  }

  val contiguous = numbers.subList(smallest, biggest + 1).sorted()
  println("Part 2: ${contiguous[0] + contiguous.last()}")
}


