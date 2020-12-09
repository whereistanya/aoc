// Advent of code 2020 day 7
import java.io.File

class Bag(name: String) {
    var name = name
    var contains = mutableMapOf<String, Int>() // {str: count}
}

fun main() {
  val fileName = "input7.txt"
  val lines: List<String> = File(fileName).readLines()

  var bags = mutableMapOf<String, Bag>()
  for (line in lines) {
    val pieces = line.replace("bags", "").replace("bag", "").replace(".", "").trim().split(" contain ")
    val outer_name = pieces[0].trim()
    val contained = pieces[1]
    var outer_bag: Bag
    if (bags.containsKey(outer_name)) {
      outer_bag = bags[outer_name]!!
    } else {
      outer_bag = Bag(outer_name)
      bags[outer_name] = outer_bag
    }

    val inners = contained.split(",").map { it.trim() }
    for (inside in inners) {
      if (inside == "no other") {
        continue
      }
      val first:String = inside.split(" ")[0].trim()
      val bag_name:String = inside.substring(first.length).trim()
      if (!bags.containsKey(bag_name)) {
        bags[bag_name] = Bag(bag_name)
      }
      outer_bag.contains[bag_name] = first.toInt()
    }
  }
  // Part one
  var can_reach_gold = mutableSetOf("shiny gold")

  for (bag in bags.values) {
    look_inside(bag, bags, can_reach_gold)
  }

  // Part 1
  println("Part 1: ${can_reach_gold.size - 1}")

  // Part two
  val bag_count = count_inside(bags["shiny gold"]!!, bags)
  println("Part 2: $bag_count bags")
}

fun count_inside(outer: Bag, bags: Map<String, Bag>): Int {
  if (outer.contains.size == 0) {
    return 0
  }
  var count = 0
  for ((bag, number) in outer.contains) {
    count += number
    count += (number * count_inside(bags[bag]!!, bags))
  }
  return count
}


fun look_inside(outer: Bag, bags: Map<String, Bag>, can_reach_gold: MutableSet<String>): Boolean {
  if (outer.name in can_reach_gold) {
    return true
  }
  for (bag_name in outer.contains.keys) {
    val bag = bags[bag_name]!!
    if (look_inside(bag, bags, can_reach_gold)) {
      can_reach_gold.add(outer.name)
      return true
    }
  }
  return false
}


