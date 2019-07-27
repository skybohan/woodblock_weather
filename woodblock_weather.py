"""
Woodblock Weather v1.0
Code adapted from Adafruit Pyportal Weather Station code by John Park
https://learn.adafruit.com/users/johnpark

Powered by DarkSky.net
"""
import sys
import time
import board
from adafruit_pyportal import PyPortal
cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)
sys.path.append(cwd)
import woodblock_weather_graphics  # pylint: disable=wrong-import-position

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Darksky.net uses Lattitude/Longitude to get weather

LOCATION = "42.5038,-92.4347"

# Set up the Darksky api call
DATA_SOURCE = "https://api.darksky.net/forecast/"
DATA_SOURCE += secrets['darksky_token']
DATA_SOURCE += "/" + LOCATION + "?exclude=daily,hourly,flags,alerts"
DATA_LOCATION = []


# Initialize the pyportal object and let us know what data to fetch and where
# to display it
pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=DATA_LOCATION,
                    status_neopixel=board.NEOPIXEL,
                    default_bg=0x000000)

gfx = woodblock_weather_graphics.Woodblock_Weather_Graphics(pyportal.splash, am_pm=True, celsius=False)

localtile_refresh = None
weather_refresh = None
while True:
    
    if (not localtile_refresh) or (time.monotonic() - localtile_refresh) > 3600:
        try:
            print("Getting time from internet!")
            pyportal.get_local_time()
            localtile_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    # This checks the weather every 5 minutes, the most often you can check for free is ~90sec
    if (not weather_refresh) or (time.monotonic() - weather_refresh) > 300:
        try:
            value = pyportal.fetch()
            print("Response is", value)
            gfx.display_weather(value)
            weather_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    gfx.update_time()
    time.sleep(30)
