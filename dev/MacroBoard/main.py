import display
import font_8x16, font_16x32
# import buttons
# # import bluetooth

disp = disp
buttons = buttons

disp.text(
	font_16x32,
	"JMicropad",
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

keyReady = {}
def checkPresses(key):
	global keyReady
	if buttons.buttons.getDown(key):
		try:
			if keyReady[key]:
				keyReady[key] = False
				return True
		except KeyError:
			return False
	else:
		keyReady[key] = True
		return False

def safe_list_get(l, i, default):
	try:
		return l[i]
	except IndexError:
		return default


# Implements a BLE HID mouse
import time
from machine import SoftSPI, Pin
hid_services = __import__("/hid_services")
hid_services.HID_DEBUG_LEVEL = 1
Keyboard = hid_services.Keyboard

FixedEditDelay = 20

class Device:
	def __init__(self):
		# Define state
		self.keys = [0x00, 0x00, 0x00, 0x00]
		self.overflowKeys = []

		# Create our device
		self.keyboard = Keyboard("JMicropad")
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
		while True:
			# try:
			self.keys = []
			if checkPresses("A"):
				try:
					cmd = input('GamePrompt> ')
					if cmd[0] == '#': # Start with # to send keycode
						self.key3 = int(cmd.replace('#', ''))
					else:
						exec(cmd)
				except Exception as err:
					print(err)

			if checkPresses(buttons.K_SELECT):
				self.keys.append(0x1D)

			if checkPresses(buttons.K_START):
				self.keys.append(0x1B)

			if checkPresses(buttons.K_A):
				self.keys.append(0x04)

			if checkPresses(buttons.K_B):
				self.keys.append(0x05)

			if checkPresses(buttons.K_UP):
				self.keys.append(0x52)

			if checkPresses(buttons.K_DOWN):
				self.keys.append(0x51)

			if checkPresses(buttons.K_LEFT):
				self.keys.append(0x50)

			if checkPresses(buttons.K_RIGHT):
				self.keys.append(0x4F)

			empty = len(self.keys) == 0

			while len(self.keys) < 4:
				self.keys.append(0x00)

			if not empty:
				print("Keys Before:", self.keys)
				self.overflowKeys = self.keys[4:]
				self.keys         = self.keys[:4]
				print("Keys Split: ", self.keys, self.overflowKeys)

			# If connected set keys and notify
			if self.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
				self.keyboard.set_keys(self.keys[0], self.keys[1], self.keys[2], self.keys[3])
				self.keyboard.notify_hid_report()

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