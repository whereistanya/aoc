// Advent of code 2020
import java.io.File


enum class Direction(val value: Int) {
    NORTH(0),
    EAST(1),
    SOUTH(2),
    WEST(3),
}

enum class Rotation(val value: Int) {
  LEFT(0),
  RIGHT(1),
}

class Location() {
  var x: Int = 0
  var y: Int = 0
  var direction: Direction = Direction.EAST

  fun forward(distance: Int) {
    this.move(this.direction, distance)
  }

  fun move(direction: Direction, distance: Int) {
    // North is positive y
    val moves = mapOf<Direction, Pair<Int, Int>>(
      Direction.NORTH to Pair<Int, Int>(0, 1),
      Direction.EAST to Pair<Int, Int>(1, 0),
      Direction.SOUTH to Pair<Int, Int>(0, -1),
      Direction.WEST to Pair<Int, Int>(-1, 0),
    )

    val (x, y) = moves[direction]!!
    this.x += (distance * x)
    this.y += (distance * y)
  }

  fun rotate(rotation: Rotation, degrees: Int) {
    var dir = this.direction.value
    val turns = degrees / 90
    if (rotation == Rotation.LEFT) {
      dir = ((dir + 4) - turns) % 4
    } else if (rotation == Rotation.RIGHT) {
      dir = (dir + turns) % 4
    }
    this.direction = Direction.values()[dir]
  }

  fun rotateAround(rotation: Rotation, degrees: Int) {
    var turns = degrees / 90
    if (rotation == Rotation.LEFT) {
      turns = 4 - turns
    }
    var x = this.x
    var y = this.y
    var tmp: Int
    for (turn in (1..turns)) {
      tmp = x
      x = y
      y = tmp * -1
    }
    this.x = x
    this.y = y
  }

  fun manhattanDistanceFrom(x: Int, y: Int): Int {
    return (Math.abs(x - this.x) + Math.abs(y - this.y))
  }


}

fun main() {
  val fileName = "input12.txt"
  val lines: List<String> = File(fileName).readLines()


  val directions = mapOf<Char, Direction>(
    'N' to Direction.NORTH,
    'E' to Direction.EAST,
    'S' to Direction.SOUTH,
    'W' to Direction.WEST
  )
  val boat = Location()
  val waypoint = Location() // The waypoint's location is always relative to the
                            // boat's.

  // Part 1
  for (line in lines) {
    var letter = line[0]
    var number = line.substring(1).toInt()
    if (letter == 'F') {
      boat.forward(number)
    } else if (letter == 'R') {
      boat.rotate(Rotation.RIGHT, number)
    } else if (letter == 'L') {
      boat.rotate(Rotation.LEFT, number)
    } else {
      boat.move(directions[letter]!!, number)
    }
  }
  println("Part 1: x: ${boat.x}, y: ${boat.y} --> ${boat.manhattanDistanceFrom(0, 0)}")

  // Part 2
  boat.x = 0
  boat.y = 0
  boat.direction = Direction.EAST
  waypoint.x = 10
  waypoint.y = 1

  for (line in lines) {
    var letter = line[0]
    var number = line.substring(1).toInt()
    if (letter == 'F') {
      // Move to the waypoint N time (the waypoint has a relative distance so
      // stays the same distance away)
      for (i in (1..number)) {
        boat.x += waypoint.x
        boat.y += waypoint.y
      }
    } else if (letter == 'R') {
      waypoint.rotateAround(Rotation.RIGHT, number)
    } else if (letter == 'L') {
      waypoint.rotateAround(Rotation.LEFT, number)
    } else {
      // The waypoint moves but the ship doesn't.
      waypoint.move(directions[letter]!!, number)
    }
  }
  println("Part 2: x: ${boat.x}, y: ${boat.y} --> ${boat.manhattanDistanceFrom(0, 0)}")

}
