#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api
from flask import make_response
import blogger
import mainKodi
import xbmc
import json
import os
import cgi


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#Función que envía los datos a la función autentificar para enviar los datos necesarios para realizar conexión con centro multimedia
@app.route("/enviar", methods=['POST'])
def enviar():
    
    id_blog = request.form['id_blog']
    nombre = request.form['usuario']
    contrasena = request.form['contrasena']
    servidor = request.form['servidor']
    mainKodi.autentificar(nombre,contrasena,servidor,id_blog) #Pasamos los parametros de validacion en blogger y servidor kodi
    
    return render_template('menu.html')

    
#Funcion que postea en blogger la pelicula almacenada en el fichero json
@app.route("/postear", methods=['POST'])
def posting():
    
    mainKodi.ult_pel()
    mainKodi.post_ultima_peli()
    return render_template('final.html')
    
#Funcion que muestra en el navegador la pelicula almacenada en el json   
@app.route("/obtener", methods=['POST'])
def obtener():
    mainKodi.ult_pel()
    pelicula= [{                
            
            'titulo': mainKodi.titulo,
            'puntuacion': mainKodi.punt,
            'id_trailer': mainKodi.id_trailer,
        }
        ]
    return jsonify({'pelicula' : pelicula})
    
#Funcion para mostrar el json con los datos de la pelicula recibiendo los datos de la conexion a traves de la url
@app.route('/obtener/<string:servidor>', methods=['GET'])
def obtener_ser(servidor):
    mainKodi.xbmc_api=xbmc.oauth_login(servidor)
    return obtener()

#Funcion que realiza el post en blogger recibiendo los datos de la conexion a traves de la url
@app.route('/postear/<string:servidor>/<string:login>/<string:password>/<string:id_blog>/', methods=['GET'])
def postear_blog(login,password,servidor,id_blog):
    mainKodi.autentificar(login,password,servidor,id_blog)
    return posting()
    
# capturar el error 404 y devolver un JSON indicando de dicho error
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No encontrado'}), 404)

#Recoje el error 500 (fallo de validacion de los datos del formulario) y nos devuelve a la pagina principal
@app.errorhandler(500)
def not_found500(error):
   return render_template('index.html')
    

    
if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8081)))
    
    