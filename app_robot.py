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

import pickle
import json
import requests

def handler(signal, f):
  print('CTRL-C pressed!')
  cam.release()
  sys.exit(0)

signal.signal(signal.SIGINT, handler)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)


#============GLOBALS=============
cam = cv2.VideoCapture(0)
data = []
last_filename = ""
data_filename = ""
sleep = .250
largura_img = 720
altura_img = 240
actions = ['LEFT','RIGHT','FORWARD','BACKWARD']
autonomous_mode = False

MODEL_URL = 'http://192.168.1.185:5010/get_direction'

#=================================

#Pinos do GPIO Raspberry 3 model B 
m11=26   
m12=19
m21=21
m22=20

GPIO.setmode(GPIO.BCM) #RASPBERRY 3 MODEL B

GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

def left(t):
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)
   time.sleep(t)
   stop()


def right(t):
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)
   time.sleep(t)
   stop()

def forward(t):
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)
   time.sleep(t)
   stop()

def backward(t):
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 1)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)
   time.sleep(t)
   stop()

def stop():
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)

def take_picture():
   cam.open(0)
   cam.set(3,largura_img) #Largura da imagem capturada
   cam.set(4,altura_img) #Altura da imagem capturada
   return cam.read()


def save_picture(action):
   global last_filename,dados
   (ret,frame) = take_picture()
   if ret:
      last_filename = 'imagem_' + get_timestamp() + '.png'
      cv2.imwrite('camera/' + last_filename,frame)
      data.append((frame,action))

def get_timestamp():
   s = '{}'.format(datetime.now())
   return s.replace(" ","_").replace(":","_").replace(".","_").replace("-","_")


#Rota e função que renderiza o .html
@app.route("/")
def index():
   #  return render_template('robot.html')
   return render_template('robot_phone.html')

#Rota e função da esquerda
@app.route('/left_side')
def left_side():
   if not autonomous_mode:
      save_picture(actions[0])
      left(sleep/2)
      return last_filename
   else:
      left(sleep/2)
      return 'OK'


#Rota e função da direita
@app.route('/right_side')
def right_side():
   if not autonomous_mode:
      save_picture(actions[1])
      right(sleep/2)
      return last_filename
   else:
      right(sleep/2)
      return 'OK'

#Rota e função da frente
@app.route('/up_side')
def up_side():
   if not autonomous_mode:
      save_picture(actions[2])
      forward(sleep)
      return last_filename
   else:
      forward(sleep)
      return 'OK'

#Rota e função de trás
@app.route('/down_side')
def down_side():
   if not autonomous_mode:
      take_picture(actions[3])
      backward(sleep)
      return last_filename
   else:
      backward(sleep)
      return 'OK'

#Rota e função de parada
@app.route('/stop')
def stop_route():
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

@app.route('/save')
def save_route():
   global data_filename, data
   if len(data):
      data_filename = 'dados_{}_{}_imagens'.format(get_timestamp(),len(data))
      file = open('data/'+data_filename,'wb')
      pickle.dump(data,file)
      file.close()
      return data_filename

@app.route('/download')
def download_route():
   return send_from_directory('data',data_filename, as_attachment=True)

@app.route('/autonomous_mode')
def autonomous():
   global autonomous_mode
   autonomous_mode = True
   while(autonomous_mode):
      (ret,frame) = take_picture()
      if ret :
         data = {'frame':frame.tolist()}
         response = requests.post(MODEL_URL,json=data)
      time.sleep(.5)
   return 'OK'

@app.route('/stop_autonomous')
def stop_autonomous():
   global autonomous_mode
   autonomous_mode = False
   return 'OK'





#NOT WORKING
# TO DO: CRIAR UM TEMPLATE EM HTML+JS PARA LISTAR OS ARQUIVOS DA PASTA
# @app.route('/camera/<path:path>') 
# def static_proxy(path):
#   return send_from_directory('camera',path)


#Hospedagem no ip da rasp
if __name__ == "__main__":
 print ("Start")
 app.run(host='0.0.0.0',port=5010)
