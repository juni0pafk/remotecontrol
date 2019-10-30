from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

#Pinos do GPIO Rasp
m11=12   
m12=16
m21=18
m22=22

##Declarações
GPIO.setmode(GPIO.BOARD)

GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

print ("Done")


#Rota e função que renderiza o .html
@app.route("/")
def index():
    return render_template('robot.html')

#Rota e função da esquerda
@app.route('/left_side')
def left_side():
    data1="LEFT"
    GPIO.output(m11 , 0)
    GPIO.output(m12 , 0)
    GPIO.output(m21 , 1)
    GPIO.output(m22 , 0)
    return 'true'

#Rota e função da direita
@app.route('/right_side')
def right_side():
   data1="RIGHT"
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)
   return 'true'

#Rota e função da frente
@app.route('/up_side')
def up_side():
   data1="FORWARD"
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)
   return 'true'

#Rota e função de trás
@app.route('/down_side')
def down_side():
   data1="BACK"
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 1)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)
   return 'true'

#Rota e função de parada
@app.route('/stop')
def stop():
   data1="STOP"
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)
   return  'true'

#Hospedagem no ip da rasp
if __name__ == "__main__":
 print ("Start")
 app.run(host='192.168.0.16',port=5010)
