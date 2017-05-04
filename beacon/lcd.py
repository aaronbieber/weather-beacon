#!/usr/bin/env python

import serial


class LCD:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)


    def clear(self):
        self.ser.write(b'\xFE\x80\xFE\x01')


    def replace(self, text):
        self.clear()
        self.ser.write(bytearray(text.encode('utf-8')))
