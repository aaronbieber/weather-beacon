# Weather Beacon

A small Python project utilizing GPIO pins on the Raspberry Pi to blink a
weather beacon similar to the one at the top of Boston's Berkeley Building.

## Installing

Set up a virtual environment, install the requirements, and run. This will only
work on a Raspberry Pi because it uses the RPi.GPIO library, which either fails
or does nothing on any other device.

From this project's root:

```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python beacon.py
```

## License

This project is made available under the permissive terms of the GPL-compatible
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE. For (not much) more detail, see
LICENSE.txt in this directory.
