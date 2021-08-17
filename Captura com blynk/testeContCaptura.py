#VERSÃO QUE O PULSO É ENVIADO PARA O SERVO MOTOR APENAS QUANDO HOUVER MUDANÇA DE AÇÃO (jitter foi corrigido, mas algumas vezes há diferença no posicionamento do servo, o que só é corrigido quando há mudança de ação)

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
sleep = .3
largura_img = 160
altura_img = 120
actions = ['LEFT MIN','LEFT MAX','FORWARD', 'RIGHT MIN', 'RIGHT MAX'] #5, 4, 7, 9, 10
autonomous_mode = False
min_right = 5 #5
max_right = 2.5 #4
frente = 7.5 #7
min_left = 10 #8
max_left = 12.5#9

cont_f = 0
cont_minLeft = 0
cont_maxLeft = 0
cont_minRight = 0
cont_maxRight = 0


#=================================

#Pinos do GPIO Raspberry 3 model B 
m11 = 3   
m12 = 4
m21 = 27
m22 = 22
servo = 12 

GPIO.setmode(GPIO.BCM) #RASPBERRY 3 MODEL B
GPIO.setwarnings(False)

token = '_MfJJENuRHD6vBUbWZ2meluchPAWIem2' #comunicação com o controle feito no app Blynk

GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.setup(servo, GPIO.OUT)


servo1 = GPIO.PWM(servo, 50) #PWM com 50Hz => duty cycle 2.5-12.5% (0-180 graus)
servo1.start(7.5)
time.sleep(1)
servo1.ChangeDutyCycle(0)

blynk = BlynkLib.Blynk(token)

def forward(t):
    #time.sleep(t/2)
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
    if valor[0] =="1":
        global cont_f, cont_minLeft, cont_maxLeft, cont_minRight, cont_maxRight
        print(cont_f)
        save_picture(actions[2])
        if cont_f == 0:
            servo1.ChangeDutyCycle(frente)
            time.sleep(sleep/2)
            print("teste")
        servo1.ChangeDutyCycle(0)
        forward(sleep)
        cont_f = 1
        cont_minLeft = 0
        cont_maxLeft = 0
        cont_minRight = 0
        cont_maxRight = 0
        #return last_filename
        

        
@blynk.VIRTUAL_WRITE(5)
def right_side_min(valor):
    if valor[0] =="1":
        global cont_f, cont_minLeft, cont_maxLeft, cont_minRight, cont_maxRight
        save_picture(actions[3])
        if cont_minRight == 0:
            servo1.ChangeDutyCycle(min_right)
            time.sleep(sleep/2)
        servo1.ChangeDutyCycle(0)
        forward(sleep)
        cont_f = 0
        cont_minLeft = 0
        cont_maxLeft = 0
        cont_minRight = 1
        cont_maxRight = 0
        #return last_filename

@blynk.VIRTUAL_WRITE(2)
def right_side_max(valor):
    if valor[0] =="1":
        global cont_f, cont_minLeft, cont_maxLeft, cont_minRight, cont_maxRight
        save_picture(actions[4])
        if cont_maxRight == 0:
            servo1.ChangeDutyCycle(max_right)
            time.sleep(sleep/2)
        servo1.ChangeDutyCycle(0)
        forward(sleep)
        cont_f = 0
        cont_minLeft = 0
        cont_maxLeft = 0
        cont_minRight = 0
        cont_maxRight = 1

        #return last_filename

        
@blynk.VIRTUAL_WRITE(6)
def left_side_min(valor):
    if valor[0] =="1":
        global cont_f, cont_minLeft, cont_maxLeft, cont_minRight, cont_maxRight
        save_picture(actions[0])
        if cont_minLeft == 0:
            servo1.ChangeDutyCycle(min_left)
            time.sleep(sleep/2)
        servo1.ChangeDutyCycle(0)
        forward(sleep)
        cont_f = 0
        cont_minLeft = 1
        cont_maxLeft = 0
        cont_minRight = 0
        cont_maxRight = 0
        #return last_filename
        
@blynk.VIRTUAL_WRITE(7)
def left_side_max(valor):
    if valor[0] =="1":
        global cont_f, cont_minLeft, cont_maxLeft, cont_minRight, cont_maxRight
        save_picture(actions[1])
        if cont_maxLeft == 0:
            servo1.ChangeDutyCycle(max_left)
            time.sleep(sleep/2)
        servo1.ChangeDutyCycle(0)
        forward(sleep)
        cont_f = 0
        cont_minLeft = 0
        cont_maxLeft = 1
        cont_minRight = 0
        cont_maxRight = 0
        
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
        
        
    




