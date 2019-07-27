#Graphics module modified from Pyportal Weather Station code by John Park.
#https://learn.adafruit.com/users/johnpark

import time
import json
import board
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

cwd = ("/"+__file__).rsplit('/', 1)[0]

small_font = cwd+"/fonts/InknutAntiqua-Regular-12.bdf"
medium_font = cwd+"/fonts/InknutAntiqua-Regular-16.bdf"
large_font = cwd+"/fonts/InknutAntiqua-Bold-25.bdf"

class Woodblock_Weather_Graphics(displayio.Group):
    def __init__(self, root_group, *, am_pm=True, celsius=True):
        super().__init__(max_size=2)
        self.am_pm = am_pm
        self.celsius = celsius

        root_group.append(self)
        self._icon_group = displayio.Group(max_size=1)
        self.append(self._icon_group)
        self._text_group = displayio.Group(max_size=3)
        self.append(self._text_group)

        self._icon_sprite = None
        self._icon_file = None
        self.set_icon(cwd+"/woodblock_weather.bmp")

        self.small_font = bitmap_font.load_font(small_font)
        self.medium_font = bitmap_font.load_font(medium_font)
        self.large_font = bitmap_font.load_font(large_font)
        glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: '
        self.small_font.load_glyphs(glyphs)
        self.medium_font.load_glyphs(glyphs)
        self.large_font.load_glyphs(glyphs)
        self.large_font.load_glyphs(('°',))
        

        self.time_text = Label(self.medium_font, max_glyphs=8)
        self.time_text.x = 245
        self.time_text.y = 25
        self.time_text.color = 0xFFFFFF
        self._text_group.append(self.time_text)

        self.temp_text = Label(self.large_font, max_glyphs=6)
        self.temp_text.x = 10
        self.temp_text.y = 195
        self.temp_text.color = 0xFFFFFF
        self._text_group.append(self.temp_text)
        
        self.description_text = Label(self.small_font, max_glyphs=60)
        self.description_text.x = 10
        self.description_text.y = 225
        self.description_text.color = 0xFFFFFF
        self._text_group.append(self.description_text)
        

    def display_weather(self, weather):
        weather = json.loads(weather)

        weather_icon = weather['currently']['icon']
        self.set_icon(cwd+"/icons/"+ weather_icon +".bmp")


        self.update_time()

        temperature = weather['currently']['temperature']
        print(temperature)
        if self.celsius:
            self.temp_text.text = "%d °C" % temperature
        else:
            self.temp_text.text = "%d °F" % temperature

        description = weather['minutely']['summary']
        description = description[0].upper() + description[1:]
        print(description)
        self.description_text.text = description
        
            
            
    def update_time(self):
        """Fetch the time.localtime(), parse it out and update the display text"""
        now = time.localtime()
        hour = now[3]
        minute = now[4]
        format_str = "%d:%02d"
        if self.am_pm:
            if hour >= 12:
                hour -= 12
                format_str = format_str+" pm"
            else:
                format_str = format_str+" am"
            if hour == 0:
                hour = 12
        time_str = format_str % (hour, minute)
        print(time_str)
        self.time_text.text = time_str

    def set_icon(self, filename):
        print("Set icon to ", filename)
        if self._icon_group:
            self._icon_group.pop()

        if not filename:
            return
        if self._icon_file:
            self._icon_file.close()
        self._icon_file = open(filename, "rb")
        icon = displayio.OnDiskBitmap(self._icon_file)
        try:
            self._icon_sprite = displayio.TileGrid(icon,
                                                   pixel_shader=displayio.ColorConverter())
        except TypeError:
            self._icon_sprite = displayio.TileGrid(icon,
                                                   pixel_shader=displayio.ColorConverter(),
                                                   position=(0,0))
        self._icon_group.append(self._icon_sprite)
        board.DISPLAY.refresh_soon()
        board.DISPLAY.wait_for_frame()
