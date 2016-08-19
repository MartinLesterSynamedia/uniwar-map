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


def parseFile(data):
    # read data into a struct
    #print (data)
    print (len(data))

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
    pos = pos + 14
    print(md3)
    pos, username2 = exractString(data, pos)
    print("username2 = " + username2)

    map_data4 = namedtuple('map_data4', 'rating_int')
    md4 = map_data4._make(unpack('>I', data[pos:pos + 4]))
    pos = pos + 4
    print(md4)
    pos, region2 = exractString(data, pos)
    print ("Region2 = %s" % region2)

    #### The rest is map data !!!
    print("*** map ***")
    for y in range(0, height):
        row = ""
        for x in range(0, width):
            byte = pos + (x * height) + y
            tile = tileLookup.get(data[byte], "?")
            row += tile
        print(row)
    pos += (x * height) + y + 1

    print("\n*** extra data *** " + str(len(data) - pos))
    row = ""
    for i in range(pos, len(data)):
        row += str(data[i])
    print(row)


folder = "./map.bin.files/"
maps = glob.glob(folder + "map*.bin")

for m in maps:
    f = open(m, 'rb')
    file_data = f.read()
    if len(file_data) > 350:
        continue
    try:
        print ("\n*************\n" + m)
        parseFile(file_data)
    except Exception as e:
        print("Error parsing file " + m + ": " + str(e))





