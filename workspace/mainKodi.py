#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xbmcjson import XBMC
import json
import io
import xbmc
import blogger
from gdata import service
import gdata.blogger.client
import gdata.client
import gdata.data
import atom.data

#variables globales
global titulo
global punt
global id_trailer
global xbmc_api
global blog_id
global blogger_service

#autentificacion
def autentificar(login,password,servidor,id_blog):
    global xbmc_api
    global blog_id
    global blogger_service
    xbmc_api=xbmc.oauth_login(servidor) #Establecemos la conexión con el centro multimedia
    blog_id=id_blog #Obtenemos el id del blog
    blogger_service=blogger.login_blog(login, password) # Establecemos conexion con blogger

#Funcion que obtiene la ultima pelicula vista y guarda los datos en variables globales
def ult_pel():
    global titulo
    global punt
    global id_trailer
    #Se guarda la respuesta a la llamada de la api en la variable pelis
    pelis= xbmc_api.VideoLibrary.GetMovies({ "filter": {"field": "playcount", "operator": "is", "value": "1"}, 
                                             "limits": { "start" : 0, "end": 1 }, "properties": ["rating","trailer"],   
                                             "sort": { "order": "descending", "method": "lastplayed" } }, id="libMovies")
    xbmc.save_json("pelis",pelis) #Guardamos el contenido de pelis en un archivo json
    datos =json.loads(open('pelis.json').read()) #Se abre el json guardado anteriormente
    titulo=datos["result"]["movies"][0]["label"] #Se asigna el titulo de la pelicula a la variable global titulo
    punt=round(datos["result"]["movies"][0]["rating"],1)#Se rondea la puntuación de la pelicula y se asigna a la variable global punt
    trailer=datos["result"]["movies"][0]["trailer"] #Se asigna el enlace del trailer a la variable trailer
    
    if (trailer!=""): #Se comprueba que el trailer esta disponible
        id_trailer=trailer[57:] #se obtiene el id del trailer y se guarda en la variable global id_trailer



#Funcion que postea la ultima pelicula vista
def post_ultima_peli():
    #Comprueba que el trailer esta disponile
    if (id_trailer!=""):
        blogEntry = blogger.CreatePublicPost(blogger_service, blog_id,
    	title='Ultima Pelicula vista', content=titulo+'<br />Puntuacion: '+str(punt)+'<br /><iframe allowfullscreen="" class="YOUTUBE-iframe-video" frameborder="0" height="266" src="https://www.youtube.com/embed/'+id_trailer+'?feature=player_embedded" width="320"></iframe>')
    else:
        blogEntry = blogger.CreatePublicPost(blogger_service, blog_id,
    	title='Ultima Pelicula vista', content=titulo+'<br />Puntuacion: '+str(punt)+'<br /> Trailer no disponible')
  

