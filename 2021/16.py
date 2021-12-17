#!/usr/bin/env python

inputfile = "input"
with open(inputfile, "r") as f:
  line = f.readline().strip()


class Packet(object):
  type = -1

class Literal(Packet):
  def __init__(self):
    self.value = -1

  def parse(self, bits, maxlength=9999999):
    i = 0
    value = ""
    while True:
      value += bits[i+1: i+5]
      if bits[i] != "1":
        break
      i += 5
      if i > maxlength:
        break
    i += 5
    self.value = int(value, 2)
    return i

  def __repr__(self):
    return "Value(%d)" % self.value

class Operator(Packet):
  def __init__(self):
    self.length = -1
    self.number = -1

  def parse(self, bits):
    lengthtypeid = bits[0]
    i = 1
    j = -1
    if lengthtypeid == "0":
      j = i + 15
      self.length = int(bits[i:j], 2)
    else:
      j = i + 11
      self.number = int(bits[i:j], 2)
    return j, self.length, self.number

  def __repr__(self):
    return "Operator(%d/%d)" % (self.length, self.number)

class PacketReader(object):
  def __init__(self, bits):
    self.bits = bits
    self.index = 0
    self.sum = 0

  def add(self, args):
    return sum(args)

  def mul(self, args):
    product = 1
    for i in args:
      product *= i
    return product

  def min(self, args):
    return min(args)

  def max(self, args):
    return max(args)

  def gt(self, args):
    return int(args[0] > args[1])

  def lt(self, args):
    return int(args[0] < args[1])

  def eq(self, args):
    return int(args[0] == args[1])

  def create_next(self, maxlength=9999999):
    initial = self.index

    # Read the header
    header = self.bits[self.index:]
    version = int(header[0:3], 2)
    self.sum += version
    typeid = int(header[3:6], 2)
    self.index += 6
    maxlength -= 6

    # Now we're past the header, make a packet from the rest
    if typeid == 4:
      packet = Literal()
      consumed = packet.parse(self.bits[self.index:], maxlength=maxlength)
      self.index += consumed
    else:
      args = []
      packet = Operator()
      consumed, length, number = packet.parse(bits[self.index:])
      self.index += consumed

      # if there's a length, get packets until the index has moved [length]
      if length != -1:
        break_at = self.index + length
        while True:
          packet, consumed = self.create_next(maxlength=length)
          args.append(packet.value)
          length -= consumed
          if self.index >= break_at:
            break
      # if there's a number, get [number] packets.
      elif number != -1:
        for i in range(number):
          packet, consumed = self.create_next()
          args.append(packet.value)

      ops = {
        0: self.add,
        1: self.mul,
        2: self.min,
        3: self.max,
        5: self.gt,
        6: self.lt,
        7: self.eq,
      }

      fn = ops[typeid]
      ret = fn(args)
      packet.value = ret
      #print("%s(%s)" % (fn.__name__, args))

    total_consumed = self.index - initial
    return packet, total_consumed


#line = "D2FE28"
#line = "38006F45291200"
#line = "A0016C880162017C3686B18A3D4780"
#line = "C200B40A82"
#line = "04005AC33890"
#line = "880086C3E88112"
#line = "D8005AC2A8F0"
#line = "9C0141080250320F1802104A08"
bits = format(int(line, 16), "0%db" % (len(line) * 4))

reader = PacketReader(bits)
packet, _ = reader.create_next()
print("Part 1", reader.sum)
print("Part 2", packet.value)
