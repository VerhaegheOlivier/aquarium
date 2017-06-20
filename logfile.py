from DBClass import DbClass
from time import gmtime, strftime
import time
import RPi.GPIO as gpio
lamp1=23
lamp2=24
ven=21

gpio.setmode(gpio.BCM)
gpio.setup(lamp1, gpio.OUT)
gpio.setup(lamp2, gpio.OUT)
gpio.setup(ven, gpio.OUT)

gpio.output(lamp1,gpio.HIGH)
gpio.output(lamp2,gpio.HIGH)
gpio.output(ven, gpio.LOW)

while True:
    db = DbClass()
    tijd = strftime("%d-%m-%Y %H:%M:%S", gmtime())
    temp=db.temp()
    gemTemp=db.getGemTemp()
    for i in gemTemp[len(gemTemp)-1]:
        db.insertLog(tijd,temp,i,1)
        print("gem temp: "+str(i))
        print("temp: "+str(temp))
        if temp > i+2:
            gpio.output(ven, gpio.HIGH)
        else:
            gpio.output(ven, gpio.LOW)
        if temp < i - 2:
            gpio.output(lamp1, gpio.LOW)
            gpio.output(lamp2, gpio.LOW)
        else:
            gpio.output(lamp1, gpio.HIGH)
            gpio.output(lamp2, gpio.HIGH)
    time.sleep(180)

