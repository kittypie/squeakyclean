import RPi.GPIO as GPIO
import time
import traceback
import os
import boto3
from datetime import datetime
from gpiozero import LightSensor
from picamera import PiCamera

GPIO.setmode(GPIO.BCM)
##
##GPIO.setup(23, GPIO.IN) #PIR
##GPIO.setup(24, GPIO.OUT) #BUzzer

ldr = LightSensor(17)
camera = PiCamera()
camera.rotation = 90
s3 = boto3.resource('s3')
##response = s3.list_buckets()

try:
    time.sleep(2) # to stabilize sensor
    while True:
        print(ldr.value)
        if ldr.value < 0.5:
            print("Motion Detected...Dispensing the toothpaste")
            camera.start_preview()
            t = datetime.now()
            timestamp=t.strftime('%b-%d-%Y_%H%M%S')
            print("Started at " + timestamp)
            print("Start : " + timestamp)
            fileName = '/home/pi/python/squeakyclean/photos/squeaky-' + timestamp + '.jpg'
            camera.capture(fileName)
            s3.meta.client.upload_file(fileName, 'squeaky-clean' ,'photos/squeaky-' + timestamp + '.jpg')
            time.sleep(2)
##            #print("Start : " , datetime.now())
            camera.stop_preview()
        else:
            print("No one brushing ... ")
##        if GPIO.input(23):
##            GPIO.output(24, True)
##            time.sleep(0.1) #Buzzer turns on for 0.5 sec
##            GPIO.output(24, False)
##            print("Motion Detected...Dispensing the toothpaste")
##            #print("Start : " , datetime.now())
        time.sleep(1) #to avoid multiple detection
##        time.sleep(0.1) #loop delay, should be less than detection delay

except Exception:
    print("Exit squeaky clean ... ")
    traceback.print_exc()
