// Advent of code 2020 day 19
import java.io.File

import kotlin.system.exitProcess

class Rule(name: String) {
  val name = name
  var matchString = ""
  var matched = mutableMapOf<String, Boolean>()
  var matches = mutableListOf<List<Rule>>()


  fun match(word: String): Boolean {
    println("Does $word match rule $name ($matches)?")
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
      if (ruleGroup.size == 1) {
        return ruleGroup[0].match(word)
      }
      if (ruleGroup.size > 2) {
        println("ERROR: expected to match only 2, got ${ruleGroup.size}:")
        println("$ruleGroup}")
        exitProcess(1)
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

///*
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
//*/

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
  var count = 0
  var zerothRule = rules["0"]!!
  for (word in words) {
    if (zerothRule.match(word)) {
      println("$word matches!")
      count += 1
    } else {
      println("$word doesn't match!")
    }
  }
  println("There were $count matches")

}
