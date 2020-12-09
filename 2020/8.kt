// Advent of code 2020 day 8
import java.io.File
import java.lang.*

class Computer() {
  var accumulator = 0
  var code = mutableListOf<Pair<String, Int>>()
  var original_code = listOf<Pair<String, Int>>()

  fun load_code(lines: MutableList<String>) {
    this.accumulator = 0
    for (line in lines) {
      var pieces = line.split(" ")
      var op = pieces[0]
      var count = pieces[1]
      var number:Int
      if (count.startsWith("+")) {
        number = count.substring(1).toInt()
      } else {
        number = count.toInt()
      }
      this.code.add(Pair(op, number))
    }
    this.original_code = this.code.toList()
  }

  fun run(): Boolean {
    var i = 0
    var seen = mutableSetOf<Int>()
    while (true) {
      if (i >= this.code.size) {
        println("Normal completion! Accumulator is ${this.accumulator}")
        return true
      }
      if (i in seen) {
        println("Loop detected. Accumulator is ${this.accumulator}")
        return false
      }
      seen.add(i)
      val op = this.code[i].first
      val arg = this.code[i].second
      if (op == "acc") {
        this.accumulator += arg
        i += 1
      } else if (op == "jmp") {
        i += arg
      } else if (op == "nop") {
        i += 1
      }
    }
  }

  fun mutate_and_run() {
    var i = 0
    while (true) {
      this.accumulator = 0
      var modified = false
      if (this.code[i].first == "jmp") {
        this.code[i] = Pair<String, Int>("nop", this.code[i].second)
        modified = true
      } else if (this.code[i].first == "nop") {
        this.code[i] = Pair<String, Int>("jmp", this.code[i].second)
        modified = true
      }
      i += 1

      if (modified) {
        val ok = this.run()
        if (ok) {
          println("Yay we're done")
          return
        } else {
          println("RESET")
          this.code = this.original_code.toMutableList()
        }
      }
    }
  }
}


fun main() {
  val fileName = "input8.txt"
  val lines: MutableList<String> = File(fileName).readLines().toMutableList()

  val computer = Computer()
  computer.load_code(lines)

  // Part 1
  computer.run()

  // Part 2
  computer.mutate_and_run()
}
