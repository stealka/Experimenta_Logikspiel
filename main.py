#!python

#####   ABOUT   #####################################################
#                                                                   #
# Brief descritption (ToDo)                                         #
#                                                                   #
# ----------------------------------------------------------------- #
#   Version:    0.1  - Basic gameplay mechanic              | MSU | #
#               0.2  - Rework and code documentation        | SKA | #
#               0.3  - Rework optimize memory               | MSU | #
# ----------------------------------------------------------------- #
#                                                                   #
#####################################################################

# -- IMPORTS --------------------------------------------------------
import pygame
import time
import copy

# -- DEFINES --------------------------------------------------------
BLACK    = (   0,   0,   0)
LH_BLACK = ( 153, 153, 153)
RED      = ( 255,   0,   0)
LH_RED   = ( 255, 153, 153)
GREEN    = (   0, 255,   0)
WHITE    = ( 255, 255, 255)


RESOLUTION = ( 800, 600)
BG_COLOUR  = ( 242,  82, 120)

BALL_RADIUS    = 50
BALL_MARK_S    =  3
BALL_MARK_L    = 10
BALL_NOMARK    =  0
BALL_DISTANCE  = 30

# Colours - Playfield, Player1, Player2
COLOURS = [WHITE, BLACK, RED]

# Playingfield coordinations - Level 1
COORDS = [  (0,0),                      (4,0),
            (0,1), (1,1), (2,1), (3,1), (4,1),
            (0,2),        (2,2),        (4,2),
            (0,3),                      (4,3)]

# Start and goal constellation - Level 1
START = [1, 2, 1, 0, 0, 0, 2, 1, 0, 2, 1, 2]
GOAL =  [2, 1, 2, 0, 0, 0, 1, 2, 0, 1, 2, 1]

# -- GENERAL PYGAME SETTINGS ----------------------------------------
# Initializing pygame module
pygame.init()
# Set Window Caption
pygame.display.set_caption("Experimenta Logikspiel")

# -- GLOBAL VARIABLES -----------------------------------------------
g_font = pygame.font.SysFont(None, 24) 
g_screen = pygame.display.set_mode(RESOLUTION)
g_clock = pygame.time.Clock()

# -- CLASSES --------------------------------------------------------
class Ball:
    """ The class Ball
    defines a single ball field item which can function as a token ball
    or a free field during one game.
    """
    def __init__(self, id):
        """
        Function Ball.__init__(self, id):
        Creates main properties of a circle field with given properties
        from a defined playing field id -> COORDS[id]

        param[in]   id   Playfield Array id with circle properties
                            (see COORDS[])
        """
        # Setting up circle properties from given COORDS[] and id
        self.id         = id
        self.colour     = START[id]
        self.position   = ((BALL_DISTANCE + 2*BALL_RADIUS) * (COORDS[self.id][0]+1),
                           (BALL_DISTANCE + 2*BALL_RADIUS) * (COORDS[self.id][1]+1))
        self.selected   = BALL_NOMARK
        self.neighbours = []

        # Iterate through all balls 
        for index in range(len(COORDS)):
            if self.id != index:
                # Check the ball for neighbour balls
                # Horizontal check
                if (abs(COORDS[self.id][0]-COORDS[index][0]) == 1
                and abs(COORDS[self.id][1]-COORDS[index][1]) == 0):
                    self.neighbours.append(index)

                # Vertical check
                elif (abs(COORDS[self.id][0]-COORDS[index][0]) == 0
                  and abs(COORDS[self.id][1]-COORDS[index][1]) == 1):
                    self.neighbours.append(index)

    def draw(self):
        """
        Function Ball.draw(self):
        Simple draw function that places the circle on a new canvas frame.
        Depending on the status of the selection property the circle gets highlighted
        with an additional rim.
        """
        pygame.draw.circle(g_screen, COLOURS[self.colour], self.position, BALL_RADIUS)
        if self.selected > BALL_NOMARK:
            pygame.draw.circle(g_screen, GREEN, self.position, BALL_RADIUS, self.selected)


    def select(self, isMarked=True):
        """
        Function Ball.select(self, isMarked):
        Sets or unsets property "selected" of the Ball. If Ball is selected (isMarked=True)
        the respective mark gets set and checkMove() gets called.
        Otherwise the mark will be removed.

        param[in]   isMarked    selection value (boolean) | Default: TRUE
        """
        if isMarked:
            self.selected = BALL_MARK_L
        else:
            self.selected = BALL_NOMARK

