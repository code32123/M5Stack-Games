# This file is executedon every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import machine
import os
import display
from machine import Pin, SPI
import SDCard
import time
import BootSprites
import font_16x32, font_8x16
import buttons
# UNUSED:
# sd = machine.SDCard(slot=3, miso=19, mosi=23, sck=18, cs=4)
# tft = ili9342c.ILI9342C(spi, 320, 240, reset=Pin(33, Pin.OUT), cs=Pin(14, Pin.OUT), dc=Pin(27, Pin.OUT), backlight=Pin(32, Pin.OUT), rotation=0, buffer_size=16*32*2)
# tft.init()
# ScreenBaud = 60000000
# SDCardBaud = 100000

"""
By Code32123
Launcher that changes directory to the folder of a selected program on an SD card,
so that the esp32 will load the main from that folder in its cwd
"""

# Mutes Speaker Buzz
dac = machine.DAC(machine.Pin(25))
dac.write(0)


spi = SPI(2, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
disp = Display.Display(spi)
print("Boot: Screen Init Done")

sd = SDCard.SDCard(spi, Pin(4))
os.mount(sd, '/sd')
print("Boot: SD card mounted succesfully")


################################################################################## launcher code below
def launcher():
	DoneMenu = False
	DisplayDone = False
	fail = False

	menuSelection = 0
	options = []

	# prevent multi-presses
	buttonUpPressed		= False
	buttonDownPressed	= False
	buttonAPressed 		= False

	BaseApps = ['Recent', 'WebRepl', '/']

	apps = ['Recent', 'WebRepl']

	for i in os.listdir("/sd/"):
		if i != "System Volume Information":
			apps.append(i)

	apps.append('/')

	print("Boot: Available apps:", apps)
	disp.text(font_16x32, "Apps", 0, 0, Display.colors.Green)
	i = 0
	for app in apps:
		options.append(app)
		disp.text(font_8x16, app, 52, 44+(i*20), Display.colors.Green)
		i += 1
	
	while not DoneMenu:
		if not DisplayDone:
			disp.drawIcon(BootSprites.Cursor, 30, 42+menuSelection*20, Display.colors.Green)
			DisplayDone = True
		if buttons.buttons.get_pressed() & buttons.K_UP:
			if not buttonUpPressed:
				if menuSelection > 0:
					disp.drawIcon(BootSprites.Blank, 30, 42+menuSelection*20, Display.colors.Green)
					menuSelection += -1
					disp.drawIcon(BootSprites.Cursor, 30, 42+menuSelection*20, Display.colors.Green)
					buttonUpPressed = True
		else:
			buttonUpPressed = False # prevent multi-presses

		if buttons.buttons.get_pressed() & buttons.K_DOWN:
			if not buttonDownPressed:
				if menuSelection < len(apps)-1:
					disp.drawIcon(BootSprites.Blank, 30, 42+menuSelection*20, Display.colors.Green)
					menuSelection += 1
					disp.drawIcon(BootSprites.Cursor, 30, 42+menuSelection*20, Display.colors.Green)
					buttonDownPressed = True
		else:
			buttonDownPressed = False

		if buttons.buttons.get_pressed() & buttons.K_A:
			if not buttonAPressed:
				if not str(apps[menuSelection]) in BaseApps:
					print("Boot: I'm going to run " + str(apps[menuSelection]))
					print("Boot: (Saving to recents file)")
					try:
						with open('recentApp', 'w+') as f:
							f.write(str(apps[menuSelection]))
					except OSError:
						print('Boot: Could write to file')
					os.chdir('/sd/' + str(apps[menuSelection]))
				elif str(apps[menuSelection]) == 'Recent':
					print("Boot: Running most recent app: ", end='')
					try:
						with open('recentApp', 'r') as f:
							recentApp = f.read()
							print(recentApp)
							os.chdir('/sd/' + recentApp)
					except OSError:
						print('\nBoot: Could load file')
						fail = True
					pass
				elif str(apps[menuSelection]) == 'WebRepl':
					print("Boot: Pulling up WebRepl")
					import webrepl, network
					ap_if = network.WLAN(network.AP_IF)
					ap_if.active(True)
					webrepl.start()
				elif str(apps[menuSelection]) == '/':
					print("Boot: Passing to /")
				buttonAPressed = True
				if not fail:
					DoneMenu = True
				else:
					fail = False
		else:
			buttonAPressed = False



launcher()
# spi.init(baudrate=SDCardBaud)
print("Boot: cwd", os.listdir())
print("Boot: That's all folks!")