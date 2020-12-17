// Advent of code 2020 day 17
import java.io.File

class Cube(lines: List<String>) {
  var points = mutableMapOf<Triple<Int, Int, Int>, Char>()
  var minX = 0
  var maxX = lines[0].length
  var minY = 0
  var maxY = lines.size
  var minZ = -1
  var maxZ = 1

  init {
    for (x in (minX..maxX - 1)) {
      for (y in (minY..maxY - 1)) {
        val z = 0  // 2-dimensional to start.
        this.points[Triple<Int, Int, Int>(x, y, z)] = lines[y][x]
      }
    }
  }

  fun printSlice(z: Int) {
    var s = "z = $z\n"
    println(s)
    for (y in ((minY - 1)..(maxY + 1))) {
      s = ""
      for (x in ((minX - 1)..(maxX + 1))) {
        s += (this.points[Triple(x, y, z)] ?: ".")
      }
      println(s)
    }
  }

  fun countActiveNeighbours(point: Triple<Int, Int, Int>): Int {
    var myx = point.first
    var myy = point.second
    var myz = point.third
    val livingNeighbours = this.points.filterKeys {
      ((it != point) and                  // exclude self
      (Math.abs(it.first - myx) <= 1) and
      (Math.abs(it.second - myy) <= 1) and
      (Math.abs(it.third -  myz) <= 1)) }.filterValues {
        it == '#'
      }
    //println("Living neighbours of $point are $livingNeighbours")
    return livingNeighbours.size
  }

  fun iterate() {
    minX -= 1
    minY -= 1
    minZ -= 1
    maxX += 1
    maxY += 1
    maxZ += 1
    val newPoints = mutableMapOf<Triple<Int, Int, Int>, Char>()
    for (x in (this.minX)..(this.maxX)) {
      for (y in (this.minY)..(this.maxY)) {
        for (z in (this.minZ)..(this.maxZ)) {
          if (!this.points.containsKey(Triple<Int, Int, Int>(x, y, z))) {
            this.points[Triple<Int, Int, Int>(x, y, z)] = '.'
     //       println("Adding point $x, $y, $z")
          }
        }
      }
    }
    for ((point, state) in this.points) {
      var newState = state
      // Check all neighbours
      var sum = countActiveNeighbours(point)
      //println("$sum of $point neighbours were alive")

      if ((state == '#') and (sum !in (2..3))) { // kotlin ranges are inclusive
        newState = '.'
      } else if ((state == '.') and (sum == 3)) {
        newState = '#'
      }
      newPoints[point] = newState
    }
    this.points = newPoints
  }
}

fun main() {
  val fileName = "input17.txt"
  var lines: List<String> = File(fileName).readLines()

/*
  lines = mutableListOf(
    ".#.",
    "..#",
    "###",
  )*/

  val cube = Cube(lines)
  cube.printSlice(0)

  for (i in 1..6) {
    cube.iterate()
  }
  var sum = cube.points.filterValues { it == '#' }.count()
  println(sum)
  
/*
cube.printSlice(-1)
  cube.printSlice(0)
  cube.printSlice(1)
  println()

  cube.iterate()
  cube.printSlice(-2)
  cube.printSlice(-1)
  cube.printSlice(0)
  cube.printSlice(1)
  cube.printSlice(2)
  println()

  cube.iterate()
  cube.printSlice(-2)
  cube.printSlice(-1)
  cube.printSlice(0)
  cube.printSlice(1)
  cube.printSlice(2)
  println()
*/
  

  /*
  for (i in 0..6) {
    var newLines = mutableListOf<String>()

    for (line in lines) {
      newLines.add(line)
    }
    lines = newLines
    println(lines)
    println()
  }*/

}
