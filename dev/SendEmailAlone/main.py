import network, umail, time
import display
import font_8x16, font_16x32
import buttons

disp = disp

class GUIinput():
	def __init__(self, name='', position = (50, 0), color = display.colors.White, inputType = 'String', value = '', label = '', labelPosition = 'undefined', labelColor = display.colors.White):
		self.name = name
		self.focusState = False
		self.value = value
		self.inputType = inputType
		self.color = color
		self.position = position
		self.label = label
		if labelPosition == 'undefined':
			self.labelPosition = (position[0] - 45, position[1])
		else:
			self.labelPosition = labelPosition
		self.labelColor = labelColor

	def processKey(self, key):
		if key == '<':
			self.value = self.value[:-1]
			self.Draw(True)
		else:
			self.value += key
			self.Draw()

	def focus(self):
		self.focusState = True
	def unFocus(self):
		self.focusState = False
	def setFocus(self, focusState):
		self.focusState = focusState
		self.Draw()
	def Draw(self, delMode = False, bg = False):
		if bg or self.inputType == 'Button':
			disp.fill_rect(self.position[0], self.position[1]-2, 200, 20, display.colors.convertColor(20, 20, 20))
		if not self.label == '':
			disp.text(
				font_8x16,
				self.label,
				self.labelPosition[0],
				self.labelPosition[1],
				self.labelColor
			)
		disp.text(
			font_8x16,
			self.value + ((' ') if delMode else ''),
			self.position[0] + 5,
			self.position[1],
			self.color,
			display.colors.convertColor(20, 20, 20) if (bg or self.inputType == 'Button') else display.colors.convertColor(0, 0, 0)
			
		)
		if self.focusState:
			disp.rect(self.position[0], self.position[1]-2, 200, 20, display.colors.convertColor(255, 255, 255))
		else:
			disp.rect(self.position[0], self.position[1]-2, 200, 20, display.colors.convertColor(100, 100, 100))

# settings = loadSettings()

sta_if = network.WLAN(network.STA_IF)

sta_if.active(True)

sta_if.connect(loadSetting('SSID'), loadSetting('Pass'))

inputValues = ['', '', '']

disp.text(
	font_16x32,
	"Con Wi-Fi",
	5,
	5,
	display.colors.White
)


print('NoConn, delaying', end='')
while not sta_if.isconnected():
	print('.', end='')
	time.sleep(0.1)
print()
print('Connected')

disp.text(
	font_16x32,
	"Con MailS",
	5,
	5,
	display.colors.White
)

smtp = umail.SMTP('smtp.gmail.com', 587, username=f'{From}', password='????????????????')

disp.text(
	font_16x32,
	"Email    ",
	5,
	5,
	display.colors.White
)

toInput =    GUIinput(name = 'ToInput'     , position = (50,  40), label = 'To: ')
subInput =   GUIinput(name = 'SubjectInput', position = (50,  62), label = 'Sub:')
msgInput =   GUIinput(name = 'MsgInput'    , position = (50,  84), label = 'Msg:')
sendButton = GUIinput(name = 'DoneButton'  , position = (50, 106), value = 'Send', inputType = 'Button')

Inputs = [toInput, subInput, msgInput, sendButton]

selection = 0
buttonUpReady = True
buttonDownReady = True
typeMode = False

