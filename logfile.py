from DBClass import DbClass
from time import gmtime, strftime
import time
while True:
    db=DbClass()
    tijd = strftime("%H:%M:%S %d-%m-%Y", gmtime())
    temp=db.temp()
    print('temp: '+str(temp))
    db.insertLog(tijd,temp,24,1)
    time.sleep(180)

