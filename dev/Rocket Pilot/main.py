import display
import font_8x16, font_16x32
# import buttons
# # import bluetooth

disp = disp
buttons = buttons

disp.text(
	font_16x32,
	"Rocketry",
	5,
	5,
	display.colors.White
)

# keyReady = {}

# def doTouches():
# 	pass

# def checkPresses(key):
# 	global keyReady
# 	if buttons.buttons.getPressed() & key:
# 		if keyReady[key]:
# 			keyReady[key] = False
# 			return True
# 	else:
# 		keyReady[key] = True
# 		return False
# def main():
# 	if checkPresses(buttons.K_B):
# 		try:
# 			exec(input('GamePrompt> '))
# 		except Exception as err:
# 			print(err)
# 	if checkPresses(buttons.K_A):
# 		doTouches()


# print("Touch App loaded sucessfully")
# updateScreen()
# while True:
# 	main()
# 	time.sleep(0.01)

# MicroPython Human Interface Device library
# Copyright (C) 2021 H. Groefsema
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
def isDown(key):
	return buttons.buttons.getPressed() & key

keyReady = {}
def checkPresses(key):
	global keyReady
	if isDown(key):
		try:
			if keyReady[key]:
				keyReady[key] = False
				return True
		except KeyError:
			return False
	else:
		keyReady[key] = True
		return False

# RocketLaunch = [
# 	"Manual",
# 	"Stage",
# 	"Throttle",
# 	"Engines",
# 	"Sleep",	100,
# 	"Right", 	35,
# 	"Sleep",	78,
# 	"Right", 	37,
# 	"Sleep",	80,
# 	"Right", 	40,
# 	"Sleep",	84,
# 	"Right", 	38,
# 	"Done",
# ]

RocketLaunch = ["Manual","Stage","Throttle","Engines","Sleep",88,"Right",20,"Sleep",70,"Right",20,"Sleep",75,"Right",30,"Sleep",70,"Right",26,"Sleep",70,"Right",28,"Sleep",88,"Right",32,"Sleep",125,"Right",25,"Sleep",800,"Stage","Right",50,"Sleep",20,"Sleep",200,"Engines","Done"]
mode = "sequence"
RocketLaunchState = 0
RocketLaunchCounter = 0

currentDirection = 0
prevCurrentDirection = 0
# Implements a BLE HID mouse
import time
from machine import SoftSPI, Pin
Keyboard = __import__("/hid_services").Keyboard

# RocketLaunch = [(x/0.5 if type(x)==int else x) for x in RocketLaunch] # Scaling
FixedEditDelay = 20

