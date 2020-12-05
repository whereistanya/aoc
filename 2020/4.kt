// Advent of code 2020 day 4
import java.io.File

class Passport() {
  val attributes: MutableMap<String, String> = mutableMapOf<String, String>()
  val required: List<String> = listOf<String>("byr", "iyr", "eyr", "hgt", "hcl",
  "ecl", "pid")
  val eyecolors: Set<String> = setOf<String>("amb", "blu", "brn", "gry", "grn", "hzl", "oth")

  fun set_attribute(k:String, v:String) {
    // println("Adding $v to $k")
    this.attributes[k] = v
  }

  fun validate(): Boolean {
    var validatefns: Map<String, (entry: String) -> Boolean> =
      mapOf<String, (entry: String) -> Boolean>(
      "byr" to { i -> this.validate_byr(i) },
      "eyr" to { i -> this.validate_eyr(i) },
      "iyr" to { i -> this.validate_iyr(i) },
      "hgt" to { i -> this.validate_hgt(i) },
      "hcl" to { i -> this.validate_hcl(i) },
      "ecl" to { i -> this.validate_ecl(i) },
      "pid" to { i -> this.validate_pid(i) },
      "cid" to { i -> this.validate_cid(i) },
      )

    for (req in this.required) {
      if (! this.attributes.containsKey(req)) {
        return false
      }
    }
    for ((k, v) in this.attributes) {
      if (validatefns.containsKey(k)) {
        val fn = validatefns[k]
        if (fn?.invoke(v) == false) {
          return false
        }
      }
    }
    return true
  }

  fun runTests() {

    assert (this.validate_byr("2002") == true)
    assert (this.validate_byr("2003") == false)
    assert (this.validate_hgt("60in") == true)
    assert (this.validate_hgt("190cm") == true)
    assert (this.validate_hgt("190in") == false)
    assert (this.validate_hgt("190") == false)
    assert (this.validate_hcl("#123abc") == true)
    assert (this.validate_hcl("#123abz") == false)
    assert (this.validate_hcl("123abc") == false)
    assert (this.validate_ecl("brn") == true)
    assert (this.validate_ecl("wat") == false)
    assert (this.validate_pid("000000001") == true)
    assert (this.validate_pid("0123456789") == false)
  }

  private fun validate_byr(entry: String): Boolean {
    val year = entry.toInt()
    if (year >= 1920 && year <= 2002) {
      return true
    }
    return false
  }
  private fun validate_iyr(entry: String): Boolean {
    val year = entry.toInt()
    if (year >= 2010 && year <= 2020) {
      return true
    }
    return false
  }
  private fun validate_eyr(entry: String): Boolean {
    val year = entry.toInt()
    if (year >= 2020 && year <= 2030) {
      return true
    }
    return false
  }
  private fun validate_hgt(entry: String): Boolean {
    if (entry.endsWith("cm") == false && entry.endsWith("in") == false) {
      return false
    }
    val unit = entry.takeLast(2)
    val height = entry.dropLast(2).toInt()
    if (unit == "cm" && height >= 150 && height <= 193) {
      return true
    }
    if (unit == "in" && height >= 59 && height <= 76) {
      return true
    }
    return false
  }
  private fun validate_hcl(entry: String): Boolean {
    if (entry[0] != "#".single()) {
      return false
    }
    for (char in entry.substring(1)) {
      if (char.isDigit() || char in "a".single().."f".single()) {
        return true
      }
    }
    return false
  }
  private fun validate_ecl(entry: String): Boolean {
    if (this.eyecolors.contains(entry)) {
      return true
    }
    return false
  }

  private fun validate_pid(entry: String): Boolean {
    if (entry.length != 9) {
      return false
    }
    for (char in entry) {
      if (char.isDigit() == false) {
        return false
      }
    }
    return true
  }
  private fun validate_cid(@Suppress("UNUSED_PARAMETER") entry: String): Boolean {
    return true
  }
}

fun main() {
  val fileName = "input4.txt"
  val lines: List<String> = File(fileName).readLines()

  val passports: MutableList<Passport> = mutableListOf<Passport>()

  var current = Passport()
  current.runTests()

  passports.add(current)
  for (line: String in lines) {
    if (line == "") {
      current = Passport() // Does this new?
      passports.add(current)
      continue
    }
    val fields = line.split(" ")
    for (field in fields) {
      val attribute = field.split(":")
      // println("Attributes! $attribute")
      current.set_attribute(attribute[0], attribute[1])
    }
  }
  var count = 0
  for (passport in passports) {
    if (passport.validate()) {
      count += 1
    }
  }

 println("$count are valid")
}
