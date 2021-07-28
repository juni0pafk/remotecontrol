from datetime import datetime
import RPi.GPIO as GPIO
import cv2
import time
import BlynkLib
import pickle



#============GLOBALS=============
cam = cv2.VideoCapture(0)
#cam.release()
data = []
last_filename = ""
data_filename = ""
sleep = .25
largura_img = 160
altura_img = 120
actions = ['LEFT MIN','LEFT MAX','FORWARD', 'RIGHT MIN', 'RIGHT MAX'] #5, 4, 7, 9, 10
autonomous_mode = False
min_left = 5
max_left = 4
frente = 7
min_right = 9
max_right = 11


#=================================

#Pinos do GPIO Raspberry 3 model B 
m11 = 3   
m12 = 4
m21 = 27
m22 = 22
servo = 18

GPIO.setmode(GPIO.BCM) #RASPBERRY 3 MODEL B
GPIO.setwarnings(False)

token = '_MfJJENuRHD6vBUbWZ2meluchPAWIem2' #comunicação com o controle feito no app Blynk

GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.setup(servo, GPIO.OUT)


servo1 = GPIO.PWM(servo, 50) #PWM com 50Hz => duty cycle 2.5-12.5% (0-180 graus)
servo1.start(7)

blynk = BlynkLib.Blynk(token)

def forward(t):
    GPIO.output(m11,1)
    GPIO.output(m12,0)
    GPIO.output(m21,1)
    GPIO.output(m22,0)
    time.sleep(t)
    stop()

def stop():
    GPIO.output(m11,0)
    GPIO.output(m12,0)
    GPIO.output(m21,0)
    GPIO.output(m22,0)
        
def take_picture():
    return cam.read()

def save_picture(action):
    global last_filename,dados
    (ret,frame) = take_picture()
    frame = cv2.resize(frame,(largura_img, altura_img))
    cv2.imshow("foto", frame)
    if ret:
        last_filename = 'imagem_' + get_timestamp() + '.png'
        cv2.imwrite('camera/' + last_filename,frame)
        data.append((frame,action))
        
def get_timestamp():
    s = '{}'.format(datetime.now())
    return s.replace(" ","_").replace(":","_").replace("-","_")

#INICIAR

@blynk.VIRTUAL_WRITE(1)
def up_side(valor):
    print(valor)
    if valor[0] =="1":
        save_picture(actions[2])
        servo1.ChangeDutyCycle(frente)
        forward(sleep)
        #return last_filename
        

        
@blynk.VIRTUAL_WRITE(6)
def left_side_min(valor):
    if valor[0] =="1":
        save_picture(actions[0])
        servo1.ChangeDutyCycle(min_left)
        forward(sleep)
        #return last_filename

@blynk.VIRTUAL_WRITE(2)
def left_side_max(valor):
    if valor[0] =="1":
        save_picture(actions[1])
        servo1.ChangeDutyCycle(max_left)
        forward(sleep)
        #return last_filename

        
@blynk.VIRTUAL_WRITE(5)
def right_side_min(valor):
    if valor[0] =="1":
        save_picture(actions[3])
        servo1.ChangeDutyCycle(min_right)
        forward(sleep)
        #return last_filename
        
@blynk.VIRTUAL_WRITE(7)
def right_side_max(valor):
    if valor[0] =="1":
        save_picture(actions[4])
        servo1.ChangeDutyCycle(max_right)
        forward(sleep)
        #return last_filename
        
        
        
@blynk.VIRTUAL_WRITE(4)
def save_route(valor):
    if valor[0] == "1":
        global data_filename, data
        if len(data):
           data_filename = 'dados_{}_{}_imagens'.format(get_timestamp(),len(data))
           file = open('data/'+data_filename,'wb')
           pickle.dump(data,file)
           file.close()
           return data_filename
        
while True:
    blynk.run()
        
        
    


