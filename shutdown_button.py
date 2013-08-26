#!/usr/bin/python

# This script is used with an LED and a momentary button, perhaps the same,
# like https://www.sparkfun.com/products/10440
# The LED should be wired to GPIO pin 23 and the button to pin 24.
# The idea is that it is run at startup (for example, from rc.local)
# It turns the LED on to indicate that it's working, and then waits
# for the user to hold down the button. When the script notices that
# the user is holding down the button (which may take up to 5 seconds),
# it starts flashing the LED to confirm. If the user continues to hold
# the button down, the LED goes off and the shutdown sequence is triggered.
# While the system is shutting down (which may take some time), the LED
# does a triple flash. When it's finished shutting down, the LED will
# turn off.

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

# let the user know that the button press has been noted by turning off the LED
GPIO.output(LED, 0)
os.system("shutdown -h now")
sleep(5)

# triple flash the LED
while True:
    flashLED(.1)
    sleep(.1)
    flashLED(.1)
    sleep(.1)
    flashLED(.1)
    sleep(.5)
