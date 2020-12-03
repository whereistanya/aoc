// Advent of code 2020 day 2
import java.io.File

fun main() {
  val inputfile = "input2.txt"
  val lines: List<String> = File(inputfile).readLines()

  var valid1 = 0
  var valid2 = 0

  for (line: String in lines) {
    val parts: List<String> = line.split(" ") //.toList()
    val rule = parts[0]
    val letter: Char = parts[1].replace(":", "").single()
    val password = parts[2]

    val constraints: List<String> = rule.split("-")
    val lmin: Int = constraints[0].toInt()
    val lmax: Int = constraints[1].toInt()
    val count: Int = password.filter{ it == letter }.count()
    // println("$lmin, $lmax, $count, $letter, $password")

    // Part 1
    if (count >= lmin && count <= lmax) {
      valid1 += 1
    }

    // Part 2
    if ((password[lmin - 1] == letter) xor (password[lmax - 1] == letter)) {
      valid2 += 1
    }
  }

  println("$valid1, $valid2")
}