KeyBoard = [
	['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '*'],
	['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', ''],
	['k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', '^'],
	['u', 'v', 'w', 'x', 'y', 'z', '.', ',', '@', ' ', '<'],
]

KeyBoardCaps = [
	['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '*'],
	['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', ''],
	['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', '_'],
	['U', 'V', 'W', 'X', 'Y', 'Z', '.', ',', '@', ' ', '<'],
]

letterMatrixCol, letterMatrixRow = 0, 0
keyReady = {}
caps = False

def checkPresses(key):
	global keyReady
	if buttons.buttons.getPressed() & key:
		if keyReady[key]:
			keyReady[key] = False
			return True
	else:
		keyReady[key] = True
		return False

def updateScreen(clr = False):
	if clr:
		disp.fill()
		disp.text(font_16x32, "Email", 5, 5, display.colors.White)
	global Inputs, selection, typeMode, letterMatrixCol, letterMatrixRow, caps
	if not typeMode:
		for elementI in range(len(Inputs)):
			element = Inputs[elementI]
			if elementI == selection:
				element.setFocus(True)
			else:
				element.setFocus(False)
			element.Draw()
	else:
		drawKB(letterMatrixCol, letterMatrixRow)

def drawKB(letterCol, letterRow):
	global caps, KeyBoard, KeyBoardCaps
	useKB = KeyBoardCaps if caps else KeyBoard
	kbPos = (10, 150)
	kbScale = (1.5, 1)
	for rowI in range(len(useKB)):
		row = useKB[rowI]
		for keyI in range(len(row)):
			key = row[keyI]
			disp.text(
				font_8x16,
				key,
				(keyI*18*kbScale[0]) + 10 + kbPos[0],
				(rowI*18*kbScale[1]) + 2 + kbPos[1],
				display.colors.White
			)
			if keyI == letterCol and rowI == letterRow:
				color = display.colors.convertColor(255, 255, 255)
			else:
				color = display.colors.convertColor(100, 100, 100)
			disp.rect((keyI*18*kbScale[0]) + 1 + kbPos[0], (rowI*18*kbScale[1]) + 1 + kbPos[1], 18*kbScale[0], 18*kbScale[1], color) 

def sendEmail():
	global inputValues
	smtp = umail.SMTP('smtp.gmail.com', 587, username=f'{From}', password='???????????????')
	smtp.to(f'To')

	smtp.write(f"From: {from}\n")
	smtp.write("To: <" + inputValues[0] + ">\n")
	smtp.write("Subject: " + inputValues[1] + "\n\n")
	smtp.write(inputValues[2])
	smtp.write("...\n")
	smtp.send()
	smtp.quit()


def main():
	global selection, buttonUpReady, buttonDownReady, typeMode, letterMatrixCol, letterMatrixRow, inputValues
	global caps
	global KeyBoard
	global KeyBoardCaps
	if checkPresses(buttons.K_B):
		try:
			exec(input('GamePrompt> '))
		except Exception as err:
			print(err)

	if checkPresses(buttons.K_START):
		updateScreen()

	if not typeMode == True:
		if checkPresses(buttons.K_SELECT):
			if Inputs[selection].name == 'DoneButton':
				sendEmail()
			else:
				typeMode = True
				updateScreen()

		if checkPresses(buttons.K_UP):
			if buttonUpReady:
				if selection > 0:
					selection += -1
					updateScreen()
				buttonUpReady = False
		else:
			buttonUpReady = True
		if checkPresses(buttons.K_DOWN):
			if buttonDownReady:
				if selection < len(Inputs)-1:
					selection += 1
					updateScreen()
					buttonDownReady = False
		else:
			buttonDownReady = True
	else:
		if checkPresses(buttons.K_UP):
			if letterMatrixRow > 0:
				letterMatrixRow += -1
			else:
				letterMatrixRow = len(KeyBoard)-1
			updateScreen()
		if checkPresses(buttons.K_DOWN):
			if letterMatrixRow < len(KeyBoard)-1:
				letterMatrixRow += 1
			else:
				letterMatrixRow = 0
			updateScreen()

		if checkPresses(buttons.K_LEFT):
			if letterMatrixCol > 0:
				letterMatrixCol += -1
			else:
				letterMatrixCol = len(KeyBoard[0])-1
			updateScreen()
		if checkPresses(buttons.K_RIGHT):
			if letterMatrixCol < len(KeyBoard[0])-1:
				letterMatrixCol += 1
			else:
				letterMatrixCol = 0
			updateScreen()

		if checkPresses(buttons.K_A):
			useKB = KeyBoardCaps if caps else KeyBoard
			key = useKB[letterMatrixRow][letterMatrixCol]
			print(key)
			if key == '^':
				caps = True
				updateScreen()
			elif key == '_':
				caps = False
				updateScreen()
			elif key == '*':
				inputValues[selection] = Inputs[selection].value
				print(inputValues)
				typeMode = False
				updateScreen(clr = True)
			else:
				Inputs[selection].processKey(key)

print("Email App loaded sucessfully")
updateScreen()
while True:
	main()
	time.sleep(0.01)
