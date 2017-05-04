#!/usr/bin/env python

import RPi.GPIO as GPIO


class Light:
    def __init__(self, redPin, greenPin, bluePin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(redPin, GPIO.OUT)
        GPIO.setup(greenPin, GPIO.OUT)
        GPIO.setup(bluePin, GPIO.OUT)

        self.redPWM = GPIO.PWM(redPin, 100)
        self.greenPWM = GPIO.PWM(greenPin, 100)
        self.bluePWM = GPIO.PWM(bluePin, 100)

        self.redPWM.start(0)
        self.greenPWM.start(0)
        self.bluePWM.start(0)

    def set(self, red, green, blue):
        self.redPWM.ChangeDutyCycle(red)
        self.greenPWM.ChangeDutyCycle(green)
        self.bluePWM.ChangeDutyCycle(blue)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.cleanup()
