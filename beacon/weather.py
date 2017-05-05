#!/usr/bin/env python

from time import time
from math import floor
import requests


class Weather:
    def __init__(self):
        self.last_updated = 0
        self.data = None

    def get_data(self):
        if int(time()) - self.last_updated > 900:
            print("Data is stale; fetching...")
            payload = {
                'q': 'Brookline, MA',
                'APPID': '60bb49289f303baf72322f1f114e1790',
                'mode': 'json',
                'units': 'imperial',
                'cnt': '1'
            }
            r = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily',
                        params=payload)

            self.data = r.json()
            self.last_updated = int(time())

        return self.data

    def get_text(self):
        data = self.get_data()

        if "list" in data\
           and len(data["list"]):

            day = data["list"][0]

        desc = day["weather"][0]["description"]
        desc += " " * (16 - len(desc))

        temp = "%s/%s" % (int(day["temp"]["max"]),
                          int(day["temp"]["min"]))

        if len(desc) == 16:
            temp = (" " * (int(floor((15 - len(temp)) / 2)))) + temp
        else:
            temp = " (%s)" % temp

        return "%s%s" % (desc, temp)

    def get_id(self):
        data = self.get_data()

        if "list" in data \
           and len(data["list"]) \
           and "weather" in data["list"][0] \
           and len(data["list"][0]["weather"]) \
           and "id" in data["list"][0]["weather"][0]:

            return int(data["list"][0]["weather"][0]["id"])

        # Return "clear" by default
        return 800
