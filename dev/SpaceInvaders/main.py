print("SI loading 1")

import time
# import random

import display
import font_16x32, font_8x16
import buttons
import sprites

GameState = "Intro Menu" # Keeps track of which stage the game is currently in
# this is generally either Intro Menu, Gameplay, or Dead

disp = disp

DisplayDone = False # Makes sure the display is only drawn once to prevent flickering
disp.fill(display.colors.Black)
# time.sleep(0.2)
spriteBuffer = bytearray(512) # Keeps track of the buffer for the sprites. Not sure how it works, but here's the example program I got it from:
#https://github.com/russhughes/ili9342c_mpy/blob/main/examples/M5STACK/bitarray.py

print("SI loading 2")

# def highScoreManager(currentScore, dificultyCode):
# 	try:
# 		with open("highScore", 'r') as f:
# 			highScoreData = json.loads(f.read())
# 			print("loading from highScore file:", highScoreData)
# 	except OSError:
# 		print("Error reading from SD")
# 		highScoreData = {}

# 	try:
# 		highScore = highScoreData[dificultyCode]
# 	except KeyError:
# 		print("Keyerror, resetting current highScore")
# 		highScoreData[dificultyCode], highScore = 0,0
# 		with open("highScore", 'w+') as f:
# 			f.write(json.dumps(highScoreData))

# 	if currentScore > highScore:
# 		highScore = currentScore
# 		highScoreData[dificultyCode] = highScore
# 		with open("highScore", 'w+') as f:
# 			f.write(json.dumps(highScoreData))
# 		print("Congrats on the highscore!")
# 	return highScore

pause = False
PauseDownRegistered = False
x, y = 50, 195
speed = 0
lives = 3
bullets = [] # {"Pos": (x, y)}
shootCooldown = time.ticks_ms()
aliens = [
	[4]
]
alienDirection = 1

def updateAliens():
	global aliens, alienDirection
	for alien in aliens:
		pass


def main():
	global DisplayDone, GameState, pause, PauseDownRegistered, x, y, speed, bullets, lives, shootCooldown
	if buttons.buttons.getPressed() & buttons.K_SELECT:
		try:
			exec(input('GamePrompt> '))
		except Exception as err:
			print(err)
	if GameState == "Intro Menu": # if your in the intro menu
		if not DisplayDone: # if the display hasn't already been drawn
			disp.fill(display.colors.Black)
			disp.text(
				font_16x32,
				"Space Invaders",
				40,
				90,
				display.colors.Green
			)
			time.sleep(0.01)
			disp.text(
				font_8x16,
				"Press Start",
				110,
				90+30,
				display.colors.Green
			)
			DisplayDone = True

		if buttons.buttons.getPressed() & buttons.K_START: # if start is pressed, erase the screen, create a snake object, clear the input stack,
			GameState = "Game Play"
			DisplayDone = False
			disp.fill(display.colors.Black) # Erase the snake

		if buttons.buttons.getPressed() & buttons.K_SELECT: # if start is pressed, erase the screen, create a snake object, clear the input stack,
			GameState = "Settings Menu"
			DisplayDone = False
			disp.fill(display.colors.Black)

		# if buttons.buttons.getPressed() & buttons.K_B:
		# 	return True
	if GameState == "Game Play":
		if not pause:
			if not DisplayDone:
				updateGame(bar=True)
				DisplayDone = True
			if buttons.buttons.getPressed() & buttons.K_LEFT:
				if speed > 0:
					speed = 0
				if speed > -15:
					speed += -2
			elif buttons.buttons.getPressed() & buttons.K_RIGHT:
				if speed < 0:
					speed = 0
				if speed < 15:
					speed += 2
			
			
			if buttons.buttons.getPressed() & buttons.K_B and (shootCooldown <= time.ticks_ms()): # Shoot
				bullets.append({"Pos": [x+14, y-8]})
				shootCooldown = time.ticks_ms() + 500
				pass

			if speed > 0:
				speed += -1
			if speed < 0:
				speed += 1
			x += speed
			if x > 285:
				x = 285
				speed = 0
			if x < 5:
				x = 5
				speed = 0

			updateGame()

			for bullet in bullets:
				if bullet['Pos'][1] > 0:
					bullet['Pos'][1] += -5
					disp.fill_rect(bullet['Pos'][0], bullet['Pos'][1], 2, 10, display.colors.Green)
				else:
					del bullet

			# updateAliens()



		# if buttons.buttons.getPressed() & buttons.K_A: # Pause
		# 	if not PauseDownRegistered:
		# 		PauseDownRegistered = True
		# 		pause = not pause
		# else:
		# 	PauseDownRegistered = False

def updateGame(bar=False):
	global x, y, bullets, lives
	if bar:
		disp.fill(display.colors.Black)
		if lives > 0:
			disp.drawIcon(sprites.PlayerIcon, 300-00, 210, display.colors.Green)
		if lives > 1:
			disp.drawIcon(sprites.PlayerIcon, 300-19, 210, display.colors.Green)
		if lives > 2:
			disp.drawIcon(sprites.PlayerIcon, 300-38, 210, display.colors.Green)
		disp.text(
			font_8x16,
			"000",
			0,
			220,
			display.colors.Green
		)
		disp.tft.hline(0, 215, 320, display.colors.Green)

	disp.fill_rect(0, 0, 320, 215, display.colors.Black, setBaud = True)
	# disp.drawIcon(sprites.PlayerP1, x   , y, display.colors.Green)
	# disp.drawIcon(sprites.PlayerP2, x+16, y, display.colors.Green)
	disp.drawIcon(sprites.Player, x, y, display.colors.Green, shape = (32, 16))


# disp.drawIcon(sprites.Ring, 80, 80, display.colors.White)
# disp.text(
# 	font_16x32,
# 	"You Died",
# 	90,
# 	90,
# 	display.colors.Red
# )

# if buttons.buttons.getPressed() & buttons.K_START:

# disp.fill(display.colors.Black)

print("SI loaded sucessfully")
while True:
	main()
	time.sleep(0.01)