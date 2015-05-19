#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xbmcjson import XBMC
import json
import io

#Funcion para establecer la conexion con el centro multimedia XBMC
def oauth_login(servidor):
    xbmc = XBMC("http://"+servidor+"/jsonrpc")
    return xbmc


#Función para grabar la información en formato JSON
def save_json(filename, data):
    with io.open('{0}.json'.format(filename),'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))

#Función para leer el fichero JSON
def load_json(filename):
    with io.open('{0}.json'.format(filename),encoding='utf-8') as f:
        return f.read()