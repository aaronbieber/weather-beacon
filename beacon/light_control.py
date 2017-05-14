#!/usr/bin/env python

import sys
from time import sleep
from .light import Light


def usage():
    print("Usage: light_control RED GREEN BLUE")
    print("")
    print("  RED    Red value, 0-100")
    print("  GREEN  Green value, 0-100")
    print("  BLUE   Blue value, 0-100")


def main():
    if len(sys.argv) < 4:
        usage()
        sys.exit(1)

    red   = float(sys.argv[1])
    green = float(sys.argv[2])
    blue  = float(sys.argv[3])

    print("Setting lights to (%s, %s, %s)" % (red,
                                              green,
                                              blue))

    with Light(13, 16, 15) as light:
        try:
            light.set(red, green, blue)
            while True:
                sleep(0.1)

        except KeyboardInterrupt:
            print("Cleaning up...")

    sys.exit(0)
