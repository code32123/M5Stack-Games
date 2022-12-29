# This file is executedon every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import buttons
try:
	if buttons.buttons.getPressed() & buttons.K_SELECT and buttons.buttons.getPressed() & buttons.K_START:
		print("Quiting for ampy! (SELECT & START during boot)")
		raise SystemExit
except OSError:
	pass
	
runApp = True # If a startup error is detected, flip to false to give up

import time
import machine
import os
import display
from machine import Pin, SPI, I2C
import SDCard
import BootSprites
import font_16x32, font_8x16
import json
from mpu6886 import MPU6886
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
disp = display.Display(spi)
print("Boot: Screen Init Done")

sd = 0;

BaseApps = ['Recent', 'Settings', 'WebRepl', '/']
apps = ['Recent', 'Settings', 'WebRepl']

def checkKB():
	disp.fill(display.colors.Black)
	global runApp
	try:
		if buttons.buttons.getPressed() & buttons.K_SELECT and buttons.buttons.getPressed() & buttons.K_START:
			print("Quiting for ampy! (SELECT & START during boot)")
			runApp = False
	except OSError:
		disp.text(font_8x16, "Keyboard error"  , 50, 20+(16*0), display.colors.Red)
		disp.text(font_8x16, "Try re-connecting"    , 50, 20+(16*1), display.colors.Red)
		disp.text(font_8x16, "Try Again",  25, 205, display.colors.Red)
		disp.text(font_8x16, "Skip"     , 240, 205, display.colors.Red)
		disp.drawIcon(BootSprites.KeyboardError, 20, 20, display.colors.Red)
		a, b = False, False
		while not (a or b):
			a, b = buttons.buttons.getDown('A'), buttons.buttons.getDown('C')
			if (time.ticks_ms() % 2000) == 0:
				disp.drawIcon(BootSprites.KeyboardError, 20, 20, display.colors.Red)
			elif (time.ticks_ms() % 2000) == 1000:
				disp.drawIcon(BootSprites.Keyboard, 20, 20, display.colors.Red)
		if a:
			checkKB()
		else:
			runApp = False

if runApp:
	checkKB()

def checkSDCard():
	disp.fill(display.colors.Black)
	global sd, runApp
	try:
		sd = SDCard.SDCard(spi, Pin(4))
		os.mount(sd, '/sd')
		print("Boot: SD card mounted succesfully")
	except:
		disp.text(font_8x16, "SD Card error"        , 50, 20+(16*0), display.colors.Red)
		disp.text(font_8x16, "Try re-inserting"     , 50, 20+(16*1), display.colors.Red)
		disp.text(font_8x16, "Press A to try again" , 50, 20+(16*2), display.colors.Red)
		disp.text(font_8x16, "Press B to skip"      , 50, 20+(16*3), display.colors.Red)
		disp.drawIcon(BootSprites.SDError, 20, 20, display.colors.Red)
		a, b = False, False
		while not (a or b):
			try:
				a, b = buttons.buttons.getPressed() & buttons.K_A, buttons.buttons.getPressed() & buttons.K_B
			except OSError:
				checkKB()
				disp.text(font_8x16, "SD Card error"        , 50, 20+(16*0), display.colors.Red)
				disp.text(font_8x16, "Try re-inserting"     , 50, 20+(16*1), display.colors.Red)
				disp.text(font_8x16, "Press A to try again" , 50, 20+(16*2), display.colors.Red)
				disp.text(font_8x16, "Press B to skip"      , 50, 20+(16*3), display.colors.Red)
			if (time.ticks_ms() % 2000) == 0:
				disp.drawIcon(BootSprites.SDError, 20, 20, display.colors.Red)
			elif (time.ticks_ms() % 2000) == 1000:
				disp.drawIcon(BootSprites.SD, 20, 20, display.colors.Red)
		if a:
			checkSDCard()
		else:
			runApp = False

if runApp:
	checkSDCard()


