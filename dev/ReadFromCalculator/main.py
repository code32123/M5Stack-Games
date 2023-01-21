import machine, time
import Display
import buttons
import network, umail, time

disp.fill(Display.colors.Black)

Clk  = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
Data = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

OldClock = 1
currentMiniByte = ""
MiniBytes = []
MiniChars = []

D_BUG = False

Table = {
	'000000': "Done",
	'000001': "A",
	'000010': "B",
	'000011': "C",
	'000100': "D",
	'000101': "E",
	'000110': "F",
	'000111': "G",
	'001000': "H",
	'001001': "I",
	'001010': "J",
	'001011': "K",
	'001100': "L",
	'001101': "M",
	'001110': "N",
	'001111': "O",
	'010000': "P",
	'010001': "Q",
	'010010': "R",
	'010011': "S",
	'010100': "T",
	'010101': "U",
	'010110': "V",
	'010111': "W",
	'011000': "X",
	'011001': "Y",
	'011010': "Z",
	'011011': " ",
	'011100': "/",
	'011101': "*",
	'011110': "-",
	'011111': "+",
	'100000': "(",
	'100001': ")",
	'100010': ".",
	'100011': ",",
	'100100': "@",
	'100101': "1",
	'100110': "2",
	'100111': "3",
	'101000': "4",
	'101001': "5",
	'101010': "6",
	'101011': "7",
	'101100': "8",
	'101101': "9",
	'101110': "0",
	'101111': ":",
	'110000': "?",

	'111100': "BodyStart",
	'111101': "SubjStart",
	'111110': "ReciStart",
	'111111': "END",
}
charX, charY = 0,0

time.sleep(1)
disp.text(font_8x16, "Conecting...", charX, charY, Display.colors.White)
print("Conecting...")

sta_if = network.WLAN(network.STA_IF)

sta_if.active(True)

creds = [('SSID','PASS')]

while not sta_if.isconnected():
	for credToTest in creds:
		print("Connecting to", credToTest[0])
		sta_if.connect(credToTest[0], credToTest[1])
		i = 20
		while not sta_if.isconnected() and i > 0:
			print('.', end="")
			i -= 1
			time.sleep(0.2)
		if not sta_if.isconnected():
			sta_if.disconnect()
		else:
			break

print("Conected")
charX, charY = 0,0
disp.text(font_8x16, "Conected    ", charX, charY, Display.colors.White)
charY += 15

smtp = umail.SMTP('smtp.gmail.com', 587, username=f'{To}', password='??????????????')

print("Start")

disp.text(font_8x16, "Ready", charX, charY, Display.colors.White)
charY += 15

CurrentText = ""
MsgType = ""
MsgList = []

timeOfLastBit = False

while True:
	if buttons.buttons.getPressed() & buttons.K_SELECT:
		try:
			exec(input('GamePrompt> '))
		except Exception as err:
			print(err)
	# print(Clk.value(), Data.value())
	if (timeOfLastBit - time.ticks_ms()) < -5000 and timeOfLastBit != False:
		print("Discarding bit - timeout")
		timeOfLastBit = False
	# else:
	# 	print(timeOfLastBit - time.ticks_ms(), timeOfLastBit)
	if charX >= 300:
		charX = 0
		charY += 15
	if charY >= 220:
		charY = 0
	if Clk.value() == 1 and OldClock == 0:
		timeOfLastBit = time.ticks_ms()
		if D_BUG:
			print('Recieved Bit:', Data.value())
		if len(currentMiniByte) < 6:
			timeOfLastBit = time.ticks_ms()
			currentMiniByte += str(Data.value())

		if len(currentMiniByte) >= 6:
			timeOfLastBit = False
			MiniBytes.append(currentMiniByte)
			MiniChars.append(Table[currentMiniByte])
			
			if D_BUG:
				print('Recieved Byte:', currentMiniByte)
				print('Recieved Char:', Table[currentMiniByte])
			else:
				if Table[currentMiniByte] == "Done":
					charY += 15
					charX = 0
					print()
					if MsgType == "Message":
						MsgList.append(CurrentText)
						CurrentText = ""
					if MsgType == "Subject":
						Subj = CurrentText
						CurrentText = ""
					if MsgType == "To":
						To = CurrentText
						CurrentText = ""

				elif Table[currentMiniByte] == "BodyStart":
					print("Message: ", end="")
					charX = 0
					charY += 15
					disp.text(font_8x16, "Message: ", charX, charY, Display.colors.White)
					charX = 9*8
					MsgType = "Message"
					CurrentText = ""
				elif Table[currentMiniByte] == "SubjStart":
					print("Subject: ", end="")
					charX = 0
					charY += 15
					disp.text(font_8x16, "Subject: ", charX, charY, Display.colors.White)
					charX = 9*8
					MsgType = "Subject"
					CurrentText = ""
				elif Table[currentMiniByte] == "ReciStart":
					print("To: ", end="")
					charX = 0
					charY += 15
					disp.text(font_8x16, "To: ", charX, charY, Display.colors.White)
					charX = 4*8
					MsgType = "To"
					CurrentText = ""
				elif Table[currentMiniByte] == "END":
					# print("SEND HERE")
					break
				else:
					print(Table[currentMiniByte], end="")
					disp.text(font_8x16, str(Table[currentMiniByte]), charX, charY, Display.colors.White)
					charX += 8
					CurrentText += Table[currentMiniByte]
			currentMiniByte = ""
	OldClock = Clk.value()
	# time.sleep(0.005)

# print("DONE, EXITED")
# print(To)
# print(Subj)
# print(Msg)
if charX != 0:
	charX = 0
	CharY += 15

disp.text(font_8x16, "Sending", charX, charY, Display.colors.White)

print("Sending ... ")

smtp.to(To)
smtp.write(f"From: {From}\n")
smtp.write("To: " + To + "\n")
smtp.write("Subject: " + Subj + "\n\n")

for line in MsgList:
	smtp.write(line + "\n")

smtp.write("\n")
smtp.write("Thanks!\n")
smtp.write(f" - {From}\n")
smtp.write("(Sent from my calculator via µmail running on an ESP32)\n")
smtp.write("...\n")
smtp.send()
smtp.quit()


disp.text(font_8x16, "Sent   ", charX, charY, Display.colors.White)
