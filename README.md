# woodblock_weather
Japanese woodblock themed weather display for PyPortal

PyPortal project based off of the weather display code by John Park 
https://learn.adafruit.com/pyportal-weather-station/overview

This version uses data from [Dark Sky API](https://www.darksky.net), the displayed images are generated using images from
the Library of Congress, and a font from Google Fonts.

## Intsallation:  
1. Sign up for a free [Dark Sky API developer account](https://darksky.net/dev).
2. Download project zip, unzip files in to PyPortal flash memory.
3. Edit woodblock_weather.py to change `LOCATION` to your desired coordinates, and rename file to code.py  
4. Edit secrets.py to correct wifi and Dark Sky api info
5. Create a folder on your flash memory called "lib" and make sure you have the following libraries from the [Adafruit Circuitpython bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) installed:  
  * adafruit_bitmap_font  
  * adafruit_bus_device  
  * adafruit_display_text  
  * adafruit_esp32spi   
  * adafruit_pyportal  
  * adafruit_sdcard  
  * adafruit_touchscreen  
  * neopixel  
  * adafruit_io