################################################################################## launcher code below
def runApp(appName):
	disp.fill(display.colors.Black)
	global BaseApps, fail
	if not appName in BaseApps:
		print("Boot: I'm going to run " + appName)
		print("Boot: (Saving to recents file)")
		try:
			with open('recentApp', 'w+') as f:
				f.write(appName)
		except OSError:
			print('Boot: Could write to file')
		os.chdir('/sd/' + appName)
	elif appName == 'Settings':
		print("Boot: Running Settings")
		os.chdir('/Set/')
	elif appName == 'WebRepl':
		print("Boot: Pulling up WebRepl")
		import webrepl, network
		ap_if = network.WLAN(network.AP_IF)
		ap_if.active(True)
		webrepl.start()
		print("Boot: (Saving to recents file)")
		try:
			with open('recentApp', 'w+') as f:
				f.write(str('WebRepl'))
		except OSError:
			print('Boot: Could write to file')
	elif appName == '/':
		print("Boot: Passing to /Dev")
		print("Boot: (Saving to recents file)")
		try:
			with open('recentApp', 'w+') as f:
				f.write('/')
		except OSError:
			print('Boot: Could write to file')
		os.chdir('/Dev/')
	elif appName == 'Recent':
		print("Boot: Running most recent app: ", end='')
		try:
			with open('recentApp', 'r') as f:
				recentApp = f.read()
				print(recentApp)
				runApp(recentApp)
		except OSError:
			print('\nBoot: Could load file')
			fail = True
		pass


# @micropython.native
def launcher():
	global BaseApps, fail
	DoneMenu = False
	displayDone = False
	fail = False

	menuSelection = 0
	options = []

	# prevent multi-presses
	buttonUpPressed		= False
	buttonDownPressed	= False
	buttonAPressed 		= False

	for i in os.listdir("/sd/"):
		if i != "System Volume Information":
			apps.append(i)

	apps.append('/')

	print("Boot: Available apps:", apps)
	disp.text(font_16x32, "Apps", 0, 0, display.colors.Green)
	i = 0
	for app in apps:
		options.append(app)
		disp.text(font_8x16, app, 52, 44+(i*20), display.colors.Green)
		i += 1
	
	while not DoneMenu:
		if not displayDone:
			disp.drawIcon(BootSprites.Cursor, 30, 42+menuSelection*20, display.colors.Green)
			displayDone = True
		if buttons.buttons.getPressed() & buttons.K_UP:
			if not buttonUpPressed:
				if menuSelection > 0:
					disp.drawIcon(BootSprites.Blank, 30, 42+menuSelection*20, display.colors.Green)
					menuSelection += -1
					disp.drawIcon(BootSprites.Cursor, 30, 42+menuSelection*20, display.colors.Green)
					buttonUpPressed = True
		else:
			buttonUpPressed = False # prevent multi-presses

		if buttons.buttons.getPressed() & buttons.K_DOWN:
			if not buttonDownPressed:
				if menuSelection < len(apps)-1:
					disp.drawIcon(BootSprites.Blank, 30, 42+menuSelection*20, display.colors.Green)
					menuSelection += 1
					disp.drawIcon(BootSprites.Cursor, 30, 42+menuSelection*20, display.colors.Green)
					buttonDownPressed = True
		else:
			buttonDownPressed = False

		if buttons.buttons.getPressed() & buttons.K_A:
			if not buttonAPressed:
				runApp(str(apps[menuSelection]))
				buttonAPressed = True
				if not fail:
					DoneMenu = True
				else:
					fail = False
		else:
			buttonAPressed = False

# spi.init(baudrate=SDCardBaud)

def loadSettings(Quiet = False):
	try:
		with open('/Set/settings', 'r') as f:
			settings = json.loads(f.read())
	except Exception as err:
		print("Failed to save settings because:")
		print(err)
		print("Resetting to defaults.")
		settings = [['SSID', ''], ['Pass', '']]
	if not Quiet:
		print('Returning settings', settings)
	return settings

def loadSetting(settingName):
	settings = loadSettings(Quiet = True)
	for sett in settings:
		if sett[0] == settingName:
			print('Returning requested setting', sett)
			return sett[1]
	return False

if runApp:
	if buttons.buttons.getPressed() & buttons.K_DOWN:
		runApp('/')
	elif buttons.buttons.getPressed() & buttons.K_UP:
		runApp('Recent')
	else:
		launcher()
else:
	print("Not running launcher - see above for reasons why it was disabled")
print("Boot: cwd:", os.getcwd())
print("Boot: ls:", os.listdir())
print("Boot: That's all folks!")
