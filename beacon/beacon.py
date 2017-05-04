#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep, time
from threading import Thread, Event
import sys
from pprint import pprint
import datetime
import serial
from math import floor

from .weather import Weather
from .lcd import LCD
from .light import Light

class Beacon:
    def __init__(self):
        # This event lets us tell the thread to end.
        self.running = Event()
        self.running.set()

        self.t = None
        self.lcd = LCD()
        self.weather = Weather()

        self.red_pin   = 13
        self.green_pin = 16
        self.blue_pin  = 15


    def light_cycle(self, color, blink):
        red = color[0]
        green = color[1]
        blue = color[2]

        print("Starting light with %s %s %s" % (red, green, blue))
        with Light(self.red_pin, self.green_pin, self.blue_pin) as light:
            light.set(red, green, blue)

            while self.running.is_set():
                if blink:
                    sleep(1)
                    light.set(0, 0, 0)
                    sleep(1)
                    light.set(red, green, blue)

                sleep(0.1)


    def start(self):
        try:
            prev_weather = False
            while True:
                weather_id = self.weather.get_id()
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

                self.lcd.replace(self.weather.get_text())
                self.t = Thread(target=self.light_cycle, args=(color, blink))
                self.t.start()
                sleep(60)

        except KeyboardInterrupt:
            print("Cleaning up...")
            self.running.clear()
            self.t.join()
            self.lcd.clear()
