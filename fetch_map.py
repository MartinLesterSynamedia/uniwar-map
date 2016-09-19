import bin2xml
from bottle import *

@route('/')
@route('/info')
@route('/map')
@route('/map/')
@route('/mapid')
@route('/mapid/')
def info():
    text = "Use http://url:port/map/[map name] to load a map by name<br>"
    text += "Use http://url:port/mapid/[map db id] to load a map by an id<br>"


@route('/map/<name>')
def map(name):
    return "Loading '%s'" % name


@route('/map/test')
def map(name):
    return static_file("/raidstore/netbeans/uniwar-map/xml/EdTestairisland.xml", root='')


@route('/mapid/<id:int>')
def mapid(id):
    binfile = "map.bin.files/map" + str(id) + ".bin"
    xmlfile = bin2xml.bin2xml(binfile, 'xml')
    print (("Loading '" + xmlfile + "' ( " + binfile + " )"))

    return static_file(xmlfile, root='./')


run(host='localhost', port=8080, debug=True)
