import RPi.GPIO as GPIO
import sys
import time
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


#servo motor pin number
servoPIN = 11
GPIO.setup(servoPIN, GPIO.OUT) #output
p = GPIO.PWM(servoPIN, 50)# pin 11 for PWM with 50Hz

#motion sensor
GPIO.setup(13, GPIO.IN) #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)#for led

#Rfid card
reader = SimpleMFRC522()

writter = SimpleMFRC522()
try:
    while 1:
     print("Hold a tag near the reader")
     id, text = reader.read()
     print(id)
     if id==974914530910: #Rfid card value it's unique
            p.start(0)
            p.ChangeDutyCycle(12.5) #motor initial position
            time.sleep(1)
            p.ChangeDutyCycle(7.5) #motor turns 90 degree
            time.sleep(1)
            while 1:
                i=GPIO.input(13)
                if i==1:               #When output from motion sensor is HIGH
                    print("Intruder detected")
                    GPIO.output(3, 1)  #Turn ON LED
                    break
            id, text = reader.read()
            print(id)
            if id==974914530910:
                GPIO.output(3, 0) #Turn OFF LED
                p.ChangeDutyCycle(12.5) #door go back to it's previous position 
                time.sleep(1)
                print(text)

finally:
  p.stop()
  GPIO.cleanup()

#for edit rfid card 

#str = input('Enter the name')
#print('Hold the card')
#try:
#    writter.write(str)
#    print('Successfull')
#finally:
#    GPIO.cleanup()