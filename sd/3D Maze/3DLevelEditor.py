import pygame


pygame.init()


width = 9
height = 9
cellSize = 40

window = pygame.display.set_mode((cellSize*height, (cellSize*width) + 20))
clock = pygame.time.Clock()

# myfont = pygame.font.SysFont('Comic Sans MS', 30)
myfont = pygame.freetype.SysFont('Arial', cellSize*(3/4))

rect = pygame.Rect(0, 0, cellSize, cellSize)
rect.center = ((cellSize*height)/2, (cellSize*width)/2)#window.get_rect().center

rightOK, leftOK, upOK, downOK, spaceOK, pOK = False, False, False, False, False, False

tileToColors = [(0,0,0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)] # Empty, redWall, greenWall, goal, spawn

selectedTile = 1

tiles = []
for y in range(height):
	tiles.append([])
	for x in range(width):
		tiles[y].append(0)
print('tiles', tiles)

def bundleForExport():
	global tiles
	tileExportDict = {'Start': 0, 'Goal': 0, 'Map': []}
	for row in range(len(tiles)):
		tileExportDict['Map'].append([])
		for column in range(len(tiles[row])):
			tile = tiles[column][row]
			if tile in [0, 1, 2]:
				tileExportDict['Map'][row].append(tile)
			elif tile == 3:
				tileExportDict['Map'][row].append(0)
				tileExportDict['Goal'] = (row, column)
			elif tile == 4:
				tileExportDict['Map'][row].append(0)
				tileExportDict['Start'] = (row+0.5, column + 0.5)
	return tileExportDict

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
		
	rect.centerx = rect.centerx % (cellSize*width)
	rect.centery = rect.centery % (cellSize*height)

	if space and spaceOK:
		tiles[int(rect.centerx/cellSize)][int(rect.centery/cellSize)] = selectedTile
		spaceOK = False
	if not space and not spaceOK:
		spaceOK = True

	window.fill(0)
	if keys[pygame.K_1]:
		selectedTile = 0
		tiles[int(rect.centerx/cellSize)][int(rect.centery/cellSize)] = selectedTile
	if keys[pygame.K_2]:
		selectedTile = 1
		tiles[int(rect.centerx/cellSize)][int(rect.centery/cellSize)] = selectedTile
	if keys[pygame.K_3]:
		selectedTile = 2
		tiles[int(rect.centerx/cellSize)][int(rect.centery/cellSize)] = selectedTile
	if keys[pygame.K_4]:
		selectedTile = 3
		tiles[int(rect.centerx/cellSize)][int(rect.centery/cellSize)] = selectedTile
	if keys[pygame.K_5]:
		selectedTile = 4
		tiles[int(rect.centerx/cellSize)][int(rect.centery/cellSize)] = selectedTile


	for row in range(len(tiles)):
		for column in range(len(tiles[row])):
			tile = tiles[row][column]
			tempRect = pygame.Rect((row*cellSize), (column*cellSize), cellSize, cellSize)
			pygame.draw.rect(window, tileToColors[tile], tempRect, int((cellSize/20)*3))
			myfont.render_to(window, ((row*cellSize)+int((cellSize/20)*7), (column*cellSize)+int((cellSize/20)*5)), str(tile), (255, 255, 255))#, bgcolor=None, style=STYLE_DEFAULT, rotation=0, size=0)

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