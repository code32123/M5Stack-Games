import ili9342c
from machine import Pin, SPI
import os, machine

"""
By Code32123
Interfaces with the ili9342c library, but simplifies a few things
and re-asserts the baud rate before each spi interaction to
make it compatible with SDCard library
"""


class colors:
	Green = ili9342c.color565(30, 255, 0)
	Black = ili9342c.BLACK
	Red = ili9342c.RED

class Display:
	def __init__(self, spi):
		self.ScreenBaud = 60000000
		self.spi = spi
		self.spi.init(baudrate=self.ScreenBaud)
		self.tft = ili9342c.ILI9342C(
			spi,
			320,
			240,
			reset=Pin(33, Pin.OUT),
			cs=Pin(14, Pin.OUT),
			dc=Pin(27, Pin.OUT),
			backlight=Pin(32, Pin.OUT),
			rotation=0,
			buffer_size=16*32*2)
		self.tft.init()
	def text(self, font, text, x, y, color):
		self.spi.init(baudrate=self.ScreenBaud)
		self.tft.text(
			font,
			text,
			x,
			y,
			color
		)
	def fill(self, color):
		self.spi.init(baudrate=self.ScreenBaud)
		self.tft.fill(color)

	def drawIcon(self, icon, x, y, fgColor, bgColor=ili9342c.BLACK):
		self.spi.init(baudrate=self.ScreenBaud)
		spriteBuffer = bytearray(512)
		self.tft.map_bitarray_to_rgb565(icon, spriteBuffer, 16, fgColor, bgColor)
		self.tft.blit_buffer(spriteBuffer, x, y, 16, 16)	