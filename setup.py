from setuptools import setup, find_packages
setup(
  name="WeatherBeacon",
  version="0.1",
  packages=find_packages(),
  entry_points={
    "console_scripts": [
        "beacon = beacon.app:run",
        "light_control = beacon.light_control:main"
    ]
  }
)
