import RPi.GPIO as GPIO

m11 = 26
m12 = 19
m21 = 20
m22 = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

while(True):
    op = input("Direção: ")
    if op == 'w':
        GPIO.output(m11,1)
        GPIO.output(m12,0)
        GPIO.output(m21,0)
        GPIO.output(m22,1)
    elif op == 's':
        GPIO.output(m11,0)
        GPIO.output(m12,0)
        GPIO.output(m21,0)
        GPIO.output(m22,0)

