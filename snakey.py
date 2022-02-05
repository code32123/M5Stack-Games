# Flickerless, control stacking snakey!

import time
import random
from machine import Pin, SPI

import ili9342c
import font_16x32, font_8x16
import buttons
import sprites

menuSelection = 0
settings = [1, 0] # Speed, Mode
settingsOptions = [[0.5,1,2], ["Normal", "Infinite"]]
tickSpeed = 6
paused = False
DeathMode = "Normal"
Gamemode = "Intro Menu" # Keeps track of which stage the game is currently in
# this is generally either Intro Menu, Gameplay, or Dead
tft = ili9342c.ILI9342C(
	SPI(2, baudrate=60000000, sck=Pin(18), mosi=Pin(23)),
	320,
	240,
	reset=Pin(33, Pin.OUT),
	cs=Pin(14, Pin.OUT),
	dc=Pin(27, Pin.OUT),
	backlight=Pin(32, Pin.OUT),
	rotation=0,
	buffer_size=16*32*2)

DisplayDone = False # Makes sure the display is only drawn once to prevent flickering
tft.init() # Initializes the display so it is blank black
tft.fill(ili9342c.BLACK)
time.sleep(0.2)
spriteBuffer = bytearray(512) # Keeps track of the buffer for the sprites. Not sure how it works, but here's the example program I got it from:
#https://github.com/russhughes/ili9342c_mpy/blob/main/examples/M5STACK/bitarray.py

def updateInputStack():
	global up, down, left, right, button, inputStack, upOpen, downOpen, rightOpen, leftOpen
	up, down, left, right = (buttons.buttons.get_pressed() & buttons.K_UP), (buttons.buttons.get_pressed() & buttons.K_DOWN), (buttons.buttons.get_pressed() & buttons.K_LEFT), (buttons.buttons.get_pressed() & buttons.K_RIGHT)
	# Manages the input stack, adding new keypresses to the stack
	if up and upOpen:
		inputStack.append(directions.UP)
		upOpen = False
	elif not up:
		upOpen = True
	if down and downOpen:
		inputStack.append(directions.DOWN)
		downOpen = False
	elif not down:
		downOpen = True
	if left and leftOpen:
		inputStack.append(directions.LEFT)
		leftOpen = False
	elif not left:
		leftOpen = True
	if right and rightOpen:
		inputStack.append(directions.RIGHT)
		rightOpen = False
	elif not right:
		rightOpen = True

def GridCellToPixel(x): # Converts a grid cell (0-19, 0-14) to coordinates across the screen
	return x*16

class directions: # Simple direction object to keep track of directions in a way that makes math on them easy.
	UP    = 0
	RIGHT = 1
	DOWN  = 2
	LEFT  = 3
	def toCoordChange(i): 
		return ((i-2)%2 * -int(((i-2)>0) - ((i-2)<0)), (i-1)%2 * int(((i-1)>0) - ((i-1)<0))) # Gets the change related to direction: left will be (-1, 0)

