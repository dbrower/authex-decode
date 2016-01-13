#!/usr/bin/env python

import sys

# File begins with a master offset table at offset 0x204.
# It consists of 1 entry giving total number of records (4 bytes LE)
# followed by 249 entries of offsets for each pair table (4 bytes LE each).
# Each pair table in consists of 500 entries giving the offset and length
# of a record (4 byte LE offset + 2 byte (LE) length each).
#
# Records are a sequence of fields separated by a 0xfe byte.
# Multiple entries in a field are prefixed with a 0xb1 byte.
#
# The order of the fields are:
#
# * Subject(s), each begins with a 0xb1 byte
# * Title, begins with 0xfe byte
# * Author, begin with 0xfe byte. Each name then begins with a 0xb1 byte
# * Date, begin with 0xfe
# * Page, begin with 0xfe
# * Illustration, begin with 0xfe
# * Sort Date, begin with 0xfe, sometimes directly followed by a 0xb1

fields = [
        "Subject:",
        "Title:",
        "Author:",
        "Date:",
        "Page:",
        "Source:",
        "Illustration:",
        "Sort Date:",
        "Field 8:",
        "Field 9:",
        "Field 10:",
        "Field 11:",
        "Field 12:",
        "Field 13:",
        "Field 14:"
]

def read32(s):
    shift = 0
    result = 0
    for c in s[:4]:
        result |= ord(c) << shift
        shift += 8
    return result

def read16(s):
    return ord(s[0]) | (ord(s[1]) << 8)

def parse_master_table(s):
    num_records = read32(s)
    s = s[4:]
    result = []
    for i in range(249):
        offset = read32(s)
        if offset != 0:
            result.append(offset)
        s = s[4:]
    return result

def parse_pair_table(s):
    result = []
    for i in range(500):
        offset = read32(s)
        length = read16(s[4:6])
        if offset != 0:
            result.append((offset, length))
        s = s[6:]
    return result

def parse_record(s):
    terms = s.split("\xfe")
    print
    i = 0
    for data in terms:
        ts = data.split("\xb1")
        for t in ts:
            if t:
                print fields[i], t
        i += 1

with open("AV03.bff","r") as f:
    s = f.read()


pair_tables = parse_master_table(s[0x204:])
for pt_offset in pair_tables:
    records = parse_pair_table(s[pt_offset:])
    for offset, length in records:
        parse_record(s[offset:offset+length])

