// Advent of code 2020 day 19
import java.io.File

import kotlin.system.exitProcess

class Rule(name: String) {
  val name = name
  var matchString = ""
  var matched = mutableMapOf<String, Boolean>()
  var matches = mutableListOf<List<Rule>>()
  var letter:String = ""
  var found = mutableSetOf<String>()

  // Approach 1: generate all possible values. Also used in approach 3.
  fun generateMatches(): MutableSet<String> {
    if (this.found.size > 0) {
      return this.found.toMutableSet()
    }
    if (letter != "") {
      return mutableSetOf<String>(letter)
    }
    for (ruleGroup in matches) {
      if (ruleGroup.size == 1) {
        for (i in ruleGroup[0].generateMatches()) {
          this.found.add(i)
        }
        continue
      }

      var firstMatches = ruleGroup[0].generateMatches()
      var secondMatches = ruleGroup[1].generateMatches()
      for (i in firstMatches) {
        for (j in secondMatches) {
          var s: String = "$i$j"
          found.add(s)
        }
      }
    }
    return found.toMutableSet() // to make sure it's a copy
  }

  // Approach 2: match recursively. Sure doesn't work with infinite loops.
  fun match(word: String): Boolean {
    if (this.matched.containsKey(word)) {
      return this.matched[word]!!
    }
    for (ruleGroup in matches) {
      if (word.length < ruleGroup.size) {
        //println("$word is too short for this $ruleGroup to match")
        continue
      }
      if (ruleGroup.size > 2) {
        println("ERROR: expected to match only 2, got ${ruleGroup.size}:")
        println("$ruleGroup}")
        exitProcess(1)
      }
      if (ruleGroup.size == 1) {
        if (ruleGroup[0].match(word)) {
          return true
        } else {
          continue
        }
      }
      val first = ruleGroup[0]
      val second = ruleGroup[1]

      var pieceSize = 1
      while(pieceSize < word.length) {
        if (first.match(word.substring(0, pieceSize))) {
          if (second.match(word.substring(pieceSize))) {
            this.matched[word] = true
            return true
          }
        }
        pieceSize += 1
      }
      //println("$word doesn't match group $ruleGroup")
    }
    //println("$word does not match rule $name")
    this.matched[word] = false
    return false
  }

  override fun toString(): String {
    return "[$name]"
  }
}



fun main() {
  val fileName = "input19.txt"
  var lines: List<String> = File(fileName).readLines()

/*
  lines = listOf<String>(
    "0: 4 1",
    "1: 2 3 | 3 2",
    "2: 4 4 | 5 5",
    "3: 4 5 | 5 4",
    """4: "a"""",
    """5: "b"""",
    "",
    "ababb",
    "babab",
    "abbba",
    "aaabb",
    "aaaabb"
  )
*/

  val rules = mutableMapOf<String, Rule>()
  val words = mutableListOf<String>()

  // Parse the input.
  for (line in lines) {
    if (line.contains(":")) {
      // It's a rule!
      val pieces = line.split(":")
      val rule = rules.getOrPut(pieces.first()) { Rule(pieces.first()) }
      rule.matchString = pieces.last() // Just used for debugging.
      for (x in pieces.last().split("|")) {
        var ruleGroup = mutableListOf<Rule>()
        for (ruleNumber in x.split(" ").map { it.trim() } ) {
          if (ruleNumber == "") {
            continue // Skip blank lines.
          }
          if (ruleNumber.toIntOrNull() == null) {
            // Not actually a number. Add to the list of matched strings instead.
            rule.matched[ruleNumber.replace("\"", "")] = true
            rule.letter = ruleNumber.replace("\"", "")
            continue
          }
          var matchingRule = rules.getOrPut(ruleNumber) { Rule(ruleNumber) }
          ruleGroup.add(matchingRule)
        }
        if (! ruleGroup.isEmpty()) {
          rule.matches.add(ruleGroup)
        }
      }
    } else if (line != "") {
      words.add(line)
    }
  }

  // Getting results in three ways.
  // Part 1
  var count1 = 0
  var count2 = 0
  // Part 2
  var count3 = 0

  var zerothRule = rules["0"]!!
  val fortyTwo = rules["42"]!!
  val thirtyOne = rules["31"]!!
  var matched = zerothRule.generateMatches()
  // 0: 8 11
  // 8: 42 | 42 8
  // 11: 42 31 | 42 11 31
  val fortyTwoMatches = fortyTwo.generateMatches()
  val thirtyOneMatches = thirtyOne.generateMatches()
  val baseLen = 8 // 5 for test input, 8 for real

  //println("Intersection = ${fortyTwoMatches.intersect(thirtyOneMatches)}")
  // No intersection, so if we match one, we don't match the other.


  /*
  println(fortyTwo.match("aaabbbbb"))
  println(fortyTwo.match("aaaaabbb"))
  println(fortyTwo.match("ababbabb"))
  println(fortyTwo.match("baaababa"))
  println(thirtyOne.match("aaabbbbb"))
  println(thirtyOne.match("aaaaabbb"))
  println(thirtyOne.match("ababbabb"))
  println(thirtyOne.match("baaababa"))
  */

  for (word in words.sorted()) {
    // Values for recursive matching, generate everything, 42/31s approaches.
    var match1 = false
    var match2 = false
    var match3 = false

    var count42 = 0
    var count31 = 0
    if (word.length.rem(baseLen) != 0) {
      // All of the 42/31 pieces have baseLen characters
      //println("Not a multiple of $baseLen")
      continue
    }
    var i = 0
    // some number of 42s, then an even number of 42 and 31s.

    // Consume as many 42s as possible.
    while (i < word.length) {
      if (fortyTwoMatches.contains(word.substring(i, i + baseLen))) {
      // Alternative: if (fortyTwo.match(word.substring(i, i + baseLen))) {
        i += baseLen
        count42 += 1
      } else {
        break
      }
    }

    // Then as many 31s as possible.
    while (i < word.length) {
      if (thirtyOneMatches.contains(word.substring(i, i + baseLen))) {
      // Alternative: if (thirtyOne.match(word.substring(i, i + baseLen))) {
        i += baseLen
        count31 += 1
      } else {
        break
      }
    }
    if (i != word.length) {
      //println("Didn't consume the whole string")
      continue
    }
    if (count31 >= count42) {
      //println("Need more 42s than 31s")
      continue
    }
    if (count42 == 0) {
      //println("No 42s")
      continue
    }
    if (count31 == 0) {
      //println("No 31s")
      continue
    }

    // 42/31s approach.
    count3 += 1
    match3 = true
    println(word)

    // Recursive matching approach.
    if (zerothRule.match(word)) {
      match1 = true
      count1 += 1
    }

    // Generate everything approach.
    if (word in matched) {
      match2 = true
      count2 += 1
    }

    // Values for recursive matching, generate everything, 42/31s approaches.
    println("$word, Part1: $match1, $match2, Part2: $match3")
  }
  println("There were Part1: $count1 or $count2 or Part2: $count3 matches")
}
