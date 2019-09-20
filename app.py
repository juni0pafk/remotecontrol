import json
import eventlet 

from flask import Flask, render_template, redirect, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS

eventlet.monkey_patch() 

app = Flask(__name__)
socketio = SocketIO(app)
socketio = SocketIO(app,async_mode = 'eventlet')

CORS(app)

estado = {
    "MOTORL": 0,
    "MOTORR": 0,
    "CAMERA" : 0"
}

@app.route("/")
def rota_inicial():
    return render_template("index.html")
    
@socketio.on('frente')
def pfrente():
 global estado
 estado["MOTORL"] = 1
 estado["MOTORR"] = 1
 estado["CAMERA"] = 1 

@socketio.on('esquerda')
def pesquerda():
 global estado
  estado["MOTORL"] = 0
  estado["MOTORR"] = 1
  estado["CAMERA"] = 1 

@socketio.on('direita')
def pdireita():
 global estado
  estado["MOTORL"] = 1
  estado["MOTORR"] = 0
  estado["CAMERA"] = 1 

@app.route("/download", methods=["GET"])
def rota_download():
 global estado
 return json.dumps(estado)
