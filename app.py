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

def handler(signal, f):
  print('CTRL-C pressed!')
  cam.release()
  sys.exit(0)

signal.signal(signal.SIGINT, handler)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)


#============GLOBALS=============
data = []
last_filename = ""
data_filename = ""
sleep = .2
actions = ['LEFT','RIGHT','FORWARD','BACKWARD']
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

def take_picture(action):
   global last_filename,dados
   cam.open(0)
   cam.set(3,320) #Largura da imagem capturada
   cam.set(4,240) #Altura da imagem capturada
   (ret,frame) = cam.read()
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
   take_picture(actions[0])
   left()
   time.sleep(sleep)
   stop()
   return last_filename

#Rota e função da direita
@app.route('/right_side')
def right_side():
   take_picture(actions[1])
   right()
   time.sleep(sleep)
   stop()
   return last_filename

#Rota e função da frente
@app.route('/up_side')
def up_side():
   take_picture(actions[2])
   forward()
   time.sleep(sleep)
   stop()
   return last_filename

#Rota e função de trás
@app.route('/down_side')
def down_side():
   take_picture(actions[3])
   backward()
   time.sleep(sleep)
   stop()
   return last_filename

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
      file = open(data_filename,'w')
      pickle.dump(data,'data/'+data_filename)
      file.close()
      return data_filename

@app.route('/download')
def download_route():
   return send_from_directory('data',data_filename)



#NOT WORKING
# TO DO: CRIAR UM TEMPLATE EM HTML+JS PARA LISTAR OS ARQUIVOS DA PASTA
# @app.route('/camera/<path:path>') 
# def static_proxy(path):
#   return send_from_directory('camera',path)


#Hospedagem no ip da rasp
if __name__ == "__main__":
 print ("Start")
 app.run(host='0.0.0.0',port=5010)
