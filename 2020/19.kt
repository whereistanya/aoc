// Advent of code 2020 day 19
import java.io.File

import kotlin.system.exitProcess

class Rule(name: String) {
  val name = name
  var matchString = ""
  var matched = mutableMapOf<String, Boolean>()
  var matches = mutableListOf<List<Rule>>()
  var letter:String = ""
  var found = mutableListOf<String>()

  fun generateMatches(): List<String> {
    //println("Generating matches for $name")
    if (letter != "") {
      return listOf<String>(letter)
    }
    var found = mutableListOf<String>()
    for (ruleGroup in matches) {
      if (ruleGroup.size == 1) {
        // 8: 42 | 42 8
        //if (this.name == '8')
        // Add this same thing a bunch of times
        for (i in ruleGroup[0].generateMatches()) {
          found.add(i)
        }
        continue
      }
      val first = ruleGroup[0]
      val second = ruleGroup[1]

      var firstMatches = first.generateMatches()
      var secondMatches = second.generateMatches()

      for (i in firstMatches) {
        for (j in secondMatches) {
          var s: String = "$i$j"
          // if (this.name == "11") {
          found.add(s)
          //println(s)
        }
      }
    }
    return found.toList()
  }

  fun match(word: String): Boolean {
    //println("Does $word match rule $name ($matches)?")
    if (this.matched.containsKey(word)) {
      //println("Returned ${this.matched[word]!!} from cache!")
      return this.matched[word]!!
    }
    //println("$word isn't cached. Matching against ${matches}")
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
        //println("Only matches one: recursing")
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
          //println("${word.substring(0, pieceSize)} matches $name!")
          if (second.match(word.substring(pieceSize))) {
            this.matched[word] = true
            //println("${word.substring(pieceSize)} also matches $name!")
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
    //return "[$name :Matches: ${matches.size} rules.Matched ${matched} strings.]"
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

  for (line in lines) {
    if (line.contains(":")) {
      // It's a rule!
      val pieces = line.split(":")
      val rule = rules.getOrPut(pieces.first()) { Rule(pieces.first()) }
      rule.matchString = pieces.last() // Just used for debugging.
      println(rule.matchString)
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
        println("Rulegroup: $ruleGroup")
        if (! ruleGroup.isEmpty()) {
          rule.matches.add(ruleGroup)
        }
      }
    } else if (line != "") {
      words.add(line)
    }
  }
  var count1 = 0
  var count2 = 0
  var zerothRule = rules["0"]!!
  var matched = zerothRule.generateMatches()

  for (word in words) {
    var match1 = false
    var match2 = false

    if (zerothRule.match(word)) {
      match1 = true
      count1 += 1
    }
    if (word in matched) {
      match2 = true
      count2 += 1
    }
    if (match1 != match2) {
      println("Bad: $word, $match1, $match2")
    } else {
      println("Good: $word, $match1, $match2")
    }
  }
  println("There were $count1 or $count2 matches")
}