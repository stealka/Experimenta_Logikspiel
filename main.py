#!python

#####   ABOUT   #####################################################
#                                                                   #
# Brief descritption (ToDo)                                         #
#                                                                   #
# ----------------------------------------------------------------- #
#   Version:    0.1  - Basic gameplay mechanic              | MSU | #
#               0.2  - Rework and code documentation        | SKA | #
# ----------------------------------------------------------------- #
#                                                                   #
#####################################################################

# -- IMPORTS --------------------------------------------------------
import pygame
import time

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

# Playingfield coordinations - Level 1
COORDS = [  (0,0, BLACK),                                           (4,0, RED),
            (0,1, BLACK), (1,1, WHITE), (2,1, WHITE), (3,1, WHITE), (4,1, RED),
            (0,2, BLACK),               (2,2, WHITE),               (4,2, RED),
            (0,3, BLACK),                                           (4,3, RED)]

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
    def __init__(self, coord):
        """
        Function Ball.__init__(self, coord):
        Creates main properties of a circle field with given properties
        from a defined playing field coord[] -> COORDS_x[]

        param[in]   coord   Playfield Array with circle properties
                            (see COORDS_x[])
        """
        # Setting up circle properties from given COORDS_x[]
        self.coord      = (coord[0], coord[1])
        self.colour     = coord[2]
        self.position   = ((BALL_DISTANCE + 2 * BALL_RADIUS) * (coord[0] + 1),
                           (BALL_DISTANCE + 2 * BALL_RADIUS) * (coord[1] + 1))
        self.selected   = BALL_NOMARK
        self.neighbours = []


    def draw(self):
        """
        Function Ball.draw(self):
        Simple draw function that places the circle on a new canvas frame.
        Depending on the status of the selection property the circle gets highlighted
        with an additional rim.
        """
        pygame.draw.circle(g_screen, self.colour, self.position, BALL_RADIUS)
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
            self.checkMove()
        else:
            self.selected = BALL_NOMARK

    def checkMove(self):
        """
        Function Ball.checkMove(self):
        Checks recursively which neighbours of the ball aren't occupied with another token
        ball. If the neighbour is free (colour: WHITE) the property "selected" gets updated.
        """
        for selectableBall in self.neighbours:
            if (selectableBall.colour is WHITE and selectableBall.selected == BALL_NOMARK):
                selectableBall.selected = BALL_MARK_S
                selectableBall.checkMove()

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
        self.selectedBall = Ball((0,0, GREEN))  # Variable to hold the selected ball object
        self.balls = []                         # List that holds all ball objects in COORDS

        # Append balls[]-list with a new ball for each ball in COORDS
        for coord in COORDS:
            self.balls.append(Ball(coord))

        # Iterate through all balls 
        for ball in self.balls:
            # Specify one ball to be checked
            for ballToCheck in self.balls:
                # Check the ball for neighbour balls
                if ball is not ballToCheck:
                    # Horizontal check
                    if (abs(ball.coord[0] - ballToCheck.coord[0]) == 1
                    and abs(ball.coord[1] - ballToCheck.coord[1])) == 0:
                        ball.neighbours.append(ballToCheck)
                    # Vertical check
                    if (abs(ball.coord[0] - ballToCheck.coord[0]) == 0
                    and abs(ball.coord[1] - ballToCheck.coord[1])) == 1:
                        ball.neighbours.append(ballToCheck)

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
                # Case(1): No ball is selected atm and the observed ball is not white.
                #   -> Select it and set depending variables accordingly.
                if not self.isBallSelected and ball.colour is not WHITE:
                    ball.select()
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
                    self.selectedBall.colour = WHITE
                    for ball in self.balls:
                        ball.select(False)
                    self.isBallSelected = False
                    self.counter += 1
                break

# -- HELPER FUNCTIONS -----------------------------------------------
def distance(p0, p1):
    """
    Function distance(p0, p1):
    Calculates the hysteresis between to given coordinates.

    parm[in]    p0     Coordinates of first position 
    parm[in]    p1     Coordinates of second position       
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