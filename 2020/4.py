#!/usr/bin/env python

"""
lines = [
  "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
  "byr:1937 iyr:2017 cid:147 hgt:183cm",
  "",
  "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
  "hcl:#cfa07d byr:1929",
  "",
  "hcl:#ae17e1 iyr:2013",
  "eyr:2024",
  "ecl:brn pid:760753108 byr:1931",
  "hgt:179cm",
  "",
  "hcl:#cfa07d eyr:2025 pid:166559648",
  "iyr:2011 ecl:brn hgt:59in",
]

lines = [
"pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980",
"hcl:#623a2f",
"",
"eyr:2029 ecl:blu cid:129 byr:1989",
"iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm",
"",
"hcl:#888785",
"hgt:164cm byr:2001 iyr:2015 cid:88",
"pid:545766238 ecl:hzl",
"eyr:2022",
"",
"iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719",
]

lines = [
  "eyr:1972 cid:100",
  "hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926",
  "",
  "iyr:2019",
  "hcl:#602927 eyr:1967 hgt:170cm",
  "ecl:grn pid:012533040 byr:1946",
  "",
  "hcl:dab227 iyr:2012",
  "ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277",
  "",
  "hgt:59cm ecl:zzz",
  "eyr:2038 hcl:74454a iyr:2023",
  "pid:3556412378 byr:2007",
]
"""
inputfile = "input4.txt"

with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

passports = []

current = {}
for line in lines:
  if line == "":
    passports.append(current)
    current = {}
  fields = line.split()
  for field in fields:
    k, v = field.split(":")
    current[k] = v
passports.append(current)


def validate(k, v):
  if k == "byr":
    v = int(v)
    if v >= 1920 and v <= 2002:
      return True
    return False
  if k == "iyr":
    v = int(v)
    if v >= 2010 and v <= 2020:
      return True
    return False
  if k == "eyr":
    v = int(v)
    if v >= 2020 and v <= 2030:
      return True
    return False
  if k == "hgt":
    if not (v.endswith("cm") or v.endswith("in")):
      return False
    height = int(v[0:-2])
    unit = v[-2:]
    if unit == "cm" and height >= 150 and height <= 193:
      return True
    if unit == "in" and height >= 59 and height <= 76:
      return True
    return False
  if k == "hcl":
    if v[0] != "#":
      return False
    for char in v[1:]:
      if not (char in ["0", "1", "2", "3", "4", "5", "6", "7",
                       "8", "9", "0", "a", "b", "c", "d", "e", "f"]):
        return False
    return True
  if k == "ecl":
    if v not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
      return False
    return True
  if k == "pid":
    if len(v) != 9:
      return False
    for char in v:
      if not char.isdigit():
        return False
    return True
  if k == "cid":
    return True
  return False

assert validate("byr", 2002) == True
assert validate("byr", 2003) == False
assert validate("hgt", "60in") == True
assert validate("hgt", "190cm") == True
assert validate("hgt", "190in") == False
assert validate("hgt", "190") == False
assert validate("hcl", "#123abc") == True
assert validate("hcl", "#123abz") == False
assert validate("hcl", "123abc") == False
assert validate("ecl", "brn") == True
assert validate("ecl", "wat") == False
assert validate("pid", "000000001") == True
assert validate("pid", "0123456789") == False

required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

valid_count = 0
invalid_count = 0
for passport in passports:
  print "PASSPORT", passport
  for req in required:
    valid = True
    if req not in passport.keys():
      print "MISSINGFIELD:", req
      valid = False
      break
  if not valid:
    invalid_count += 1
    continue
  valid = True
  for field in passport.keys():
    if not validate(field, passport[field]):
      print "Invalid:", field, passport[field]
      valid = False
      break
    else:
      print "Valid:", field, passport[field]
  if valid:
    print "VALID"
    valid_count += 1
  else:
    print "INVALID"
    invalid_count += 1
print len(passports), valid_count, invalid_count
