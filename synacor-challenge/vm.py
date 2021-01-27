#!/usr/bin/env python3

import struct # for unpacking the binary integers

import disassembler
import mud

class Computer(object):
  def __init__(self):
    self.memory = [0] * 32768
    self.registers = [0, 0, 0, 0, 0, 0, 0, 0]
    self.stack = []
    self.index = 0
    self.opcodes = {
      0: self.halt,
      1: self.set,
      2: self.push,
      3: self.pop,
      4: self.eq,
      5: self.gt,
      6: self.jmp,
      7: self.jt,
      8: self.jf,
      9: self.add,
      10: self.mult,
      11: self.mod,
      12: self.myand,
      13: self.myor,
      14: self.mynot,
      15: self.rmem,
      16: self.wmem,
      17: self.call,
      18: self.ret,
      19: self.out,
      20: self.myin,
      21: self.noop,
    }
    self.line = ""
    self.lineindex = 99999

  def setCode(self, binary):
    # TODO: make sure I have all the numbers.
    numberCount = int(len(binary) / 2)
    # H means "unsigned short" (i.e., 16 bit int) because of course it does.
    # < means little endian.
    code = struct.unpack('<' + ('H' * numberCount), binary)
    for i in range(0, len(code) - 1):
      self.memory[i] = code[i]

  def disassemble(self):
    disassembler.disassemble(self.memory)

  def run(self):
    while True:
      op = self.memory[self.index]
      try:
        fn = self.opcodes[op]
      except KeyError:
        print("Don't know how to handle opcode %d" % op)
        exit()
      #print("  [%d]: %d %s" % (self.index, op, fn.__name__))
      fn()

  def jumpToIndex(self, i):
    self.index = i

  def mod(self, num):
    return num % 32768

  def value(self, num):
    # numbers 0..32767 mean a literal value
    # numbers 32768..32775 instead mean the value in registers 0..7
    if num >= 32776:
      print("%d is invalid" % num)
      exit()
    if num >= 32768:
      # it's a register
      return self.valueFromRegister(num)
    return num % 32768

  def valueFromRegister(self, num):
    register = num % 32768
    return self.registers[register]

  def writeMemory(self, index, value):
    if index >= 32776:
      print("writeMemory: %d is invalid" % index)
      exit()
    if index >= 32768:
      # it's a register
      register = index % 32768
      self.registers[register] = value % 32768
    else:
      self.memory[index] = value % 32768

  def setRegisterAtIndex(self, index, value):
    # Get the address listed at the index address, convert it to a register,
    # set it to the value.
    register = self.memory[index] % 32768
    #print("Set register %d to %d" % (register, value % 32768))
    self.registers[register] = value % 32768


  # Opcodes
  def halt(self): # Opcode 0
    print("Halting")
    print(self.registers)
    exit(0)

  def set(self): # Opcode 1
    value = self.value(self.memory[self.index + 2])
    self.setRegisterAtIndex(self.index + 1, value)
    self.index += 3

  def push(self): # Opcode 2
    a = self.memory[self.index + 1]
    self.stack.append(self.valueFromRegister(a))
    self.index += 2

  def pop(self): # Opcode 3
    if not self.stack:
      print("Unexpectedly empty stack. Quitting.")
      exit()
    self.setRegisterAtIndex(self.index + 1, self.stack.pop())
    self.index += 2

  def eq(self): # Opcode 4
    b = self.value(self.memory[self.index + 2])
    c = self.value(self.memory[self.index + 3])
    #print("eq", b, c)

    if b == c:
      self.setRegisterAtIndex(self.index + 1, 1)
    else:
      self.setRegisterAtIndex(self.index + 1, 0)
    self.index += 4

  def gt(self): # Opcode 5
    b = self.value(self.memory[self.index + 2])
    c = self.value(self.memory[self.index + 3])
    if b > c:
      self.setRegisterAtIndex(self.index + 1, 1)
    else:
      self.setRegisterAtIndex(self.index + 1, 0)
    self.index += 4

  def jmp(self): # Opcode 6
    #print("jmp %d" % self.memory[self.index + 1])
    a = self.value(self.memory[self.index + 1])
    self.jumpToIndex(a)

  def jt(self): # Opcode 7
    a = self.value(self.memory[self.index + 1])
    b = self.value(self.memory[self.index + 2])
    if a:
      self.jumpToIndex(b)
    else:
      self.index += 3
 
  def jf(self): # Opcode 8
    a = self.value(self.memory[self.index + 1])
    b = self.value(self.memory[self.index + 2])
    if not a:
      self.jumpToIndex(b)
    else:
      self.index += 3

  def add(self): # Opcode 9
    b = self.value(self.memory[self.index + 2])
    c = self.value(self.memory[self.index + 3])
    # infinite loop? uncomment
    #print ("Adding %d and %d" % (b, c))
    self.setRegisterAtIndex(self.index + 1, (b + c))
    self.index += 4

  def mult(self): # Opcode 10
    b = self.value(self.memory[self.index + 2])
    c = self.value(self.memory[self.index + 3])
    self.setRegisterAtIndex(self.index + 1, (b * c))
    self.index += 4

  def mod(self): # Opcode 10
    b = self.value(self.memory[self.index + 2])
    c = self.value(self.memory[self.index + 3])
    self.setRegisterAtIndex(self.index + 1, (b % c))
    self.index += 4

  def myand(self): # Opcode 12
    b = self.value(self.memory[self.index + 2])
    c = self.value(self.memory[self.index + 3])
    self.setRegisterAtIndex(self.index + 1, (b & c))
    self.index += 4

  def myor(self): # Opcode 13
    b = self.value(self.memory[self.index + 2])
    c = self.value(self.memory[self.index + 3])
    self.setRegisterAtIndex(self.index + 1, (b | c))
    self.index += 4

  def mynot(self): # Opcode 14
    b = self.value(self.memory[self.index + 2])
    self.setRegisterAtIndex(self.index + 1, (~ b))
    self.index += 3

  def rmem(self): # Opcode 15
    # read memory at address <b> and write it to <a>
    a = self.memory[self.index + 1]
    b = self.memory[self.index + 2]
    #print ("rmem", a, b)

    # read memory at address b (which might be in a register)
    if b >= 32768:
      addrFromRegister = self.registers[b % 32768]
      value = self.memory[addrFromRegister]
    else:
      #print ("reading b from memory address", b)
      value = self.memory[b]

    if a >= 32768:
      # it's a register
      register = a % 32768
      self.registers[register] = value
      #print("Setting register %d to %d" % (register, value))
    else: # TODO
      print("thought it was a register")
      exit()
      self.memory[a] = b % 32768
    self.index += 3


  def wmem(self): # Opcode 16
  # write the value from <b> into memory at address <a>
    a = self.memory[self.index + 1]
    b = self.memory[self.index + 2]
    #print ("wmem", a, b)

    if b >= 32768:
      # actually the value of the register b
      value = self.registers[b % 32768]
    else:
      value = b

    if a >= 32768:
      addr = self.registers[a % 32768]
    else:
      addr = a
    self.memory[addr] = value
    self.index += 3

  def call(self): # Opcode 17
    a = self.value(self.memory[self.index + 1])
    self.stack.append(self.index + 2)
    self.jumpToIndex(a)

  def ret(self): # Opcode 18
    if not self.stack:
      print("Unexpectedly empty stack. Quitting.")
      exit()
    self.jumpToIndex(self.stack.pop())

  def myin(self): # Opcode 20
    """read a character from the terminal and write its ascii code to <a>; it can
    be assumed that once input starts, it will continue until a newline is
    encountered; this means that you can safely read whole lines from the
    keyboard and trust that they will be fully read

    Type 'go' to solve the text adventure.
    """
    a = self.memory[self.index + 1] 
    # TODO: might it not be a register?
    register = a % 32768
    if self.lineindex >= len(self.line):
      self.line = input("=> ")
      if self.line == "go":
        self.line = mud.solve_puzzle()
      self.line += '\n'
      self.lineindex = 0
    self.registers[register] = ord(self.line[self.lineindex])
    self.lineindex += 1
    self.index += 2
    

  def out(self): # Opcode 19
    a = self.value(self.memory[self.index + 1])
    print(chr(a), end='')
    self.index += 2

  def noop(self): # Opcode 21
    self.index += 1

numbers = []
with open("challenge.bin", "rb") as f:
  binary = f.read()

computer = Computer()
computer.setCode(binary)
computer.disassemble()
# To run the tests, comment the setCode above, uncomment these
#computer.registers[7] = 6161
#x=[9,32768,32769,4,19,32768]
#for i in range(len(x)):
#  computer.memory[i] = x[i]
#print(computer.memory[0:20])
#print(computer.registers)
computer.run()

