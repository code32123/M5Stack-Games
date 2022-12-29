import ili9342c
from machine import Pin, SPI
import os
import machine

"""
By Code32123
Interfaces with the ili9342c library, but simplifies a few things
and re-asserts the baud rate before each spi interaction to
make it compatible with SDCard library
"""


class colors:
	Green = ili9342c.color565(30, 255, 0)
	Black = ili9342c.BLACK
	White = ili9342c.WHITE
	Red = ili9342c.RED
	Blue = ili9342c.BLUE
	def convertColor(r, g, b):
		return ili9342c.color565(r, g, b)

class Display:
	Width, Height = (320, 240)
	def __init__(self, spi):
		self.ScreenBaud = 60000000 # Default = 60000000
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
			buffer_size=16*32*2),
		self.tft.init()

	def getTFTObj(self):
		return self.tft

	def fill_rect(self, x, y, width, height, color, setBaud = True):
		x, y = int(x), int(y)
		if setBaud:
			self.spi.init(baudrate=self.ScreenBaud)
		self.tft.fill_rect(x, y, width, height, color)

	def rect(self, x, y, width, height, color, setBaud = True):
		if setBaud:
			self.spi.init(baudrate=self.ScreenBaud)
		self.tft.rect(int(x), int(y), int(width), int(height), color)

	def pixel(self, x, y, color, setBaud = True):
		x, y = int(x), int(y)
		if setBaud:
			self.spi.init(baudrate=self.ScreenBaud)
		self.tft.pixel(x, y, color)

	def text(self, font, text, x, y, color, bg = colors.Black, setBaud = True):
		x, y = int(x), int(y)
		if setBaud:
			self.spi.init(baudrate=self.ScreenBaud)
		self.tft.text(
			font,
			text,
			x,
			y,
			color,
			bg,
		)
	def fill(self, color = colors.Black, setBaud = True):
		self.spi.init(baudrate=self.ScreenBaud)
		self.tft.fill(color)

	def line(self, x0, y0, x1, y1, color, setBaud = True):
		x0, y0 = int(x0), int(y0)
		x1, y1 = int(x1), int(y1)
		if setBaud:
			self.spi.init(baudrate=self.ScreenBaud)
		self.tft.line(x0, y0, x1, y1, color)

	def vline(self, x, y, length, color, setBaud = True):
		x, y = int(x), int(y)
		if setBaud:
			self.spi.init(baudrate=self.ScreenBaud)
		self.tft.vline(x, y, length, color)

	def hline(self, x, y, length, color, setBaud = True):
		x, y = int(x), int(y)
		if setBaud:
			self.spi.init(baudrate=self.ScreenBaud)
		self.tft.hline(x, y, length, color)

	def drawIcon(self, icon, x, y, fgColor, bgColor=ili9342c.BLACK, shape=(16, 16), setBaud = True):
		x, y = int(x), int(y)
		if x >= 0 and y >= 0:
			if setBaud:
				self.spi.init(baudrate=self.ScreenBaud)
			spriteBuffer = bytearray(512)
			self.tft.map_bitarray_to_rgb565(icon, spriteBuffer, shape[0], fgColor, bgColor)
			self.tft.blit_buffer(spriteBuffer, x, y, shape[0], shape[1])	
