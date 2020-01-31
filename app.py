#Raspberry Web Controlled Robot (Circuit Digest)
#Adaptado: Andressa Theotônio

from flask import Flask
from flask import render_template, request, send_file, send_from_directory
from flask_cors import CORS

from datetime import datetime
import RPi.GPIO as GPIO
import cv2
import time

import sys
import signal

def handler(signal, frame):
  print('CTRL-C pressed!')
  cam.release()
  sys.exit(0)

signal.signal(signal.SIGINT, handler)


app = Flask(__name__)
CORS(app)

cam = cv2.VideoCapture(0)
cam.set(3,320) #Largura da imagem capturada
cam.set(4,240) #Altura da imagem capturada
img_counter = 0
last_filename = ""


#Pinos do GPIO Rasp
# m11=12   
# m12=16
# m21=18
# m22=22

#Pinos do GPIO Raspberry 3 model B 
m11=26   
m12=19
m21=21
m22=20

sleep = .2


##Declarações
# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM) #RASPBERRY 3 MODEL B

GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

def left():
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)

def right():
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)

def forward():
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)

def backward():
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 1)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)

def stop():
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)

def take_picture():
   global last_filename
   ret,frame = cam.read()
   if ret:
      last_filename = 'camera/imagem_{}'.format(datetime.now())
      last_filename = last_filename.replace(" ","_").replace(":","_").replace(".","_").replace("-","_") + '.png'
      cv2.imwrite(last_filename,frame)


#Rota e função que renderiza o .html
@app.route("/")
def index():
   #  return render_template('robot.html')
   return render_template('robot_phone.html')

#Rota e função da esquerda
@app.route('/left_side')
def left_side():
   take_picture()
   data1="LEFT"
   left()
   time.sleep(sleep)
   stop()
   return last_filename

#Rota e função da direita
@app.route('/right_side')
def right_side():
   take_picture()
   data1="RIGHT"
   right()
   time.sleep(sleep)
   stop()
   return last_filename

#Rota e função da frente
@app.route('/up_side')
def up_side():
   take_picture()
   data1="FORWARD"
   forward()
   time.sleep(sleep)
   stop()
   return last_filename

#Rota e função de trás
@app.route('/down_side')
def down_side():
   take_picture()
   data1="BACK"
   backward()
   time.sleep(sleep)
   stop()
   return last_filename

#Rota e função de parada
@app.route('/stop')
def stop_route():
   data1="STOP"
   stop()
   return  'true'

@app.route('/get_last_image')
def image_route():
   if len(last_filename):
      #return send_file(last_filename,mimetype='image/png')
      return last_filename

@app.route('/camera/<path:path>')
def send_image(path):
    return send_from_directory('camera', path)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

#NOT WORKING
# TO DO: CRIAR UM TEMPLATE EM HTML+JS PARA LISTAR OS ARQUIVOS DA PASTA
# @app.route('/camera/<path:path>') 
# def static_proxy(path):
#   return send_from_directory('camera',path)


#Hospedagem no ip da rasp
if __name__ == "__main__":
 print ("Start")
 app.run(host='0.0.0.0',port=5010)
