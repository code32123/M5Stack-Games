import pygame


pygame.init()


width = 32
height = 16
cellSize = 30

window = pygame.display.set_mode((cellSize*width, (cellSize*height) + 20))
clock = pygame.time.Clock()

# myfont = pygame.font.SysFont('Comic Sans MS', 30)
myfont = pygame.freetype.SysFont('Arial', cellSize*(3/4))

rect = pygame.Rect(0, 0, cellSize, cellSize)
rect.center = ((cellSize)/2, (cellSize)/2)#window.get_rect().center

rightOK, leftOK, upOK, downOK, spaceOK, pOK = False, False, False, False, False, False

# tileToColors = [(0,0,0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)] # Empty, redWall, greenWall, goal, spawn
tileToColors = [(0,0,0), (200, 200, 200)] # 0, 1

selectedTile = 1

tiles = []
for y in range(height):
	tiles.append([])
	for x in range(width):
		tiles[y].append(0)
print('tiles', tiles)

def bundleForExport():
	global tiles
	tileExportString = ''
	for row in range(len(tiles)):
		rowStr = ''
		for column in range(len(tiles[row])):
			rowStr += str(tiles[row][column])

		workingString = rowStr
		tileExportStringMini = ''
		while len(workingString) > 0:
			tileExportStringMini += ('0b' + workingString[:8] + ', ')
			workingString = workingString[8:]
			# input(workingString)

		tileExportString += '\n\t' + tileExportStringMini

	return 'Name = bytearray([' + str(tileExportString).replace("'", "")[:-1] + '])'

run = True
while run:
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			# print(pygame.key.name(event.key))
			pass

	keys = pygame.key.get_pressed()
	
	space = bool(keys[pygame.K_SPACE])
	right = bool(keys[pygame.K_RIGHT])
	left  = bool(keys[pygame.K_LEFT])
	up    = bool(keys[pygame.K_UP])
	down  = bool(keys[pygame.K_DOWN])
	p  = bool(keys[pygame.K_p])
	if right and rightOK:
		rect.x += cellSize
		rightOK = False
	if not right and not rightOK:
		rightOK = True
	if left and leftOK:
		rect.x -= cellSize
		leftOK = False
	if not left and not leftOK:
		leftOK = True
	if up and upOK:
		rect.y -= cellSize
		upOK = False
	if not up and not upOK:
		upOK = True
	if down and downOK:
		rect.y += cellSize
		downOK = False
	if not down and not downOK:
		downOK = True
	if p and pOK:
		print(bundleForExport())
		pOK = False
	if not p and not pOK:
		pOK = True

	# rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * cellSize
	# rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * cellSize
		
	rect.centerx = (rect.centerx % (cellSize*width))
	rect.centery = (rect.centery % (cellSize*height))

	if space and spaceOK:
		tiles[int(rect.centery/cellSize)][int(rect.centerx/cellSize)] = selectedTile
		spaceOK = False
	if not space and not spaceOK:
		spaceOK = True

	window.fill(0)
	if keys[pygame.K_1]:
		selectedTile = 0
		tiles[int(rect.centery/cellSize)][int(rect.centerx/cellSize)] = selectedTile
	if keys[pygame.K_2]:
		selectedTile = 1
		tiles[int(rect.centery/cellSize)][int(rect.centerx/cellSize)] = selectedTile
	# if keys[pygame.K_3]:
	# 	selectedTile = 2
	# 	tiles[int(rect.centery/cellSize)][int(rect.centerx/cellSize)] = selectedTile
	# if keys[pygame.K_4]:
	# 	selectedTile = 3
	# 	tiles[int(rect.centery/cellSize)][int(rect.centerx/cellSize)] = selectedTile
	# if keys[pygame.K_5]:
	# 	selectedTile = 4
	# 	tiles[int(rect.centery/cellSize)][int(rect.centerx/cellSize)] = selectedTile


	for row in range(len(tiles)):
		for column in range(len(tiles[row])):
			tile = tiles[row][column]
			tempRect = pygame.Rect((column*cellSize), (row*cellSize), cellSize, cellSize)
			pygame.draw.rect(window, tileToColors[tile], tempRect, int((cellSize/20)*3))
			myfont.render_to(window, ((column*cellSize)+int((cellSize/20)*7), (row*cellSize)+int((cellSize/20)*5)), str(tile), (255, 255, 255))#, bgcolor=None, style=STYLE_DEFAULT, rotation=0, size=0)

	pygame.draw.rect(window, (255, 255, 255), rect, int(cellSize/20)) # cursor

	for i in range(len(tileToColors)):
		# print(i, tileToColors[i], 20*i)
		pygame.draw.rect(window, tileToColors[i], pygame.Rect(20*i, (cellSize*width), 20, 20))
		pygame.draw.rect(window, (255, 255, 255), pygame.Rect(20*i, (cellSize*width), 20, 20), 1)
	pygame.draw.rect(window, tileToColors[selectedTile], pygame.Rect((cellSize*height)-20, (cellSize*width), 20, 20))
		

	# print("FRAME")
	pygame.display.flip()

pygame.quit()
exit()
