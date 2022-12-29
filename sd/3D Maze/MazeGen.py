import random

class MazeGenerator:
	def __init__(self):
		self.mapa = []
		self.stack = []
		self.visited = []


	def validCell(self, cellToCheck):
		x, y = cellToCheck
		return (x <= self.width-1) and (x >= 0) and (y <= self.height-1) and (y >= 0)


	def getNeighbors(self, cellToCheck):
		neighbours = []
		intermediets = []
		cellx=cellToCheck[0]
		celly=cellToCheck[1]

		if not (cellx, celly+2) in self.visited and self.validCell((cellx, celly+2)):
			neighbours.append((cellx, celly+2))
			intermediets.append((cellx, celly+1))
		if not (cellx, celly-2) in self.visited and self.validCell((cellx, celly-2)):
			neighbours.append((cellx, celly-2))
			intermediets.append((cellx, celly-1))
		if not (cellx+2, celly) in self.visited and self.validCell((cellx+2, celly)):
			neighbours.append((cellx+2, celly))
			intermediets.append((cellx+1, celly))
		if not (cellx-2, celly) in self.visited and self.validCell((cellx-2, celly)):
			neighbours.append((cellx-2, celly))
			intermediets.append((cellx-1, celly))
			
		# print('Cell', cellToCheck, 'has neighbours', neighbours)
		return neighbours, intermediets

	def genMaze(self, size=(15, 15)):
		self.height, self.width = size
		self.mapa = []
		self.stack = []
		self.visited = []
		for y in range(self.height):
			self.mapa.append([])
			for x in range(self.width):
				self.mapa[y].append(1)
				if (x == self.width-1) or (self.width == 0) or (y == self.height-1) or (self.height == 0):
					self.visited.append((x, y))


		cell = (1, 1) 													# Choose the initial cell,
		self.visited.append(cell) 											# mark it as visited
		self.stack.insert(0, cell) 											# and push it to the stack
		self.mapa[cell[0]][cell[1]] = 0
		self.spawn = (cell[0]+0.5, cell[1] + 0.5)
		self.goal = (self.width-2, self.height-2)

		while len(self.stack) > 0 and len(self.stack) < 1000: 					# While the stack is not empty
			cell = self.stack.pop(0) 										# Pop a cell from the stack and make it a current cell
			neighbours, intermediets = self.getNeighbors(cell)
			if len(neighbours) >= 1: 									# If the current cell has any neighbours which have not been visited
				self.stack.insert(0, cell) 									# Push the current cell to the stack
				randNum = random.randint(0, len(neighbours)-1)
				chosenIntermediet = intermediets[randNum] 
				chosenCell        = neighbours[randNum] 				# Choose one of the unvisited neighbours

				self.mapa[chosenCell[0]][chosenCell[1]] = 0
				self.mapa[chosenIntermediet[0]][chosenIntermediet[1]] = 0 	# Remove the wall between the current cell and the chosen cell

				self.visited.append(chosenCell) 								# Mark the chosen cell as visited
				self.stack.insert(0, chosenCell) 							# and push it to the stack

		# for i in mapa:
		# 	print(i)
		# print(goal, spawn)

		mapExportDict = {'Start': self.spawn, 'Goal': self.goal, 'Map': self.mapa}
		return mapExportDict

if __name__ == '__main__':
	MazeGenerator = MazeGenerator()
	print(MazeGenerator.genMaze())