#!python

# -- IMPORTS --------------------------------------------------------
import pygame
import time

# -- DEFINES --------------------------------------------------------
BLACK = (   0,   0,   0)
RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = (   0,   0, 255)
WHITE = ( 255, 255, 255)


def drawBoard(screen):
    "Function used to initially draw the playing field as a base for each new frame"
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (400, 400), 40)


def init():
    "Init function that sets up all necessary initial configurations"
    
    # Initializing pygame module
    pygame.init()
    
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dTime = 0
    
    while running:
        # Poll for events
        # pygame.QUIT event is called when user clicked X
        # to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Call drawBoard to set-up the base playing field for
        #   the new frame.
        drawBoard(screen)
                
        pygame.display.flip()
        
        pygame.draw.circle(screen, BLACK, (400, 400), 42)
        pygame.draw.circle(screen, RED, (400, 400), 40)        
               
        pygame.display.flip()
    

if __name__ == '__main__':
    init()