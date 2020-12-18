// Advent of code 2020
import java.io.File

fun main() {
  var fileName = "input18.txt"
  var lines: List<String> = File(fileName).readLines()

  // Need to run with -ea (e.g., java -ea -jar aoc.jar) to enable assertions!
  assert (doMath("1 + (2 * 3) + (4 * (5 + 6))", 2) == 51L)
  assert (doMath("2 * 3 + (4 * 5)", 2) == 46L)
  assert (doMath("5 + (8 * 3 + 9 + 3 * 4 * 3)", 2) == 1445L)
  assert (doMath("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 2) == 669060L)
  assert (doMath("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 2) == 23340L)
  println("TESTS PASSED")

  val part = 2  // Change to 1 for part 1!
  var total = 0L
  for (line in lines) {
     total += doMath(line, part)
  }
  println("Part $part: $total")
}

fun doMath(line: String, part: Int): Long {
  var list = line.replace(" ", "").toMutableList()
  var i = 0
  if (part == 2) {
    while (i < list.size - 1) {
      if (list[i] == '+') {
        parenSurround(list, i)
        i += 1 // Move past the character we just added.
      }
      i += 1
    }
  }
  return evaluate(list)
}



fun parenSurround(line: MutableList<Char>, index: Int) {
  //Write parens around the units before and after this operator.
  // Mutates the list passed to it.

  // Go backwards to find the open.
  var openParen = index - 1
  if (line[index - 1] in '0'..'9') {
    openParen = index - 1
  } else {
    if (line[index - 1] != ')') {
      println("ERROR: index ${index - 1} expected ), got ${line[index - 1]}")
    }
    var parenCount = 1
    while (openParen >= 0) {
      openParen -= 1
      var found = line[openParen]
      if (found == '(') {
        parenCount -= 1
      }
      if (found == ')') {
        parenCount += 1
      }
      if (parenCount == 0) {
        break
      }
    }
  }
  // Now go forward to find the close
  var closeParen = index + 1
  if (line[index + 1] in '0'..'9') {
    // Just write a paren there.
    closeParen = index + 1
  } else {
    if (line[index + 1] != '(') {
      println("ERROR: index ${index + 1}  expected (, got ${line[index + 1]}")
    }
    var parenCount = 1
    while (closeParen < line.size) {
      closeParen += 1
      var found = line[closeParen]
      if (found == '(') {
        parenCount +=1
      }
      if (found == ')') {
        parenCount -= 1
      }
      if (parenCount == 0) {
        break
      }
    }
  }
  line.add(closeParen + 1, ')')
  line.add(openParen, '(')
}


fun evaluate(line: List<Char>): Long {
  var total = 0L
  var next_operator = '+'
  var i = 0
  while (i < line.size) {
    val c = line[i]
    var digit = Character.getNumericValue(c).toLong()
    if (c in '0'..'9') {
 	    total = op(total, next_operator, digit)
    } else if ((c == '+') or (c == '*')) {
      next_operator = c
    } else if (c == '(') {
      // continue to closing paren
      var parenCount = 1
      var toIndex = i + 1
      while (toIndex < line.size) {
        var found = line[toIndex]
        if (found == '(') {
          parenCount += 1
        }
        if (found == ')') {
          parenCount -=1
        }
        if (parenCount == 0) {
          break
        }
        toIndex += 1
      }
      total = op(total, next_operator, evaluate(line.subList(i + 1, toIndex)))
      i = toIndex
    }
    // skip spaces, also don't need to handle ')s' because they're included in
    // the rules for '('.
    i += 1
  }
  return total
}

fun op(i: Long, op: Char, j: Long): Long {
  if (op == '+') {
    return (i + j)
  } else if (op == '*') {
   return (i * j)
  }
  println("ERROR: unexpected operator")
  return 0
}
