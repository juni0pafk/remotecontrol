import json

from flask import Flask, render_template, redirect, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)

estado = {
    "MOTOR1": 0,
    "MOTOR2": 0,
    "CAMERA" : 0"
}
    
    
@socketio.on('frente')
def pfrente():
 global estado
 estado["MOTORL"] = 1
 estado["MOTORR"] = 1
 estado["CAMERA"] = 1 

@socketio.on('atras')
def ptras():
 global estado
  estado["MOTORL"] = 2
  estado["MOTORR"] = 2
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

@app.route("/")
def rota_inicial():
    return render_template("index.html")

@app.route("/download", methods=["GET"])
def rota_download():
 global estado
 return json.dumps(estado)
 
