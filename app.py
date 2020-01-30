#Raspberry Web Controlled Robot (Circuit Digest)
#Adaptado: Andressa Theotônio

from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

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

sleep = .5


##Declarações
# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM) #RASPBERRY 3 MODEL B

GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

print ("Done")

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


#Rota e função que renderiza o .html
@app.route("/")
def index():
   #  return render_template('robot.html')
   return render_template('robot_phone.html')

#Rota e função da esquerda
@app.route('/left_side')
def left_side():
   data1="LEFT"
   left()
   time.sleep(sleep)
   stop()
   return 'true'

#Rota e função da direita
@app.route('/right_side')
def right_side():
   data1="RIGHT"
   right()
   time.sleep(sleep)
   stop()
   return 'true'

#Rota e função da frente
@app.route('/up_side')
def up_side():
   data1="FORWARD"
   forward()
   time.sleep(sleep)
   stop()
   return 'true'

#Rota e função de trás
@app.route('/down_side')
def down_side():
   data1="BACK"
   backward()
   time.sleep(sleep)
   stop()
   return 'true'

#Rota e função de parada
@app.route('/stop')
def stop_route():
   data1="STOP"
   stop()
   return  'true'

#Hospedagem no ip da rasp
if __name__ == "__main__":
 print ("Start")
 app.run(host='0.0.0.0',port=5010)