class Device:
	def __init__(self):
		# Define state
		self.key0 = 0x00
		self.key1 = 0x00
		self.key2 = 0x00
		self.key3 = 0x00

		# Create our device
		self.keyboard = Keyboard("JKeyboard")
		# Set a callback function to catch changes of device state
		self.keyboard.set_state_change_callback(self.keyboard_state_callback)
		# Start our device
		self.keyboard.start()
		self.keyboard.set_bonding(True)
		self.keyboard.set_le_secure(True)
		self.oldState = ''

	# Function that catches device status events
	def keyboard_state_callback(self):
		if self.keyboard.get_state() is Keyboard.DEVICE_IDLE:
			return
		elif self.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:
			return
		elif self.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
			return
		else:
			return

	def keyboard_event_callback(self, bytes):
		print("Keyboard state callback with bytes: ", bytes)

	def advertise(self):
		self.keyboard.start_advertising()

	def stop_advertise(self):
		self.keyboard.stop_advertising()

	# Main loop
	def start(self): #2A = Bkspc
		global RocketLaunch, RocketLaunchState, RocketLaunchCounter, mode, currentDirection, prevCurrentDirection
		while True:
			# try:
			self.key0, self.key1, self.key2, self.key3 = 0x00, 0x00, 0x00, 0x00
			if checkPresses(buttons.K_B):
				try:
					cmd = input('GamePrompt> ')
					if cmd[0] == '#':
						self.key3 = int(cmd.replace('#', ''))
					else:
						exec(cmd)
				except Exception as err:
					print(err)

			if mode == "edit":
				if checkPresses(buttons.K_START):
					mode = "sequence"
					disp.text(font_8x16, " "*10, 5, 40, display.colors.White)
					disp.text(font_8x16, " "*10, 5, 60, display.colors.White)
					if RocketLaunch[-1] == "Sleep":
						RocketLaunch.append(RocketLaunchCounter)
					RocketLaunch.append("Done")
					RocketLaunchCounter = 0
					RocketLaunchState = 0

				NoButtonsHeld = not(isDown(buttons.K_LEFT) or isDown(buttons.K_RIGHT) or isDown(buttons.K_UP) or isDown(buttons.K_DOWN) or isDown(buttons.K_A))
				time.sleep_ms(FixedEditDelay)
				if NoButtonsHeld:
					RocketLaunchCounter += 1
					time.sleep_ms(100)
					currentDirection = "Sleep"
				elif prevCurrentDirection == "Sleep": # If buttons are still held but it's in sleep mode
					print("ADDING COMMAND", prevCurrentDirection)
					RocketLaunch.append(prevCurrentDirection)
					print("ADDING COMMAND", RocketLaunchCounter)
					RocketLaunch.append(RocketLaunchCounter)
					currentDirection = 0
					RocketLaunchCounter = 0

				if isDown(buttons.K_LEFT) and not isDown(buttons.K_RIGHT):
					RocketLaunchCounter += 1
					currentDirection = "Left"
					self.key2 = 0x14
				elif prevCurrentDirection == "Left":
					print("ADDING COMMAND", prevCurrentDirection)
					RocketLaunch.append(prevCurrentDirection)
					print("ADDING COMMAND", RocketLaunchCounter)
					RocketLaunch.append(RocketLaunchCounter)
					RocketLaunchCounter = 0

				if isDown(buttons.K_RIGHT) and not isDown(buttons.K_LEFT):
					currentDirection = "Right"
					RocketLaunchCounter += 1
					self.key2 = 0x08
				elif prevCurrentDirection == "Right":
					print("ADDING COMMAND", prevCurrentDirection)
					RocketLaunch.append(prevCurrentDirection)
					print("ADDING COMMAND", RocketLaunchCounter)
					RocketLaunch.append(RocketLaunchCounter)
					RocketLaunchCounter = 0

				if isDown(buttons.K_UP):
					currentDirection = "Throttle"
					self.key2 = 0x1D  # z (Throttle)
				elif prevCurrentDirection == "Throttle":
					print("ADDING COMMAND", prevCurrentDirection)
					RocketLaunch.append(prevCurrentDirection)
					RocketLaunchCounter = 0

				if isDown(buttons.K_DOWN):
					currentDirection = "Engines"
					self.key2 = 0x2C  # ' ' (Engines)


				if isDown(buttons.K_A):
					currentDirection = "Stage"
					self.key2 = 0x28  # Enter (Stage)


				if prevCurrentDirection != currentDirection:
					prevCurrentDirection = currentDirection
					print("ADDING COMMAND", currentDirection)
					RocketLaunch.append(currentDirection)
					if currentDirection in ["Sleep", "Left", "Right"]:
						print("ADDING COMMAND", RocketLaunchCounter)
						RocketLaunch.append(RocketLaunchCounter)
					RocketLaunchCounter = 0

				# if not (RocketLaunch[-1] == currentDirection or currentDirection == 0):
				# 	RocketLaunch.append(currentDirection)
				# 	print("ADDING COMMAND", currentDirection)
				disp.text(font_8x16, str(currentDirection) + ' ' + str(RocketLaunchCounter) + (" "*10), 5, 60, display.colors.White)

			if mode == "sequence":
				if checkPresses(buttons.K_SELECT):
					if RocketLaunch[RocketLaunchState] == "Manual":
						mode = "edit"
						RocketLaunch = ["Manual"]
						disp.text(font_8x16, "Editor" + (' '*6), 5, 40, display.colors.White)
						RocketLaunchState = 0
						RocketLaunchCounter = 0
						continue
					else:
						RocketLaunchState = 0
						RocketLaunchCounter = 0
				state = RocketLaunch[RocketLaunchState]

				textDisp = str(state)
				if str(state) in ["Left", "Right", "Sleep"]:
					nxtState = RocketLaunch[RocketLaunchState+1]
					textDisp += ' ' + str(nxtState-RocketLaunchCounter) + '/' + str(nxtState)
				if str(state) == "Manual":
					textDisp += ' ' + str(RocketLaunchCounter)
				textDisp += ' '*10
				disp.text(font_8x16, textDisp, 5, 40, display.colors.White)

				if state == "Stage":
					print("Stage")
					self.key2 = 0x28
					RocketLaunchState += 1
					
				elif state == "Throttle":
					print("Throttle")
					self.key2 = 0x1D
					RocketLaunchState += 1
					
				elif state == "Engines":
					print("Engines")
					self.key2 = 0x2C
					RocketLaunchState += 1
					
				elif state == "Left":
					RocketLaunchCounter += 1
					if RocketLaunchCounter == 2:
						print("Left |", end = '')
					if RocketLaunchCounter <= (RocketLaunch[RocketLaunchState+1]):
						self.key2 = 0x14
						print("#", end = '')
					else:
						RocketLaunchState += 2
						RocketLaunchCounter = 0
						print("|")
					
				elif state == "Right":
					RocketLaunchCounter += 1
					if RocketLaunchCounter == 2:
						print("Right |", end = '')
					if RocketLaunchCounter <= (RocketLaunch[RocketLaunchState+1]):
						self.key2 = 0x08
						print("#", end = '')
					else:
						RocketLaunchState += 2
						RocketLaunchCounter = 0
						print("|")
					
				elif state == "Sleep":
					RocketLaunchCounter += 1
					if RocketLaunchCounter == 2:
						print("Sleep |", end = '')
					if RocketLaunchCounter <= (RocketLaunch[RocketLaunchState+1]):
						time.sleep_ms(100)
						print("#", end = '')
					else:
						RocketLaunchState += 2
						RocketLaunchCounter = 0
						print("|")

				elif state == "Done":
					print("Done")
					RocketLaunchState = 0
					RocketLaunchCounter = 0

				elif state == "Manual":
					RocketLaunchCounter += 1
					# Read pin values and update variables
					if isDown(buttons.K_LEFT) or isDown(buttons.K_RIGHT) and not (isDown(buttons.K_LEFT) and isDown(buttons.K_RIGHT)):
						if isDown(buttons.K_LEFT):
							self.key0 = 0x14  # q (Left)
						else:
							self.key0 = 0x08  # e (Right)
					else:
						self.key0 = 0x00

					if (isDown(buttons.K_UP) or isDown(buttons.K_DOWN) or isDown(buttons.K_A)) and not (isDown(buttons.K_UP) and isDown(buttons.K_DOWN) and isDown(buttons.K_A)):
						if isDown(buttons.K_UP):
							self.key1 = 0x1D  # z (Throttle)
						elif isDown(buttons.K_DOWN):
							self.key1 = 0x2C  # ' ' (Engines Toggle)
						else:
							self.key1 = 0x28  # Enter (Stage)
					else:
						self.key1 = 0x00
					if checkPresses(buttons.K_START):
						RocketLaunchState += 1
						RocketLaunchCounter = 0

			if self.oldState != str(self.key0) + str(self.key1) + str(self.key2) + str(self.key3):
				self.oldState = str(self.key0) + str(self.key1) + str(self.key2) + str(self.key3)
				# If connected set keys and notify
				if self.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
					self.keyboard.set_keys(self.key0, self.key1, self.key2, self.key3)
					self.keyboard.notify_hid_report()

			# If the variables changed do something depending on the device state
			# if (self.key0 != 0x00) or (self.key1 != 0x00) or (self.key2 != 0x00) or (self.key3 != 0x00):
				# If idle start advertising for 30s or until connected
				if self.keyboard.get_state() is Keyboard.DEVICE_IDLE:
					self.keyboard.start_advertising()
					i = 10
					while i > 0 and self.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:
						time.sleep(3)
						i -= 1
					if self.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:
						self.keyboard.stop_advertising()

			if self.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
				time.sleep_ms(20)
			else:
				time.sleep(2)
			# except TypeError as err:
			# 	print(err)

	def send_char(self, char):
		if char == " ":
			mod = 0
			code = 0x2C
		elif ord("a") <= ord(char) <= ord("z"):
			mod = 0
			code = 0x04 + ord(char) - ord("a")
		elif ord("A") <= ord(char) <= ord("Z"):
			mod = 1
			code = 0x04 + ord(char) - ord("A")
		else:
			assert 0

		self.keyboard.set_keys(code)
		self.keyboard.set_modifiers(left_shift=mod)
		self.keyboard.notify_hid_report()
		time.sleep_ms(2)

		self.keyboard.set_keys()
		self.keyboard.set_modifiers()
		self.keyboard.notify_hid_report()
		time.sleep_ms(2)


	def send_string(self, st):
		for c in st:
			self.send_char(c)

	# Only for test
	def stop(self):
		self.keyboard.stop()

	# Test routine
	def test(self):
		time.sleep(5)
		self.keyboard.set_battery_level(50)
		self.keyboard.notify_battery_level()
		time.sleep_ms(2)

		# Press Shift+W
		self.keyboard.set_keys(0x1A)
		self.keyboard.set_modifiers(right_shift=1)
		self.keyboard.notify_hid_report()

		# release
		self.keyboard.set_keys()
		self.keyboard.set_modifiers()
		self.keyboard.notify_hid_report()
		time.sleep_ms(500)

		# Press a
		self.keyboard.set_keys(0x04)
		self.keyboard.notify_hid_report()

		# release
		self.keyboard.set_keys()
		self.keyboard.notify_hid_report()
		time.sleep_ms(500)

		# Press s
		self.keyboard.set_keys(0x16)
		self.keyboard.notify_hid_report()

		# release
		self.keyboard.set_keys()
		self.keyboard.notify_hid_report()
		time.sleep_ms(500)

		# Press d
		self.keyboard.set_keys(0x07)
		self.keyboard.notify_hid_report()

		# release
		self.keyboard.set_keys()
		self.keyboard.notify_hid_report()
		time.sleep_ms(500)

		self.send_string(" Hello World")

		self.keyboard.set_battery_level(100)
		self.keyboard.notify_battery_level()

d = Device()
d.start()