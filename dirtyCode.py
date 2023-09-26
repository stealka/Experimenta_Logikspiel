# version 0.3

import pygame
import time
import copy

PINK	= ( 242,  82, 120)
RED     = ( 255,   0,   0)
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
GREEN   = (   0, 255,   0)

COLORS = [WHITE, BLACK, RED]

RESOLUTION = (800, 600)
BALL_RADIUS = 50
BALL_SMALLMARK = 3
BALL_BIGMARK = 10
BALL_NOMARK = 0
BALL_DISTANCE = 30

COORDS = [	(0,0),						(4,0),
			(0,1), (1,1), (2,1), (3,1), (4,1),
			(0,2),		  (2,2),		(4,2),
			(0,3),						(4,3)]

START = [1, 2, 1, 0, 0, 0, 2, 1, 0, 2, 1, 2]
GOAL =  [2, 1, 2, 0, 0, 0, 1, 2, 0, 1, 2, 1]

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
pygame.display.set_caption("experimenta")
font = pygame.font.SysFont(None, 24)

def distance(p0, p1):
	return ((p0[0]-p1[0])**2 + (p0[1]-p1[1])**2)**0.5

class Ball:
	def __init__(self, id):
		self.id = id
		self.color = START[id]
		self.position = ((BALL_DISTANCE + 2*BALL_RADIUS) * (COORDS[self.id][0]+1), (BALL_DISTANCE + 2*BALL_RADIUS) * (COORDS[self.id][1]+1))
		self.selected = BALL_NOMARK

		self.neighbours = []
		for index in range(len(COORDS)):
			if self.id != index:
				if abs(COORDS[self.id][0]-COORDS[index][0]) == 1 and abs(COORDS[self.id][1]-COORDS[index][1]) == 0:
					self.neighbours.append(index)
				elif abs(COORDS[self.id][0]-COORDS[index][0]) == 0 and abs(COORDS[self.id][1]-COORDS[index][1]) == 1:
					self.neighbours.append(index)

	def draw(self):
		pygame.draw.circle(screen, COLORS[self.color], self.position, BALL_RADIUS)
		if self.selected > BALL_NOMARK:
			pygame.draw.circle(screen, GREEN, self.position, BALL_RADIUS, self.selected)

	def select(self, isMarked=True):
		if isMarked:
			self.selected = BALL_BIGMARK
		else:
			self.selected = BALL_NOMARK

class BallGame:
	def __init__(self):
		self.counter = 0
		self.isBallSelected = False
		self.selectedBall = Ball(0)

		self.balls = []
		for coord in COORDS:
			self.balls.append(Ball(len(self.balls)))

	def draw(self):
		screen.fill(PINK)
		for ball in self.balls:
			ball.draw()
		img = font.render('Moves: '+str(self.counter), True, BLACK)
		screen.blit(img, (20, 20))

	def move(self, ball):
		if not self.isBallSelected and ball.color != 0:
			ball.select()
			checkBalls = []
			checkBalls.append(ball.id)
			while len(checkBalls) > 0:
				for selectableBall in self.balls[checkBalls[0]].neighbours:
					if self.balls[selectableBall].color == 0 and self.balls[selectableBall].selected == BALL_NOMARK:
						self.balls[selectableBall].selected = BALL_SMALLMARK
						checkBalls.append(selectableBall)
				checkBalls.pop(0)

			self.selectedBall = ball
			self.isBallSelected = True

		elif self.isBallSelected and ball.selected == BALL_BIGMARK:
			for ball in self.balls:
				ball.select(False)
			self.isBallSelected = False

		elif self.isBallSelected and ball.selected == BALL_SMALLMARK:
			ball.color = self.selectedBall.color
			self.selectedBall.color = 0
			for ball in self.balls:
				ball.select(False)
			self.isBallSelected = False
			self.counter += 1

	# def getMoves(self):
	# 	possibleMoves = []
	# 	for ball in self.balls:
	# 		if ball.color is not WHITE:
	# 			ball.select()
	# 			for possibleMove in self.balls:
	# 				if possibleMove.selected == BALL_SMALLMARK:
	# 					possibleMoves.append((ball.coord, possibleMove.coord))
	# 			for deselectBall in self.balls:
	# 				deselectBall.select(False)
	# 	return possibleMoves

	def clicked(self, position):
		for ball in self.balls:
			if distance(position, ball.position) < BALL_RADIUS:
				self.move(ball)
				break;

	def setState(self, state):
		for i in range(len(self.balls)):
			self.balls[i].color = state[i]
			self.balls[i].selected = BALL_NOMARK
			self.isBallSelected = False

	def getState(self):
		state = []
		for i in range(len(self.balls)):
			state.append(self.balls[i].color)
		return state

class State:
	def __init__(self, id, inputState, parent, moves):
		self.id = id
		self.state = inputState
		self.parent = parent
		self.distanceToStart = moves
		self.distanceToGoal = 0
		self.stateValue = 0
		self.calculateDistance()

	def calculateDistance(self):
		self.distanceToGoal = 0
		noWhite = True
		for index in range(len(self.state)):
			if self.state[index] != GOAL[index]:
				self.distanceToGoal += 1
				if self.state[index] == 0:
					noWhite = False
		if noWhite:
			self.distanceToGoal += 1
		self.stateValue = self.distanceToStart + self.distanceToGoal

	def updateParent(self, newParent, newMoves):
		self.parent = newParent
		self.distanceToStart = newMoves
		self.calculateDistance()

	def getNeighbours(self):
		neighbours = []
		myGame = BallGame()
		for position in range(len(GOAL)):
			myGame.setState(self.state)
			myGame.move(myGame.balls[position])
			moves = []
			for move in range(len(GOAL)):
				if myGame.balls[move].selected == BALL_SMALLMARK:
					moves.append(move)
			for move in moves:
				myGame.setState(self.state)
				myGame.move(myGame.balls[position])
				myGame.move(myGame.balls[move])
				neighbours.append(myGame.getState())
		return neighbours

def main():
	solving = True
	running = True
	ballGame = BallGame()

	if solving:
		states = []
		checkStates = []
		states.append(State(0, copy.deepcopy(ballGame.getState()), 0, 0))
		checkStates.append(0)

		counter = 0

		while running:
			stateToBeCalculated = 0
			stateValue = -1
			for stateId in checkStates:
				if stateValue == -1 or states[stateId].stateValue < stateValue:
					stateValue = states[stateId].stateValue
					stateToBeCalculated = states[stateId].id
			checkStates.remove(stateToBeCalculated)

			stateNeighbours = states[stateToBeCalculated].getNeighbours()
			for stateNeighbour in stateNeighbours:
				if stateNeighbour == GOAL:
					running = False
					print(str(states[stateToBeCalculated].distanceToStart + 1) + " moves needed!")
					
					break

				stateInList = False
				for state in states:
					if state.state == stateNeighbour:
						if state.distanceToStart > states[stateToBeCalculated].distanceToStart + 1:
							state.updateParent(stateToBeCalculated, states[stateToBeCalculated].distanceToStart + 1)
						stateInList = True
						break
				if not stateInList:
					newId = len(states)
					states.append(State(newId, stateNeighbour, stateToBeCalculated, states[stateToBeCalculated].distanceToStart + 1))
					checkStates.append(newId)

			if len(checkStates) == 0:
				print("no solution found")
				running = False

	while running:
		# check and progress input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				ballGame.clicked(pygame.mouse.get_pos())

		# update window
		ballGame.draw()
		pygame.display.flip()
		clock.tick(30)

	pygame.quit()

if __name__ == "__main__":
	main()