import RPi.GPIO as GPIO
import time
from test_mult_proc import f_rec #, f_busy
from datetime import datetime
from multiprocessing import Process
import subprocess
import os, signal


RecLEDPin = 18  # blue
BusyLEDPin = 23 # red
ButtonPin = 17


Recording = False
Busy = False

p_rec = Process(target=f_rec, args=(datetime.now().strftime('%H-%M-%S'),))
# p_busy = Process(target=f_busy, args=(datetime.now().strftime('%H-%M-%S'),))

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    print("setting up")
    GPIO.setup(RecLEDPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BusyLEDPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def updateStatus(ev=None):
    global Recording, Busy, p_rec
    print("time to update")
    if (not Recording and not Busy):
        Recording = True
        Busy = False
        p_rec.start()
    elif(Recording):            # R: True, B: meh
        Recording = False
        Busy = True
        p_rec.terminate()
        p_rec = Process(target=f_rec, args=(datetime.now().strftime('%H-%M-%S'),))
    else:                       # R: False, B: True
        Recording = False
        Busy = False

    GPIO.output(RecLEDPin, Recording)
    GPIO.output(BusyLEDPin, Busy)

def loop():
    print("in loop")
    GPIO.add_event_detect(ButtonPin, GPIO.FALLING, callback=updateStatus,
                          bouncetime=200)
    while True:
        time.sleep(0.1)

def destroy():
    GPIO.output(RecLEDPin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()



# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(18,GPIO.OUT)
# print "LED on"
# GPIO.output(18,GPIO.HIGH)
# time.sleep(1)
# print "LED off"
# GPIO.output(18,GPIO.LOW)