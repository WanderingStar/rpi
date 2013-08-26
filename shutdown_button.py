#!/usr/bin/python

import os
import RPi.GPIO as GPIO
from time import sleep

LED = 23
BUTTON = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED, GPIO.OUT, initial=1)
GPIO.setup(BUTTON, GPIO.IN)

def flashLED(secs):
    GPIO.output(LED, 0)
    sleep(secs)
    GPIO.output(LED, 1)

flag = False
count = 0
while not flag:
    # check to see if the button has been pushed
    if GPIO.input(BUTTON):
        # keep track of how many successive cycles the button has been pushed
        count += 1
        if count < 5:
            # if the the button hasn't been held down long enough yet, flash the LED
            flashLED(0.25)
        else:
            # if the button has been held down long enough, trigger the shutdown
            flag = True
    # button is not pressed
    else:
        # reset the counter
        count = 0

    # check infrequently until we notice that the button has been pressed
    if count > 0:
        sleep(.25)
    else:
        sleep(5)

# let the user know that the button press has been noted
GPIO.output(LED, 0)
os.system("shutdown -h now")
sleep(3)

while True:
    flashLED(.1)
    sleep(.1)
    flashLED(.1)
    sleep(.1)
    flashLED(.1)
    sleep(.5)
