#!/usr/bin/env python

class Computer(object):
  def __init__(self):
    self.regA = 0
    self.regB = 0
    self.regC = 0
    self.code = []
    self.instr = 0
    self.halt = False
    self.output = []
    self.fail_fast = False

  """
    Each instruction also reads the 3-bit number after it as an input; this is
    called its operand. There are two types of operands; each instruction specifies
    the type of its operand. The value of a literal operand is the operand itself.
    For example, the value of the literal operand 7 is the number 7. The value
    of a combo operand can be found as follows:

      Combo operands 0 through 3 represent literal values 0 through 3.
      Combo operand 4 represents the value of register A.
      Combo operand 5 represents the value of register B.
      Combo operand 6 represents the value of register C.
      Combo operand 7 is reserved and will not appear in valid programs.
  """
  def combo_operand(self, opval):
    if opval in [0, 1, 2, 3]:
      return opval, "literal %d" % opval
    if opval == 4:
      return self.regA, "val of regA"
    if opval == 5:
      return self.regB, "val of regB"
    if opval == 6:
      return self.regC, "val of regC"
    if opval == 7:
      print("Unexpected opval 7")
      exit()

  def move_pointer(self, index):
    # only move_pointer writes to the pointer
    self.instr = index

  def next_number(self):
    if self.instr >= len(self.code):
      self.halt = True
      return
    val = self.code[self.instr]
    self.move_pointer(self.instr + 1)
    return val

  def _divide(self, numerator):
    operand, desc = self.combo_operand(self.next_number())
    denominator = pow(2, operand)
    value = int(numerator / denominator)
    return value, desc

  def adv(self):
    """The adv instruction (opcode 0) performs division. The numerator is the
    value in the A register. The denominator is found by raising 2 to the power
    of the instruction's combo operand. (So, an operand of 2 would divide A by 4
    (2^2); an operand of 5 would divide A by 2^B.) The result of the division
    operation is truncated to an integer and then written to the A register."""
    numerator = self.regA
    val, desc = self._divide(numerator)
    if DEBUG: print("adv: Setting regA to regA/2^(%s), aka %d/something" % (desc, numerator))
    self.regA = val

  def bxl(self):
    """The bxl instruction (opcode 1) calculates the bitwise XOR of register B
    and the instruction's literal operand, then stores the result in register B."""
    val1 = self.regB
    val2 = self.next_number()
    self.regB = val1 ^ val2
    if DEBUG: print("bxl: Storing regB(%d)^literal %d in regB" % (val1, val2))


  def bst(self):
    """The bst instruction (opcode 2) calculates the value of its combo operand
    modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to
    the B register."""
    val1, desc = self.combo_operand(self.next_number())
    val1 = val1 % 8
    if DEBUG: print("bst: Storing %s mod 8 (%d) in regB" % (desc, val1))
    self.regB = val1

  def jnz(self):
    """The jnz instruction (opcode 3) does nothing if the A register is 0. However,
    if the A register is not zero, it jumps by setting the instruction pointer to
      the value of its literal operand; if this instruction jumps, the instruction
      pointer is not increased by 2 after this instruction. """
    val = self.next_number()
    if DEBUG: print("jnz: Jumping to pos %d if A reg isn't zero. It's: %d" % (val, self.regA))
    if self.regA != 0:
      self.move_pointer(val)


  def bxc(self):
    """The bxc instruction (opcode 4) calculates the bitwise XOR of register B and
    register C, then stores the result in register B. (For legacy reasons, this
    instruction reads an operand but ignores it.)"""
    _ = self.next_number()
    val1 = self.regB
    val2 = self.regC
    if DEBUG: print("bxc: Setting regB to regB^regC – %d^%d" % (val1, val2))
    self.regB = val1 ^ val2

  def out(self):
    """The out instruction (opcode 5) calculates the value of its combo operand
    modulo 8, then outputs that value. (If a program outputs multiple values,
    they are separated by commas.)"""
    output, desc = self.combo_operand(self.next_number())
    output = output % 8
    if DEBUG: print("out: printing out %s: %d" % (desc, output))
    self.output.append(output)
    if self.fail_fast:
      if len(self.code) > len(self.output):
        self.halt = True
        return

      i = len(self.output) - 1
      try:
        if self.output[i] != self.code[i]:
          self.halt = True
      except IndexError:
        print(self.code, self.output)

  def bdv(self):
    """The bdv instruction (opcode 6) works exactly like the adv instruction except
    that the result is stored in the B register. (The numerator is still read from
    the A register.)"""
    numerator = self.regA
    val, desc = self._divide(numerator)
    if DEBUG: print("bdv: Setting regB to regA/2^(%s), aka %d/something" % (desc, numerator))
    self.regB = val

  def cdv(self):
    """The cdv instruction (opcode 7) works exactly like the adv instruction except
    that the result is stored in the C register. (The numerator is still read from
    the A register.)"""
    numerator = self.regA
    val, desc = self._divide(numerator)
    if DEBUG: print("cdv: Setting regC to regA/2^(%s), aka %d/something" % (desc, numerator))
    self.regC = val

  def run(self, code, a=0, b=0, c=0):
    self.reset()
    self.code = code
    self.regA = a
    self.regB = b
    self.regC = c
    if DEBUG: print("Welcome to friendly computer.")
    fns = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]
    if DEBUG: print("Running program:", self.code)
    while not self.halt:
      num = self.next_number()
      if num is None:
        break
      inst = fns[num]
      inst()
      if DEBUG: print("[%d] [%d] [%d]" % (self.regA, self.regB, self.regC))
      #if DEBUG: print("Regs: [%d] [%d] [%d] Code: [%s]  instr [%d]" % (self.regA, self.regB, self.regC, self.code, self.instr))
    final = ",".join([str(x) for x in self.output])
    return final

  def reset(self):
    self.output = []
    self.code = ""
    self.instr = 0
    self.regA = 0
    self.regB = 0
    self.regC = 0
    self.halt = False