class snake:
	def __init__(self):
		self.body = [(3,3), (4,3), (5,3)] # LAST IS HEAD
		self.head = (5,3) # Stores the position of the snakes head
		self.direction = directions.RIGHT # Snake starts going right
		self.apple = self.genNewApple() # Start the game with a new apple
		self.tail = (2,3) # stores the position of the last peice of the snake (It isn't in the body list because it is immedietly removed - the tail keeps track of which cell needs to be erase to keep the snake moving)
		self.score = 0
		for segment in self.body:
			self.draw("body", segment[0], segment[1])
		self.draw("head", self.head[0], self.head[1])
		self.draw("apple", self.apple[0], self.apple[1])

	def draw(self, sprite, cellX, cellY):
		if sprite=="apple": # To draw an apple, pull from the sprites prgram and color it red on black (Leaving off the black will cause a CPU panic because of an unhandled C exception. Have fun!)
			tft.map_bitarray_to_rgb565(sprites.Apple, spriteBuffer, 16, ili9342c.RED, ili9342c.BLACK)
			tft.blit_buffer(spriteBuffer, GridCellToPixel(cellX), GridCellToPixel(cellY), 16, 16)
		elif sprite=="head":
			tft.map_bitarray_to_rgb565(sprites.SnakeHead, spriteBuffer, 16, ili9342c.color565(30, 255, 0), ili9342c.BLACK)
			tft.blit_buffer(spriteBuffer, GridCellToPixel(cellX), GridCellToPixel(cellY), 16, 16)
		elif sprite=="body":
			tft.map_bitarray_to_rgb565(sprites.SnakeBody, spriteBuffer, 16, ili9342c.color565(30, 255, 0), ili9342c.BLACK)
			tft.blit_buffer(spriteBuffer, GridCellToPixel(cellX), GridCellToPixel(cellY), 16, 16)
		elif sprite=="empty":
			tft.map_bitarray_to_rgb565(sprites.Blank, spriteBuffer, 16, ili9342c.color565(30, 255, 0), ili9342c.BLACK)
			tft.blit_buffer(spriteBuffer, GridCellToPixel(cellX), GridCellToPixel(cellY), 16, 16)

	def genNewApple(self): # Generates a valid apple by regenerating it until it doesn't land on a snake bit
		toCheck = (random.randint(0, 19), random.randint(0, 14))
		while toCheck in self.body:
			toCheck = (random.randint(0, 19), random.randint(0, 14))
		return toCheck

	def move(self, newDirection):
		validDirection = (self.direction % 2) != (newDirection % 2) # check if the current direction is perpendicular to the new direction
		if validDirection:
			self.direction = newDirection # only update the direction if the new direction is valid, otherwise continue the same way
		coordChange = directions.toCoordChange(self.direction) # gets the change of the new direction. both x and y will be between -1 and 1. See toCoordChange
		newCoord = (self.head[0] + coordChange[0], self.head[1] + coordChange[1]) # Find the new coord by calculating the change by adding the change to the current
		if (not newCoord in self.body) and (newCoord[0] >= 0) and (newCoord[0] <= 19) and (newCoord[1] >= 0) and (newCoord[1] <= 14) or (DeathMode != "Normal"): # if the coordinate is 'safe', and your supposed to die, then continue
			self.draw("body", self.head[0], self.head[1]) # Cover up the old head with a body segment
			self.body.append(newCoord) # Construct a tuple that represents the moved head, and append it to the end
			self.head = newCoord # update the head to be he new coordinate
			if self.apple[0] == self.head[0] and self.apple[1] == self.head[1]: # if the new head is on an apple, update the score, generate a new apple, and draw the new apple
				self.score+=1
				self.apple = self.genNewApple()
				self.draw("apple", self.apple[0], self.apple[1])
			else:
				self.tail = self.body.pop(0) # if the new head is empty, remove the tail
				self.draw("empty", self.tail[0], self.tail[1]) # and draw over the tail
			self.draw("head", self.head[0], self.head[1]) # draw a new head on the new square, overlapping the apple or empty square
		else: # if the coordinate is 'unsafe', update the gamemmode to Dead and reset the DisplayDone
			global Gamemode, DisplayDone
			Gamemode = "Dead"
			DisplayDone = False



