def moo():
  print("moo moo")

def op(number):
  ops = {
      0:  ("HALT", 0),
      1:  ("SET",  2),
      2:  ("PUSH", 1),
      3:  ("POP",  1),
      4:  ("EQ",   3),
      5:  ("GT",   3),
      6:  ("JMP",  1),
      7:  ("JT",   2),
      8:  ("JF",   2),
      9:  ("ADD",  3),
      10: ("MULT", 3),
      11: ("MOD",  3),
      12: ("AND",  3),
      13: ("OR",   3),
      14: ("NOT",  2),
      15: ("RMEM", 2),
      16: ("WMEM", 2),
      17: ("CALL", 1),
      18: ("RET",  0),
      19: ("PRINT",1),
      20: ("IN",   1),
      21: ("NOOP", 0),
  }
  # TODO: throws KeyError
  try:
    op, argCount = ops[number]
    return op, argCount
  except KeyError:
    return "DATA", 0


def disassemble(ints):
  index = 0
  while index < len(ints):
    opName, argCount = op(ints[index])
    #if not opName:
    #  break
    s = "%d  => " % index
    vals = []
    for i in range(1, argCount + 1):
      if opName == "PRINT":
        vals.append(chr(ints[index + i]))
      elif ints[index + i] in range(32768, 32776):
        vals.append("[%s]" % chr((ints[index + i] % 32768) + 97))  # register
      else:
        vals.append(str(ints[index + i]))

    if opName == "EQ":
      s += "IF %s == %s, %s = 1, ELSE %s = 0" % (vals[1], vals[2], vals[0],
                                                 vals[0])
    elif opName == "GT":
      s += "IF %s > %s, %s = 1, ELSE %s = 0" % (vals[1], vals[2], vals[0],
                                                vals[0])
    elif opName == "ADD":
      try:
        total = "=> %d" % ((int(vals[1]) + int(vals[2])) % 32776)
      except ValueError:
        total = ""
      s += "%s = (%s + %s) %s" % (vals[0], vals[1], vals[2], total)

    elif opName == "MULT":
      try:
        total = "=> %d" % ((int(vals[1]) * int(vals[2])) % 32776)
      except ValueError:
        total = ""
      s += "%s = (%s * %s) %s" % (vals[0], vals[1], vals[2], total)

    elif opName == "AND":
      try:
        total = "=> %d" % ((int(vals[1]) & int(vals[2])) % 32776)
      except ValueError:
        total = ""
      s += "%s = (%s & %s) %s" % (vals[0], vals[1], vals[2], total)

    elif opName == "OR":
      try:
        total = "=> %d" % ((int(vals[1]) | int(vals[2])) % 32776)
      except ValueError:
        total = ""
      s += "%s = (%s | %s) %s" % (vals[0], vals[1], vals[2], total)

    elif opName == "NOT":
      try:
        total = "=> %d", (~ int(vals[1]))
      except ValueError:
        total = ""
      s += "%s = NOT %s %s" % (vals[0], vals[1], total)
    else:
      s += "%s " % opName
      s += " ".join(vals)

    print (s)
    index += (argCount + 1)


