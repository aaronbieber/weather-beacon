#!/usr/bin/env python

import datetime


def log(message):
    time = datetime.datetime.today().strftime("%c")
    print("[%s] %s" % (time, message))
