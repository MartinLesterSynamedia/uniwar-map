# -*- coding: utf-8 -*-

import argparse
import glob
from struct import *
from collections import namedtuple
import xml.etree.cElementTree as ET


tilesetLookup = {
    0: "Plains",
    1: "Ice",
    2: "Mars",
    3: "Volcano",
    4: "Desert",
}

tileLookup = {
    0: " ",
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

VERSION = 0
WIDTH = 6
HEIGHT = 7
PLAYERS = 9
TITLE = 14
MAP_DATA = 31

fileTemplate = []


def initFileTemplate():
    global fileTemplate
    fileTemplate = [
        {"version": "UINT"},
        {"unknown01": "UINT"},
        {"unknown02": "UBYTE"},
        {"unknown03": "UBYTE"},
        {"unknown04": "UBYTE"},
        {"unknown05": "UBYTE"},
        {"width": "USHORT"},
        {"height": "USHORT"},
        {"mission": "USHORT"},
        {"players": "UBYTE"},
        {"start_credits": "UINT"},
        {"base_credits": "USHORT"},
        {"description": "STRING"},
        {"v3_unknown": "V3INT"},
        {"title": "STRING"},
        {"unknown06": "UBYTE"},
        {"tile_set": "tileSet"},
        {"map_id": "UINT"},
        {"unknown07": "INT"},
        {"user_id_1": "INT"},
        {"region_1": "STRING"},
        {"username_1": "STRING"},
        {"rating_1": "USHORT"},
        {"unknown08": "USHORT"},
        {"played": "USHORT"},
        {"thumbup": "USHORT"},
        {"thumbdown": "USHORT"},
        {"user_id_2": "INT"},
        {"username_2": "STRING"},
        {"rating_2": "UINT"},
        {"region_2": "STRING"},
        {"map_data": "mapData"},
        {"player_bases": "playerBases"},
        {"padding": "padding"},
        {"unit_data": "unitData"},
        {"extra_data": "extraData"},
    ]

type2byte = {
    "UBYTE": [1, "B"],
    "USHORT": [2, "H"],
    "INT": [4, "i"],
    "UINT": [4, "I"],
}


def func_STRING(data, pos):
    length = unpack('>H', data[pos:pos + 2])
    length = length[0]
    pos += 2

    if length > 255:
        text = "[Silly length]"
    elif length > 0:
        try:
            text = unpack('>' + str(length) + 's', data[pos:pos + length])
            text = text[0]
            text = text.decode()
        except:
            text = str(text)
        pos += length
    else:
        text = "[BLANK]"

    return pos, text


def func_tileSet(data, pos):
    i = unpack('>B', data[pos:pos + 1])
    i = i[0]
    pos += 1
    return pos, tilesetLookup.get(i, "** FIND OUT **")


def func_V3INT(data, pos):
    i = 0
    version = fileTemplate[VERSION]["version"]
    #print("Version is " + str(version))
    if (version == 3):
        i = unpack('>i', data[pos:pos + 4])
        i = i[0]
        pos += 4
    return pos, i


def func_mapData(data, pos):
    map_data = {}
    width = fileTemplate[WIDTH]["width"]
    height = fileTemplate[HEIGHT]["height"]

    #print("*** map ***")
    i = 0
    for y in range(0, height):
        row = []
        for x in range(0, width):
            byte = pos + (x * height) + y
            val = unpack('>b', data[byte])[0]
            tile = tileLookup.get(val, "?")
            row += tile
        #print(''.join(map(str, row)))
        map_data.update({"row" + format(i, '02'): row})
        i += 1

    pos += (x * height) + y + 1
    return pos, map_data


def func_playerBases(data, pos):
    players = fileTemplate[PLAYERS]["players"]

    player_bases = {}
    for p in range(1, players + 1):
        base_data = namedtuple('base_data', 'bases')
        bd = base_data._make(unpack('>H', data[pos:pos + 2]))
        pos += 2
        player = "player" + str(p)
        player_bases[player] = {"bases": bd.bases}
        #print(player_bases)
        for i in range(1, bd.bases + 1):
            base_data2 = namedtuple('base_data2', 'x y z')
            bd2 = base_data2._make(unpack('>HHB', data[pos:pos + 5]))
            pos += 5
            #print("Player " + str(p) + " Base " + str(i) + ": " + str(bd2))
            base = "base" + str(i)
            player_bases[player][base] = {'x': bd2.x, 'y': bd2.y, 'z': bd2.z}

    #print(player_bases)
    return pos, player_bases


def func_padding(data, pos):
    players = fileTemplate[PLAYERS]["players"]

    padding = []
    ## Remove some random padding depending on number of players
    for p in range(0, 8 - players):
        pad = namedtuple('pad', 'S1')
        val = pad._make(unpack('>H', data[pos:pos + 2]))
        pos += 2
        padding += val

    return pos, padding


def func_unitData(data, pos):
    players = fileTemplate[PLAYERS]["players"]

    unit_data = {}
    for p in range(1, players + 1):
        unit_data3 = namedtuple('unit_data3', 'unit_types')
        ud3 = unit_data3._make(unpack('>H', data[pos:pos + 2]))
        pos += 2
        player = "player" + str(p)
        unit_data[player] = {"unit_types": ud3.unit_types}
        #print("Player " + str(p) + " " + str(ud3))
        for u in range(1, ud3.unit_types + 1):
            unit_data1 = namedtuple('unit_data1', 'unit_type units')
            ud1 = unit_data1._make(unpack('>HH', data[pos:pos + 4]))
            pos += 4
            #print("Player " + str(p) + " " + str(ud1))

            unit_type = unitLookup.get(ud1.unit_type, "ERROR")
            unit_data[player][unit_type] = {"units": ud1.units}

            for i in range(1, ud1.units + 1):
                unit_data2 = namedtuple('unit_data2', 'x y z')
                ud2 = unit_data2._make(unpack('>HHB', data[pos:pos + 5]))
                pos += 5
                unit = unit_type + str(i)
                unit_data[player][unit_type][unit] = {'x': ud2.x, 'y': ud2.y, 'z': ud2.z}
                #print("Player " + str(p) + " " + unit_name + " " + str(i) + ": " + str(ud2))

    return pos, unit_data


def func_extraData(data, pos):
    #print("\n*** extra " + str(len(data) - pos) + " bytes of data *** ")

    row = []
    for i in range(pos, len(data)):
        val = unpack('>B', data[i])[0]
        row.append(val)

    return 0, row


def parseFile(data):
    global fileTemplate

    functions = globals().copy()
    functions.update(locals())
    pos = 0
    for i in range(0, len(fileTemplate)):
        block = fileTemplate[i]
        for variable in block:
            data_type = block[variable]
            dt = type2byte.get(data_type, "function")
            if dt == "function":
                func = "func_" + data_type
                #print("Calling " + func)
                func = functions.get(func)
                pos, value = func(data, pos)
                #print(variable + " => " + str(value))
            else:
                #print(dt)
                value = unpack('>' + dt[1], data[pos:pos + dt[0]])
                pos += dt[0]
                value = value[0]
                #print(variable + " => " + str(value))

            ## Update the list with the value from the file
            block[variable] = value
    #print(fileTemplate)


def generateXmlRecurse(var, block, element):
    if type(block).__name__ == 'dict':
        sub = ET.SubElement(element, var)
        #print(var)
        for variable in sorted(block):
            value = block[variable]
            generateXmlRecurse(variable, value, sub)
    else:
        value = block
        ET.SubElement(element, str(var)).text = str(value).strip('[]')
        #print((str(element) + ": " + var + " => " + str(value)))


def generateXML(dest):
    dest = dest.rstrip('/')
    title = fileTemplate[TITLE]["title"]

    root = ET.Element("map")
    for i in range(0, len(fileTemplate)):
        block = fileTemplate[i]
        for variable in block:
            value = block[variable]
            value = generateXmlRecurse(variable, value, root)

    tree = ET.ElementTree(root)
    filename = dest + "/" + title + ".xml"
    try:
        tree.write(filename)
        print(("Generated '" + filename + "'"))
    except Exception as e:
        print(("Error generating '" + filename + "' : " + str(e)))

#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", type=str, required=True, help="uniwar map*.bin file. Wild cards permitted")
parser.add_argument("-d", "--dest", type=str, default=".", help="Optional output folder")

args = parser.parse_args()
#print (args)

maps = glob.glob(args.source)

if maps == 0:
    print ("No maps found: " + args.source)
    exit(0)

for m in maps:
    f = open(m, 'rb')
    file_data = f.read()

    print ("**************************\n" + m)

    initFileTemplate()
    try:
        parseFile(file_data)
    except Exception as e:
        print("Error parsing file " + m + ": " + str(e))

    generateXML(args.dest)

