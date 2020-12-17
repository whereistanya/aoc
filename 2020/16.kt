// Advent of code 2020 day 16
import java.io.File
import kotlin.system.exitProcess


class Constraint(desc: String) {
  var validRanges = mutableListOf<Pair<Int, Int>>()  // min, max
  init {
    for (range in desc.split(" or ")){
      // Turning a list of two things into a pair. Is this idiomatic or just
      // unreadable?
      validRanges.add(range.split("-").map{ it.toInt() }.zipWithNext().first())
    }
    println("Made constraint: $validRanges")
  }

  fun validate(value: Int): Boolean {
    for (range in validRanges) {
      // It'd be easier to do a set here but I suspect we'll want these distinct
      // ranges for part two.
      if ((value >= range.first) and (value <= range.second)) {
        return true
      }
    }
    return false
  }

  fun validate(values: List<Int>): Boolean {
    for (value in values) {
      if (! this.validate(value)) {
        return false
      }
    }
    return true
  }
}

class TicketValidator() {
  var constraints = mutableMapOf<String, Constraint>()

  fun addConstraint(field: String, ranges: String) {
    println("Adding Constraint: $field -> $ranges")
    this.constraints[field] = Constraint(ranges)
  }

  fun validateFitsAnyField(value: Int): Boolean {
    for (constraint in constraints.values) {
      if (constraint.validate(value)) {
        return true
      }
    }
    return false
  }
}

class Ticket(fields: List<Int>) {
  var values = fields
  var valid = true
}

fun main() {
  val fileName = "input16.txt"
  var lines: List<String> = File(fileName).readLines()
  /*
  lines = listOf<String>(
    "class: 1-3 or 5-7",
    "row: 6-11 or 33-44",
    "seat: 13-40 or 45-50",
    "",
    "your ticket:",
    "7,1,14",
    "",
    "nearby tickets:",
    "7,3,47",
    "40,4,50",
    "55,2,20",
    "38,6,12",
  )
  lines = listOf<String>(
    "class: 0-1 or 4-19",
    "row: 0-5 or 8-19",
    "seat: 0-13 or 16-19",
    "",
    "your ticket:",
    "11,12,13",
    "",
    "nearby tickets:",
    "3,9,18",
    "15,1,5",
    "5,14,9",
  )
  */

  val validator = TicketValidator()
  var myTicket = Ticket(listOf<Int>())
  val nearbyTickets = mutableListOf<Ticket>()

  var typeIndex = 0
  for (line in lines) {
    if (line == "") {
      typeIndex += 1
    } else if (typeIndex == 0) {
      // Fields.
      var pieces = line.split(":").map { it.trim() }
      validator.addConstraint(pieces.first(), pieces.last())
    } else if (typeIndex == 1) {
      // My ticket.
      if (line == "your ticket:") { continue }
      println("myticket: $line")
      myTicket.values = line.split(",").map{ it.toInt() }
    } else if (typeIndex == 2) {
      // Other tickets.
      if (line == "nearby tickets:") { continue }
      println("nearby: $line")
      var fields = line.split(",").map{ it.toInt() }
      nearbyTickets.add(Ticket(fields))
    } else {
      // Error.
      println("ERROR in input validation")
      exitProcess(1)
    }
  }

  println("My ticket is: ${myTicket.values}")

  // Part one
  var sum = 0
  for (ticket in nearbyTickets) {
    for (value in ticket.values) {
      if (!validator.validateFitsAnyField(value)) {
        println("INVALID: $value")
        sum += value
        ticket.valid = false
      }
    }
  }
  println(sum)

  // Part 2
  val valuesForField = mutableMapOf<Int, MutableList<Int>>()
  for (ticket in nearbyTickets) {
    if (! ticket.valid) {
      continue
    }
    var fields = ticket.values
    for (i in (0..(fields.size - 1))) {
      if (!valuesForField.contains(i)) {
        valuesForField[i] = mutableListOf<Int>()
      }
      valuesForField[i]!!.add(fields[i])
    }
  }

  println(valuesForField)
  var possibleForField = mutableMapOf<String, MutableList<Int>>()
  for ((fieldName, constraints) in validator.constraints) {
    possibleForField[fieldName] = mutableListOf<Int>()
    for ((mysteryField, values) in valuesForField) {
      if (constraints.validate(values)) {
        possibleForField[fieldName]!!.add(mysteryField)
      } else {
        //println("Field $mysteryField couldn't be $fieldName")
        //println("Because $values didn't match ${constraints.validRanges}")
      }
    }
  }

  val actualForField = mutableMapOf<String, Int>()
  var toFind = possibleForField.size
  while (toFind > 0) {
    for ((field, possible) in possibleForField) {
      if (possible.size != 1) {
        continue
      }
      val actualFieldValue = possible.single()
      actualForField[field] = actualFieldValue
      toFind -= 1
      for ((k, v) in possibleForField) {
        var tmp = v
        tmp.remove(actualFieldValue)
        possibleForField[k] = tmp
      }
    }
  }
  println(actualForField)

  var result = 1L
  for ((fieldName, fieldIndex) in actualForField) {
    if (fieldName.startsWith("departure")) {
      result *= myTicket.values[fieldIndex]
    }
  }
  println("Part two: $result")
}
