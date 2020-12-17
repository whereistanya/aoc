// Advent of code 2020 day 17
import java.io.File

data class Point(var x: Int, var y: Int, var z: Int, var a: Int) {}

class Cube(lines: List<String>) {
  var points = mutableMapOf<Point, Char>()
  var minX = 0
  var maxX = lines[0].length
  var minY = 0
  var maxY = lines.size
  var minZ = -1
  var maxZ = 1
  // Part 2
  var minA = -1
  var maxA = 1
  

  init {
    for (x in (minX..maxX - 1)) {
      for (y in (minY..maxY - 1)) {
        val z = 0  // 2-dimensional to start.
        val a = 0
        this.points[Point(x, y, z, a)] = lines[y][x]
      }
    }
  }

  fun printSlice(z: Int) {
    var s = "z = $z\n"
    println(s)
    for (y in ((minY - 1)..(maxY + 1))) {
      s = ""
      for (x in ((minX - 1)..(maxX + 1))) {
        s += (this.points[Point(x, y, z, 0)] ?: ".")
      }
      println(s)
    }
  }

  fun countActiveNeighbours(point: Point): Int {
    var myx = point.x
    var myy = point.y
    var myz = point.z
    var mya = point.a
    val livingNeighbours = this.points.filterKeys {
      ((it != point) and                  // exclude self
      (Math.abs(it.x - myx) <= 1) and
      (Math.abs(it.y - myy) <= 1) and
      (Math.abs(it.z - myz) <= 1) and
      (Math.abs(it.a -  mya) <= 1)) }.filterValues {
        it == '#'
      }
    //println("Living neighbours of $point are $livingNeighbours")
    return livingNeighbours.size
  }

  fun iterate(part: Int = 2) {
    minX -= 1
    minY -= 1
    minZ -= 1
    minA -= 1
    maxX += 1
    maxY += 1
    maxZ += 1
    maxA += 1

    //maxA = 0
    //maxA = 0

    val newPoints = mutableMapOf<Point, Char>()
    val toCheck = mutableListOf<Point>()
    for (x in (this.minX)..(this.maxX)) {
      for (y in (this.minY)..(this.maxY)) {
        for (z in (this.minZ)..(this.maxZ)) {
          if (part == 1) {
            toCheck.add(Point(x, y, z, 0))
          } else {
            for (a in (this.minA)..(this.maxA)) {
              toCheck.add(Point(x, y, z, a))
            }
          }
        }
      }
    }
    for (point in toCheck) {
      var state = points[point] ?: '.'
      var newState = state
      // Check all neighbours
      var sum = countActiveNeighbours(point)
      //println("$sum of $point neighbours were alive")

      if ((state == '#') and (sum !in (2..3))) { // kotlin ranges are inclusive
        newState = '.'
      } else if ((state == '.') and (sum == 3)) {
        newState = '#'
      }
      if (newState == '#') {
        newPoints[point] = newState
      }
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

  val part = 1
  for (i in 1..6) {
    cube.iterate(part=part)
  }
  var sum = cube.points.filterValues { it == '#' }.count()
  println("Part $part: $sum")

}