computer = Computer()

# Real input

regA = 37293246
regB = 0
regC = 0
code = "2,4,1,6,7,5,4,4,1,7,0,3,5,5,3,0"
code = code.strip()

"""
# Test 1
regA = 729
regB = 0
regC = 0
code = "0,1,5,4,3,0"
"""

DEBUG = False
instructions = [int(x) for x in code.split(",")]
part1 = computer.run(instructions, a=regA)
print("Part 1:", part1)


part2 = 0

"""
# Python version of the input code. Not actually needed in the end.
def run(origa):
  out = []
  i = 0
  a = origa
  b = 0

  alist = []
  while a != 0:
    alist.append(a)
    b = (a % 8) ^ 6
    b = b ^ int(a / pow(2, b))
    b = b ^ 7
    res = b % 8
    a = int(a / 8)
    out.append(res)
    if len(out) > len(instructions):
      break
    if out[i] != instructions[i]:
      break
    i += 1
  return out
"""

# stripped down version of what the python code does to get b from a
def getb(a):
  b = a % 8
  b = b ^ 6
  b = b ^ int(a / pow(2, b))
  b = b ^ 7
  return b


toTry = []
toFind = instructions[::-1] # reversed

halt = False
for a in range(8):
  output = []
  i = 0
  toTry = [a]
  for i in range(0, len(toFind)):
    # going one digit at a time..., toFind[i]
    toTryNext = []
    for a in toTry:
      b = getb(a)
      if (b % 8) != toFind[i]:
        continue
      # try all the numbers, N, where int(N / 8) = a
      for n in range(a * 8, (a + 1) * 8):
        if halt:
          break
        toTryNext.append(n)
        output = computer.run(instructions, a=n)
        if output == code:
          part2 = n
          halt = True
          break
    if len(toTryNext) == 0:
      break
    toTry = toTryNext


print("Part 2:", part2)
