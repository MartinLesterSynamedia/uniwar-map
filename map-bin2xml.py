# -*- coding: utf-8 -*-

import glob
from struct import *
from collections import namedtuple


def exractString(data, pos):
    length = unpack('>H', data[pos:pos + 2])
    length = length[0]
#    print("string length = " + str(length))
    pos += 2
    if length > 255:
        text = "<Silly length>"
    elif length > 0:
        text = unpack('>' + str(length) + 's', data[pos:pos + length])
        text = text[0]
        text = text.decode()
        pos += length
    else:
        text = "<BLANK>"
#    print(str(text))
    return pos, text

tileLookup = {
    0: ".",
    1: "_",
    2: "B",
    3: "F",
    4: "M",
    5: "S",
    6: "D",
    7: "w",
    8: "P",
    9: "+",
}

unitLookup = {
    1: "Basic",
    2: "Medic",
    3: "Range",
    4: "Tank",
    5: "Light",
    6: "Boat",
    7: "Medium",
    8: "Converted",
}


def parseFile(data):
    # read data into a struct
    #print (data)
    print ("Data size = " + str(len(data)))

    map_data = namedtuple('map_data', 'version I1 b1 b2 b3 b4 width height mission players start_credits base_credits')
    md = map_data._make(unpack('>IIBBBBHHHBIH', data[0:25]))
    pos = 25
    pos, desc = exractString(data, pos)

    width = md.width
    height = md.height

    if (md.version == 3):
        i1 = unpack('>i', data[pos:pos + 4])
        i1 = i1[0]
        pos += 4
        print("v3 only int = " + str(i1))  # always 0

    pos, name = exractString(data, pos)
    print ("Name = %s" % name)
    print ("Description = %s" % desc)
    print ("width = " + str(width) + ". Height = " + str(height))

    print (md)

    map_data2 = namedtuple('map_data2', 'b1 b2 map_id i1 userid1')
    md2 = map_data2._make(unpack('>BBIii', data[pos:pos + 14]))
    pos += 14
    print(md2)

    pos, region1 = exractString(data, pos)
    print ("Region1 = %s" % region1)
    pos, username1 = exractString(data, pos)
    print ("Username1 = %s" % username1)

    map_data3 = namedtuple('map_data3', 'rating1 s1 played up down userid2')
    md3 = map_data3._make(unpack('>HHHHHi', data[pos:pos + 14]))
    pos += 14
    print(md3)
    pos, username2 = exractString(data, pos)
    print("username2 = " + username2)

    map_data4 = namedtuple('map_data4', 'rating_int')
    md4 = map_data4._make(unpack('>I', data[pos:pos + 4]))
    pos += 4
    print(md4)
    pos, region2 = exractString(data, pos)
    print ("Region2 = %s" % region2)

    #### The rest is map data !!!
    print("*** map ***")
    for y in range(0, height):
        row = ""
        for x in range(0, width):
            byte = pos + (x * height) + y
            val = unpack('>b', data[byte])[0]
            tile = tileLookup.get(val, "?")
            row += tile
        print(row)
    pos += (x * height) + y + 1

    for p in range(1, md.players + 1):
        base_data = namedtuple('base_data', 'bases')
        bd = base_data._make(unpack('>H', data[pos:pos + 2]))
        pos += 2
        print("Player " + str(p) + " Bases/Ports: " + str(bd.bases))
        for i in range(1, bd.bases + 1):
            base_data2 = namedtuple('base_data2', 'x y b1')
            bd2 = base_data2._make(unpack('>HHB', data[pos:pos + 5]))
            pos += 5
            print("Player " + str(p) + " Base " + str(i) + ": " + str(bd2))

    ## Remove some random padding depending on number of players
    for p in range(0, 8 - md.players):
        unit_data = namedtuple('unit_data', 'S1')
        unit_data._make(unpack('>H', data[pos:pos + 2]))
        pos += 2

    for p in range(1, md.players + 1):
        unit_data3 = namedtuple('unit_data3', 'unit_types')
        ud3 = unit_data3._make(unpack('>H', data[pos:pos + 2]))
        pos += 2
        print("Player " + str(p) + " " + str(ud3))
        for i in range(1, ud3.unit_types + 1):
            unit_data1 = namedtuple('unit_data1', 'unit_type units')
            ud1 = unit_data1._make(unpack('>HH', data[pos:pos + 4]))
            pos += 4
            print("Player " + str(p) + " " + str(ud1))
            unit_name = unitLookup.get(ud1.unit_type, "ERROR")
            for i in range(1, ud1.units + 1):
                unit_data2 = namedtuple('unit_data2', 'x y b1')
                ud2 = unit_data2._make(unpack('>HHB', data[pos:pos + 5]))
                pos += 5
                print("Player " + str(p) + " " + unit_name + " " + str(i) + ": " + str(ud2))

    print("\n*** extra data *** " + str(len(data) - pos))
    row = ""
    for i in range(pos, len(data)):
        val = unpack('>B', data[i])[0]
        row += str(val)
    print(row)


folder = "./map.bin.files/"
maps = glob.glob(folder + "map*.bin")

for m in maps:
    f = open(m, 'rb')
    file_data = f.read()
#    if len(file_data) > 450:
#        continue
    try:
        print ("\n*************\n" + m)
        parseFile(file_data)
    except Exception as e:
        print("Error parsing file " + m + ": " + str(e))





