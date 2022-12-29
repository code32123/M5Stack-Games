import machine
import os
import ili9342c
from machine import Pin, SPI
import SDCard

dac = machine.DAC(machine.Pin(25))
dac.write(0)

ScreenBaud = 60000000
SDCardBaud = 100000

spi = SPI(2, baudrate=ScreenBaud, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

tft = ili9342c.ILI9342C(
	spi,
	320,
	240,
	reset=Pin(33, Pin.OUT),
	cs=Pin(14, Pin.OUT),
	dc=Pin(27, Pin.OUT),
	backlight=Pin(32, Pin.OUT),
	rotation=0,
	buffer_size=16*32*2)
tft.init()

print("Screen Init Done")

for i in range(0, 20):
	if i%2==0:
		tft.fill(ili9342c.BLACK)
	else:
		tft.fill(ili9342c.RED)

spi.init(baudrate=SDCardBaud)

sd = SDCard.SDCard(spi, Pin(4))

os.mount(sd, '/sd')
print(os.listdir("/sd"))
print(os.listdir("/sd/"))
print(os.listdir("/sd/Snakey"))
print(os.listdir("/sd/System Volume Information"))
print("SD card mounted succesfully")

print("Card Init Done")

for i in range(0, 5):
	if i%2==0:
		tft.fill(ili9342c.BLACK)
	else:
		tft.fill(ili9342c.RED)

print("Reset Baud to Screen")

spi.init(baudrate=ScreenBaud)

for i in range(0, 20):
	if i%2==0:
		tft.fill(ili9342c.BLACK)
	else:
		tft.fill(ili9342c.RED)

print("It should succeed when the baud is reset back to " + str(SDCardBaud))

spi.init(baudrate=SDCardBaud)
print(os.listdir("/sd/"))
print(os.listdir("/sd/Snakey"))
