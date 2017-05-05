#!/usr/bin/env python

from time import sleep
from threading import Thread, Event
from pprint import pprint
import datetime
import Queue

from .weather import Weather
from .lcd import LCD
from .light import Light


class Beacon:
    def __init__(self):
        # This event lets us tell the thread to end.
        self.q = Queue.Queue()
        self.running = Event()
        self.running.set()

        self.t = None
        self.lcd = LCD()
        self.weather = Weather()

        self.red_pin   = 13
        self.green_pin = 16
        self.blue_pin  = 15


    def log(self, message):
        time = datetime.datetime.today().strftime("%c")
        print("[%s] %s" % (time, message))


    def light_control(self):
        red = 0
        green = 0
        blue = 0
        blink = False

        with Light(self.red_pin, self.green_pin, self.blue_pin) as light:
            while self.running.is_set():
                try:
                    val = self.q.get(False)
                    red = val[0]
                    green = val[1]
                    blue = val[2]
                    blink = val[3]

                    self.log("Got new light value (%s, %s, %s, %s)" % (red,
                                                                       green,
                                                                       blue,
                                                                       blink))

                    light.set(red, green, blue)
                    self.q.task_done()
                except Queue.Empty:
                    pass

                if blink:
                    sleep(1)
                    light.set(0, 0, 0)
                    sleep(1)
                    light.set(red, green, blue)

                sleep(0.1)


    def start(self):
        try:
            prev_weather = False
            self.t = Thread(target=self.light_control)
            self.t.start()

            while True:
                weather_id = self.weather.get_id()
                self.log("Got weather ID %s" % weather_id)
                blink = False

                if weather_id == 800 or weather_id == 801 or weather_id == 802:
                    self.log("Weather is 80x clear")
                    color = (0, 20, 100)
                elif weather_id == 803 or weather_id == 804:
                    self.log("Weather is 80x cloudy")
                    color = (0, 20, 100)
                    blink = True
                elif weather_id >= 500 and weather_id < 600:
                    self.log("Weather is 50x rain")
                    color = (100, 0, 0)
                elif weather_id >= 600 and weather_id < 700:
                    self.log("Weather is 60x snow")
                    color = (100, 0, 0)
                    blink = True

                description = self.weather.get_text()
                self.log("`%s`" % description)
                self.lcd.replace(description)
                self.log("Queue (%s, %s, %s, %s)" % (color[0], color[1], color[2], blink))
                self.q.put((color[0], color[1], color[2], blink))
                sleep(60)

        except KeyboardInterrupt:
            print
            self.log("Cleaning up...")
            self.q.join()
            self.running.clear()
            self.t.join()
            self.lcd.clear()
