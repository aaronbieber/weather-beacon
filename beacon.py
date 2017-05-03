#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
from threading import Thread, Event
import sys
import requests
from pprint import pprint
import datetime

class Weather:
    def __init__(self):
        pass

    def get_all(self):
        payload = {
            'q': 'Brookline, MA',
            'APPID': '60bb49289f303baf72322f1f114e1790',
            'mode': 'json',
            'units': 'imperial',
            'cnt': '1'
        }
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily',
                     params=payload)

        return r.json()

    def get_id(self):
        data = self.get_all()

        if "list" in data \
           and len(data["list"]) \
           and "weather" in data["list"][0] \
           and len(data["list"][0]["weather"]) \
           and "id" in data["list"][0]["weather"][0]:

            return int(data["list"][0]["weather"][0]["id"])

        # Return "clear" by default
        return 800


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


def main():
    redPin   = 13
    greenPin = 16
    bluePin  = 15

    def light_cycle(run, color, blink):
        red = color[0]
        green = color[1]
        blue = color[2]

        print("Starting light with %s %s %s" % (red, green, blue))
        with Light(redPin, greenPin, bluePin) as light:
            light.set(red, green, blue)

            while run.is_set():
                if blink:
                    sleep(1)
                    light.set(0, 0, 0)
                    sleep(1)
                    light.set(red, green, blue)

                sleep(0.1)

    # This event lets us tell the thread to end.
    run = Event()
    run.set()

    try:
        prev_weather = False
        while True:
            weather = Weather()
            weather_id = weather.get_id()
            print("Got weather ID %s" % weather_id)
            blink = False

            if weather_id == 800 or weather_id == 801 or weather_id == 802:
                print("Weather is 80x clear")
                color = (0, 20, 100)
            elif weather_id == 803 or weather_id == 804:
                print("Weather is 80x cloudy")
                color = (0, 20, 100)
                blink = True
            elif weather_id >= 500 and weather_id < 600:
                print("Weather is 50x rain")
                color = (100, 0, 0)
            elif weather_id >= 600 and weather_id < 700:
                print("Weather is 60x snow")
                color = (100, 0, 0)
                blink = True

            t = Thread(target=light_cycle, args=(run, color, blink))
            t.start()
            sleep(60)

    except KeyboardInterrupt:
        print("Cleaning up...")
        run.clear()
        t.join()
        GPIO.cleanup()


def calculateStep(prevValue, endValue):
    step = endValue - prevValue
    if step:
        step = 1020 / step

    return step


def calculateVal(step, val, i):
    if step and i % step == 0:
        if (step > 0):
            val += 1
        elif (step < 0):
            val -= 1

    if val > 100:
        val = 100
    elif (val < 0):
        val = 0

    return val


def crossFade(startColor, endColor):
    global red_pwm
    global green_pwm
    global blue_pwm

    redVal = startColor[0]
    greenVal = startColor[1]
    blueVal = startColor[2]

    stepR = calculateStep(redVal, endColor[0])
    stepG = calculateStep(greenVal, endColor[1])
    stepB = calculateStep(blueVal, endColor[2])

    for i in xrange(0, 1020):
        redVal   = calculateVal(stepR, redVal, i)
        greenVal = calculateVal(stepG, greenVal, i)
        blueVal  = calculateVal(stepB, blueVal, i)

        print("%s, %s, %s" % (redVal, greenVal, blueVal))

        red_pwm.ChangeDutyCycle(redVal)
        green_pwm.ChangeDutyCycle(greenVal)
        blue_pwm.ChangeDutyCycle(blueVal)

        sleep(0.004)


if __name__ == '__main__':
    main()