class Game:
    def __init__(self):
        """
        Function Game.__init__(self):
        Creates main relations of the individual balls in COORDS and unites them in a
        game context. This is done by initally adding all available balls of COORDS to
        one array that is used as a reference during the game.
        Secondly, the same array is used to determine all neighbours for each ball
        horizontally as well as vertically by iterating through the array.
        Furthermore some game variable get declared.
        """
        self.counter = 0                        # Moves counter for the game
        self.isBallSelected = False             # Boolean value if a ball is selected 
        self.selectedBall = Ball(0)             # Variable to hold the selected ball object
        self.balls = []                         # List that holds all ball objects in COORDS

        # Append balls[]-list with a new ball for each ball in COORDS
        for coord in COORDS:
            self.balls.append(Ball(len(self.balls)))

    def draw(self):
        """
        Function Game.draw(self):
        Simple drwa function, that sets up the background and calls the Ball.draw()-function
        for each ball used in the game.
        Furthermore the counter display gets added to picture.
        """
        # Fill background of the playing field with the background colour
        g_screen.fill(BG_COLOUR)

        # Call the draw()-function for each ball of balls[] 
        for ball in self.balls:
            ball.draw()

        # Add current moves counter to the canvas
        img = g_font.render("Moves: " + str(self.counter), True, BLACK)
        g_screen.blit(img, (20, 20))

    # add comments
    def move(self, ball):
        # Case(1): No ball is selected atm and the observed ball is not white.
        #   -> Select it and set depending variables accordingly.
        if not self.isBallSelected and ball.colour != 0:
            ball.select()
            checkBalls = []
            checkBalls.append(ball.id)
            while len(checkBalls) > 0:
                for selectableBall in self.balls[checkBalls[0]].neighbours:
                    if (self.balls[selectableBall].colour == 0 and 
                        self.balls[selectableBall].selected == BALL_NOMARK):
                        self.balls[selectableBall].selected = BALL_MARK_S
                        checkBalls.append(selectableBall)
                checkBalls.pop(0)

            self.selectedBall = ball
            self.isBallSelected = True

        # Case(2): A ball is selected atm and the observed ball has a big rim.
        #   -> Unselect all balls and set depending variables accordingly.
        elif self.isBallSelected and ball.selected == BALL_MARK_L:
            for ball in self.balls:
                ball.select(False)
            self.isBallSelected = False

        # Case(3): A ball is selected atm and the observed ball has a small rim.
        #   -> Swap the colours of the selected and the observed ball, unselect
        #      all balls and set depending variables accordingly.
        elif self.isBallSelected and ball.selected == BALL_MARK_S:
            ball.colour = self.selectedBall.colour
            self.selectedBall.colour = 0
            for ball in self.balls:
                ball.select(False)
            self.isBallSelected = False
            self.counter += 1

    def clicked(self, position):
        """
        Function Game.clicked(self, position):
        Determines if the clicked-event is used on a ball, by comparing the mouse
        position to the position and the surface of each ball used in the game.

        parma[in]   position    current position of the mouse during a click-event
        """
        # Iterate through all balls in the game
        for ball in self.balls:
            # Check if the mouse position is inside the surface of the ball
            if (distance(position, ball.position) < BALL_RADIUS):
                self.move(ball)
                break

    # add comments
    def setState(self, state):
        for i in range(len(self.balls)):
            self.balls[i].colour = state[i]
            self.balls[i].selected = BALL_NOMARK
            self.isBallSelected = False

    # add comments
    def getState(self):
        state = []
        for i in range(len(self.balls)):
            state.append(self.balls[i].colour)
        return state

# add comments
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
        myGame = Game()
        for position in range(len(GOAL)):
            myGame.setState(self.state)
            myGame.move(myGame.balls[position])
            moves = []
            for move in range(len(GOAL)):
                if myGame.balls[move].selected == BALL_MARK_S:
                    moves.append(move)
            for move in moves:
                myGame.setState(self.state)
                myGame.move(myGame.balls[position])
                myGame.move(myGame.balls[move])
                neighbours.append(myGame.getState())
        return neighbours

# -- HELPER FUNCTIONS -----------------------------------------------
def distance(p0, p1):
    """
    Function distance(p0, p1):
    Calculates the hysteresis between to given coordinates.

    parm[in]    p0     Coordinates of first position 
    parm[in]    p1     Coordinates of second position
    
    return      Hysteresis value between given coordinates     
    """
    return ((p0[0]-p1[0])**2 + (p0[1]-p1[1])**2)**0.5


# -- MAIN -----------------------------------------------------------
def main():
    """
    Function main():
    Main function that gets called on start and handles the whole game    
    """
    # Set runner variable for a new game
    running = True
    
    # Create a new game
    game = Game()

    # add comments
    solving = False
    # add comments
    if solving:
        states = []
        checkStates = []
        states.append(State(0, copy.deepcopy(game.getState()), -1, 0))
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
                    previousState = GOAL
                    currentState = states[stateToBeCalculated].state
                    while stateToBeCalculated != 0:
                        currentState = states[stateToBeCalculated].state
                        displayedMove = ""
                        for i in range(len(previousState)):
                            if previousState[i] == 0 and currentState[i] > 0:
                                displayedMove += str(COORDS[i])
                                break
                        displayedMove += " -> "
                        for i in range(len(previousState)):
                            if previousState[i] > 0 and currentState[i] == 0:
                                displayedMove += str(COORDS[i])
                                break
                        print(displayedMove)
                        previousState = currentState
                        stateToBeCalculated = states[states[stateToBeCalculated].parent].id
                    currentState = START
                    displayedMove = ""
                    for i in range(len(previousState)):
                        if previousState[i] == 0 and currentState[i] > 0:
                            displayedMove += str(COORDS[i])
                            break
                    displayedMove += " -> "
                    for i in range(len(previousState)):
                        if previousState[i] > 0 and currentState[i] == 0:
                            displayedMove += str(COORDS[i])
                            break
                    print(displayedMove)
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
        # Poll for events
        for event in pygame.event.get():
            # pygame.QUIT event is called when user clicked X
            # to close the window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.clicked(pygame.mouse.get_pos())
        
        # Call Game.draw() to set-up the playing field for a new frame.
        game.draw()
        pygame.display.flip()
        g_clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()