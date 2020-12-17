// Advent of code 2020 day 14
import java.io.File
import kotlin.math.pow
import kotlin.system.exitProcess
import java.util.Queue
import java.util.LinkedList

class MemoryBank() {
  val memory: MutableMap<Long, Long> = mutableMapOf<Long, Long>()
  var mask: Long = 0L
  var extraInput: Long = 0L
  // Part 2
  var maskPlusExtra: String = ""

  fun parseUpdateMask(line: String) {
    val maskPlusExtra = line.split("mask = ").last()
    this.maskPlusExtra = maskPlusExtra.padStart(64, '0')
    // println("Set mask to ${maskPlusExtra.padStart(64, '0')}")
    val mask = maskPlusExtra.map {
      it -> if ( it == 'X') '1' else '0'}
      .joinToString("")
    val extra = maskPlusExtra.map {
      it -> if (it == '1') '1' else '0' }
      .joinToString("")
    // println("Mask     to ${mask.padStart(64, '0')}")
    // println("Extra    is ${extra.padStart(64, '0')}")
    this.mask = mask.toLong(2)
    this.extraInput = extra.toLong(2)
  }

  fun generateAddresses(decimal: Long): List<String> {
    val mask = this.maskPlusExtra
    var binaryAddress = java.lang.Long.toBinaryString(decimal)
      .padStart(64, '0')
      .toString()
      .toCharArray()
    if (mask.length != binaryAddress.size) {
      println("ERROR: lengths didn't match ($mask vs $decimal)")
      exitProcess(1)
    }
    for (i in 0..mask.length - 1) {
      if (mask[i] == '1') {
        binaryAddress[i] = '1'
      } else if (mask[i] == 'X') {
        binaryAddress[i] = 'X'
      }
    }
    var toReturn = mutableListOf<String>()
    var addresses: Queue<CharArray> = LinkedList<CharArray>(mutableListOf(binaryAddress))
    while (addresses.size > 0) {
      var address = addresses.remove()
      val xcount = address.count{ it == 'X' }
      if (xcount == 0) {
        toReturn.add(address.joinToString(""))
        continue  // nothing back in the queue
      }
      for (i in 0..mask.length - 1) {
        if (address[i] == 'X') {
          address[i] = '0'
          addresses.add(address)
          address = address.copyOf()
          address[i] = '1'
          addresses.add(address)
        }
      }
    }
    return toReturn
  }

  fun parseUpdateMemSetV2(line: String) {
    // A version 2 decoder chip doesn't modify the values being written at all.
    // It's modifying the addresses.
    val pieces = line.split(" = ")
    val address = pieces.first().substring(4).dropLast(1).toLong()
    val value = pieces.last().toLong()

    val addresses = generateAddresses(address)
    for (x in addresses) {
      this.memory[x.toLong(2)] = value
    }
  }

  fun parseUpdateMemSetV1(line: String) {
    val pieces = line.split(" = ")
    val address = pieces.first().substring(4).dropLast(1).toLong()  // decimal
    val input: Long = pieces.last().toLong() // Used as binary
    // (input & mask) | extraInput
    // println("Input    is ${java.lang.Long.toBinaryString(input).padStart(64, '0')}")
    // println("Extra    is ${java.lang.Long.toBinaryString(extraInput).padStart(64, '0')}")
    val value = (input and this.mask) or (this.extraInput)
    this.memory[address] = value
  }

}

fun main() {
  val fileName = "input14.txt"
  var lines: List<String> = File(fileName).readLines()
/*
  lines = listOf<String>(
    "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
    "mem[8] = 11",
    "mem[7] = 101",
    "mem[8] = 0",
  )
  lines = listOf<String>(
  "mask = 000000000000000000000000000000X1001X",
  "mem[42] = 100",
  "mask = 00000000000000000000000000000000X0XX",
  "mem[26] = 1",
  )
*/

  // Part1
  var memorybank = MemoryBank()

  for (line in lines) {
    if (line.startsWith("mask = ")) {
      memorybank.parseUpdateMask(line)
    } else if (line.startsWith("mem")) {
      memorybank.parseUpdateMemSetV1(line)
    }
  }

  var sum = 0L
  for (v in memorybank.memory.values) {
    sum += v
  }
  println("Part 1: $sum")

  // Part2
  memorybank = MemoryBank() // reset

  for (line in lines) {
    if (line.startsWith("mask = ")) {
      memorybank.parseUpdateMask(line)
    } else if (line.startsWith("mem")) {
      memorybank.parseUpdateMemSetV2(line)
    }
  }

  sum = 0L
  for (v in memorybank.memory.values) {
    sum += v
  }
  println("Part 2: ${sum}")
}
