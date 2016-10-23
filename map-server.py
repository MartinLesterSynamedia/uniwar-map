#!/usr/bin/python

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


@route('/test')
def test():
    return static_file("map.html", root='./')


@route('/map/<name>')
def map(name):
    params = {
        'js_url': url('/js'),
        'css_url': url('/css'),
        'name': name,
    }
    return template("map.tpl", params)


@route('/mapid/<id:int>')
def mapid(id):
    binfile = "map.bin.files/map" + str(id) + ".bin"
    xmlfile = bin2xml.bin2xml(binfile, 'xml')
    print (("Loading '" + xmlfile + "' ( " + binfile + " )"))

    return static_file(xmlfile, root='./')


@route('/xml/<name>')
def xml(name):
    name = name + ".xml"
    return static_file(name, root='xml')


@route('/css')
def css():
    return static_file("map.css", root='./')


@route('/js')
def js():
    return static_file("map.js", root='./')


@route('/assets/<path:path>')
def assets(path):
    return static_file(path, root='./assets/')


run(host='localhost', port=8080, debug=True)
