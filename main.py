#!python

#####   ABOUT   #####################################################
#                                                                   #
# Brief descritption (ToDo)                                         #
#                                                                   #
# ----------------------------------------------------------------- #
#   Version:    0.1  - Basic gameplay mechanic              | MSU | #
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
g_running = True


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
        self.coord = (coord[0], coord[1])
        self.color = coord[2]
        self.position = ((BALL_DISTANCE + 2 * BALL_RADIUS) * (coord[0] + 1),
                         (BALL_DISTANCE + 2 * BALL_RADIUS) * (coord[1] + 1))
        self.selected = BALL_NOMARK
        self.neighbours = []


    def draw(self):
        """
        Function Ball.draw(self):
        Simple draw function that places the circle on a new canvas frame.
        Depending on the status of the selection property the circle gets highlighted
        with an additional rim.
        """
        pygame.draw.circle(g_screen, self.color, self.position, BALL_RADIUS)
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
            if (selectableBall.color is WHITE and selectableBall.selected == BALL_NOMARK):
                selectableBall.selected = BALL_MARK_S
                selectableBall.checkMove()

class Game:
    def __init__(self):
        pass

    def draw(self):
        pass

    def clicked(self, position):
        pass

def main():
    """
    Main function that gets called on start and handles the whole game
    """

    while g_running:
        # Poll for events
        for event in pygame.event.get():
            # pygame.QUIT event is called when user clicked X
            # to close the window
            if event.type == pygame.QUIT:
                g_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Game.clicked(pygame.mouse.get_pos())
        
        # Call Game.draw() to set-up the playing field for a new frame.
        Game.draw()
        pygame.display.flip()
        g_clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()


# def drawBoard(screen):
#     """
#     Function used to initially draw the playing field as a base for each new frame
#     """
#     g_screen.fill(BG_COLOUR)
#     pygame.draw.circle(screen, RED, (400, 400), 40)


# def init():
#     """
#     Init function that sets up all necessary initial configurations
#     """
#     dTime = 0