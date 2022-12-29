# line(self, x0, y0, x1, y1, color)

# import random
import display
# import font_16x32, font_8x16
import buttons
# import sprites
# import json
import math
import time
from MazeGen import MazeGenerator
MazeGenerator = MazeGenerator()
# M5Stack screen is 320x240

print("3D maze!")

screenWidth = 320
screenHeight = 240

def LoadLevel():
	global currentMap, currentLevel, maps, goal, posx, posy, rot
	rot = math.pi/4
	currentMapDict = MazeGenerator.genMaze()
	print(currentMapDict)
	goal = currentMapDict['Goal']
	posx, posy = currentMapDict['Start']
	currentMap = currentMapDict['Map']
	for y in range(len(currentMap)):
		for x in range(len(currentMap[y])):
			if currentMap[x][y] == 1:
				currentMap[x][y] = (255, 0, 0)
			if currentMap[x][y] == 2:
				currentMap[x][y] = (0, 255, 0)

LoadLevel()

rot = math.pi/4
fov = 60

# disp.line(0, 0, screenWidth, screenHeight, display.colors.Black)
# disp.line(screenWidth, 0, 0, screenHeight, display.colors.Black)

def ThickLine(x1, y1, x2, y2, color):
		disp.tft.vline(x1-3, y1, y2-y1, color)
		disp.tft.vline(x1-2, y1, y2-y1, color)
		disp.tft.vline(x1-1, y1, y2-y1, color)
		disp.tft.vline(x1+0, y1, y2-y1, color)
		disp.tft.vline(x1+1, y1, y2-y1, color)
		disp.tft.vline(x1+2, y1, y2-y1, color)

def DrawLine(x, h, blockTheme, d=0):

	y1, y2 = int((-h*theExpandingConstant)+(screenHeight/2)), int((h*theExpandingConstant)+(screenHeight/2))
	if y1 < 1:
		y1 = 0
	if y2 > screenHeight:
		y2 = screenHeight - 1
	r, g, b = blockTheme[0] - d, blockTheme[1] - d, blockTheme[2] - d
	r, g, b = r if r>0 else 0, g if g>0 else 0, b if b>0 else 0, 
	ThickLine(x, y1, x, y2, display.colors.convertColor(r, g, b))

def deg2rad(deg):
	return deg * (math.pi/180)

def cosApprox(rot):
	return math.cos(rot)

def sinApprox(rot):
	return math.sin(rot)

theRandomShrinkingConstant = 0.05 # Default: 0.02
theExpandingConstant = 100 # Default: 80
moveConstant = 0.5 # Default: 0.3

def DrawScreen():
	# time1 = time.time_ns(), time.time_ns()-time1
	time1 = time.time_ns()
	global rot, posx, posy, theRandomShrinkingConstant, currentMap, screenWidth, fov
	disp.fill_rect(0, 0, int(screenWidth), int(screenHeight/2), display.colors.convertColor(135, 206, 235))
	disp.fill_rect(0, int(screenHeight/2), int(screenWidth), int(screenHeight/2), display.colors.convertColor(124, 252, 0))
	for i in range(fov+1):
		time2 = time.time_ns()
		rot_i = rot + deg2rad(i - int(fov/2))
		x, y = posx, posy
		sin, cos = (theRandomShrinkingConstant*sinApprox(rot_i), theRandomShrinkingConstant*cosApprox(rot_i))
		n = 0
		time6 = time.time_ns()
		while True:
			x, y = x + cos, y + sin
			n += 1
			if int(x) == goal[0] and int(y) == goal[1] and n%5 == 0 and i%3 == 0:
				bottom = 1/(theRandomShrinkingConstant * n)
				y2 = int((bottom*theExpandingConstant)+(screenHeight/2))
				if y2 > screenHeight:
					y2 = screenHeight - 1
				# disp.tft.pixel(int(i*(screenWidth/fov)), y2+1, display.colors.Blue)
				# disp.tft.pixel(int(i*(screenWidth/fov)), y2-1, display.colors.Blue)
				disp.tft.pixel(int(i*(screenWidth/fov)), y2, display.colors.Blue)
				# disp.tft.pixel(int(i*(screenWidth/fov))+1, y2, display.colors.Blue)
				# disp.tft.pixel(int(i*(screenWidth/fov))-1, y2, display.colors.Blue)
			if currentMap[int(x)][int(y)] != 0:
				h = 1/(theRandomShrinkingConstant * n)
				break
		time6 = time.time_ns()-time6
		time3 = time.time_ns()
		DrawLine(int(i*(screenWidth/fov)), h, currentMap[int(x)][int(y)], n)
		# print('RAY', int((time.time_ns()-time2)/1000), 'LINE', int((time.time_ns()-time3)/1000), 'NOT LINE', int((time.time_ns()-time2)/1000) - int((time.time_ns()-time3)/1000), 'InchingLoop', int(time6/1000))
	# print('FRAME', int((time.time_ns()-time1)/1000))

currentLevel = 0

DrawScreen()
while True:
	if buttons.buttons.getPressed() & buttons.K_SELECT:
		try:
			exec(input('GamePrompt> '))
		except Exception as err:
			print(err)
	if buttons.buttons.getPressed() & buttons.K_START:
		DrawScreen()
	x, y = posx, posy
	up, down, left, right, a, b = (buttons.buttons.getPressed() & buttons.K_UP), (buttons.buttons.getPressed() & buttons.K_DOWN), (buttons.buttons.getPressed() & buttons.K_LEFT), (buttons.buttons.getPressed() & buttons.K_RIGHT), (buttons.buttons.getPressed() & buttons.K_A), (buttons.buttons.getPressed() & buttons.K_B)
	if up:
		x, y = (x + moveConstant*cosApprox(rot), y + moveConstant*sinApprox(rot))
	if down:
		x, y = (x - moveConstant*cosApprox(rot), y - moveConstant*sinApprox(rot))
	if a:
		x, y = (x + moveConstant*cosApprox((math.pi/2)+rot), y + moveConstant*sinApprox((math.pi/2)+rot))
	if b:
		x, y = (x - moveConstant*cosApprox((math.pi/2)+rot), y - moveConstant*sinApprox((math.pi/2)+rot))
	if left:
		rot = rot - math.pi/8
	if right:
		rot = rot + math.pi/8
	if currentMap[int(x)][int(y)] == 0:
		posx, posy = x, y
	if int(posx) == goal[0] and int(posy) == goal[1]:
		LoadLevel()
	if left or right or up or down or a or b:
		DrawScreen()