def main():
	global DisplayDone, Gamemode, tft, spriteBuffer, gameSnake, i, up, down, left, right, upOpen, downOpen, leftOpen, rightOpen, inputStack, tickSpeed, menuSelection, settings, settingsOptions, DeathMode, paused
	if Gamemode == "Intro Menu": # if your in the intro menu
		if not DisplayDone: # if the display hasn't already been drawn
			tft.fill(ili9342c.BLACK) # fill the screen with black, draw the title and subtitle
			tft.text(
				font_16x32,
				"SNAKEY",
				100,
				90,
				ili9342c.color565(30, 255, 0)
			)
			time.sleep(0.01)
			tft.text(
				font_8x16,
				"Press Start",
				100+3,
				90+30,
				ili9342c.color565(30, 255, 0)
			)
			# tft.text(
			# 	font_8x16,
			# 	"Select Settings",
			# 	100,
			# 	90+45,
			# 	ili9342c.color565(30, 255, 0)
			# )
			DisplayDone = True

		if buttons.buttons.get_pressed() & buttons.K_START: # if start is pressed, erase the screen, create a snake object, clear the input stack,
			Gamemode = "Game Play"
			DisplayDone = False
			tft.fill(ili9342c.BLACK) # Erase the snake
			gameSnake = snake() # Create a new snake
			up, down, left, right = False, False, False, False # Keeps track of which buttons are currently pressed
			upOpen, downOpen, leftOpen, rightOpen = False, False, False, False # Keeps track of whether the buttons is already pressed, so that when you hold it down it only triggers once
			i = 0
			inputStack = []

		if buttons.buttons.get_pressed() & buttons.K_SELECT: # if start is pressed, erase the screen, create a snake object, clear the input stack,
			Gamemode = "Settings Menu"
			menuSelection = 0
			DisplayDone = False
			inputStack = []
			tft.fill(ili9342c.BLACK)

	elif Gamemode == "Settings Menu":
		if not DisplayDone: # The same as the menu, but with different text
			# tft.fill(ili9342c.BLACK)
			tft.map_bitarray_to_rgb565(sprites.Cursor, spriteBuffer, 16, ili9342c.color565(30, 255, 0), ili9342c.BLACK)
			tft.blit_buffer(spriteBuffer, GridCellToPixel(2), GridCellToPixel((menuSelection)+3), 16, 16)
			tft.text(
				font_16x32,
				"SNAKEY",
				52,
				20,
				ili9342c.color565(30, 255, 0)
			)
			tft.text(
				font_8x16,
				"Speed: " + str(settingsOptions[0][settings[0]]) + "         ",
				52,
				50,
				ili9342c.color565(30, 255, 0)
			)
			time.sleep(0.01)
			tft.text(
				font_8x16,
				"Mode:  " + str(settingsOptions[1][settings[1]]) + "         ",
				52,
				50+15,
				ili9342c.color565(30, 255, 0)
			)
			tft.text(
				font_8x16,
				"A/B is pause/unpause",
				52,
				50+30,
				ili9342c.color565(30, 255, 0)
			)
			tft.text(
				font_8x16,
				"Arrows are movement",
				52,
				50+45,
				ili9342c.color565(30, 255, 0)
			)
			tft.text(
				font_8x16,
				"Select is settings (Here)",
				52,
				50+60,
				ili9342c.color565(30, 255, 0)
			)
			tft.text(
				font_8x16,
				"Start is continue",
				52,
				50+75,
				ili9342c.color565(30, 255, 0)
			)
			DisplayDone = True

		if buttons.buttons.get_pressed() & buttons.K_START:
			Gamemode = "Intro Menu"
			DisplayDone = False
			if settingsOptions[0][settings[0]] == 0.5:
				tickSpeed = 8
			elif settingsOptions[0][settings[0]] == 1:
				tickSpeed = 4
			elif settingsOptions[0][settings[0]] == 2:
				tickSpeed = 2
			DeathMode = settingsOptions[1][settings[1]]

		updateInputStack()
		if len(inputStack) != 0:
			newestButtonPress = inputStack.pop(0)
			if newestButtonPress == directions.UP:
				if menuSelection > 0:
					tft.map_bitarray_to_rgb565(sprites.Blank, spriteBuffer, 16, ili9342c.color565(30, 255, 0), ili9342c.BLACK)
					tft.blit_buffer(spriteBuffer, GridCellToPixel(2), GridCellToPixel((menuSelection)+3), 16, 16)
					menuSelection += -1
					tft.map_bitarray_to_rgb565(sprites.Cursor, spriteBuffer, 16, ili9342c.color565(30, 255, 0), ili9342c.BLACK)
					tft.blit_buffer(spriteBuffer, GridCellToPixel(2), GridCellToPixel((menuSelection)+3), 16, 16)

			if newestButtonPress == directions.DOWN:
				if menuSelection < 1:
					tft.map_bitarray_to_rgb565(sprites.Blank, spriteBuffer, 16, ili9342c.color565(30, 255, 0), ili9342c.BLACK)
					tft.blit_buffer(spriteBuffer, GridCellToPixel(2), GridCellToPixel((menuSelection)+3), 16, 16)
					menuSelection += 1
					tft.map_bitarray_to_rgb565(sprites.Cursor, spriteBuffer, 16, ili9342c.color565(30, 255, 0), ili9342c.BLACK)
					tft.blit_buffer(spriteBuffer, GridCellToPixel(2), GridCellToPixel((menuSelection)+3), 16, 16)

			if newestButtonPress == directions.LEFT:
				if settings[menuSelection] > 0:
					settings[menuSelection] += -1
					DisplayDone = False

			if newestButtonPress == directions.RIGHT:
				if settings[menuSelection] < len(settingsOptions[menuSelection])-1:
					settings[menuSelection] += 1
					DisplayDone = False

	elif Gamemode == "Game Play":
		if paused:
			if buttons.buttons.get_pressed() & buttons.K_B: # if start is pressed, erase the screen, create a snake object, clear the input stack,
				paused = False
		else:
			i += 1
			updateInputStack()

			if i%(tickSpeed*2) == 0: # every tickSpeed frames, 
				if len(inputStack) == 0: # if there's no keypresses, let the snake continue
					gameSnake.move(gameSnake.direction) # Note that the snakes current direction is invalid, but it defaults to it's current direction
				else:
					gameSnake.move(inputStack.pop(0)) # Get and remove the first item, then advance the list to the next position
			if buttons.buttons.get_pressed() & buttons.K_A: # if start is pressed, erase the screen, create a snake object, clear the input stack,
				paused = True

	elif Gamemode == "Dead":
		if not DisplayDone: # The same as the menu, but with different text
			tft.fill(ili9342c.BLACK)
			tft.text(
				font_16x32,
				"You Died",
				90,
				90,
				ili9342c.RED
			)
			time.sleep(0.01)
			tft.text(
				font_8x16,
				"Your score was " + str(gameSnake.score),
				90+3,
				90+30,
				ili9342c.RED
			)
			DisplayDone = True

		if buttons.buttons.get_pressed() & buttons.K_START:
			Gamemode = "Game Play"
			DisplayDone = False
			tft.fill(ili9342c.BLACK)
			gameSnake = snake()
			up, down, left, right = False, False, False, False
			upOpen, downOpen, leftOpen, rightOpen = False, False, False, False # Keeps track of whether the buttons is already pressed, so that when you hold it down it only triggers once
			i = 0
			inputStack = []

		if buttons.buttons.get_pressed() & buttons.K_SELECT: # if start is pressed, erase the screen, create a snake object, clear the input stack,
			Gamemode = "Settings Menu"
			menuSelection = 0
			DisplayDone = False
			inputStack = []
			tft.fill(ili9342c.BLACK)
