#!python

#####   ABOUT   #####################################################
#                                                                   #
# Brief descritption (ToDo)                                         #
#                                                                   #
# ----------------------------------------------------------------- #
#   Version:    0.1  - Class created                        | MSU | #
# ----------------------------------------------------------------- #
#                                                                   #
#####################################################################

# -- IMPORTS --------------------------------------------------------
import pygame
from globals import *

# -- DEFINES --------------------------------------------------------
BUTTON_STATE_DEFAULT = 0
BUTTON_STATE_CLICKED = 1
BUTTON_STATE_HOVERED = 2

BUTTON_COLOURS = [(100,100,100),(200,200,200),(120,120,120)]

# -- CLASSES --------------------------------------------------------
class Button:
    """
    The class Button adds the game engine element button. A button can have a label,
    a position and size and a function that is called when the button is clicked.
    In addition to that a button changes color when hovered.
    """
    def __init__(self, g_screen, position, text, g_font, oneClickFunction):
        """
        Function Button.__init__(self, g_screen, position, text, g_font, oneClickFunction):
        Initializes a button and setting it's default parameters.
        param[in]   g_screen            screen object to draw the button on top
        param[in]   position            position of the button in pixel
        param[in]   text                text of the button label
        param[in]   g_font              font of the button label
        param[in]   oneClickFunction    function to be called if button is clicked
        """
        self.g_screen = g_screen
        self.position = position
        self.textPosition = (self.position[0]+30, self.position[1] +self.position[3]-28)
        self.text = text
        self.g_font = g_font
        self.oneClickFunction = oneClickFunction
        self.state = BUTTON_STATE_DEFAULT

    def draw(self):
        """
        Function Button.draw(self):
        Simple draw function that places the rectangle on a new canvas frame.
        If the Button object is hovered or clicked it changes its appearance.
        """
        pygame.draw.rect(self.g_screen, BUTTON_COLOURS[self.state], self.position)
        img = self.g_font.render(str(self.text), True, BLACK)
        self.g_screen.blit(img, self.textPosition)

    def checkHover(self, position):
        """
        Function Button.checkHover(self, position):
        Determines if the mouse is hovering over a button and changing it's color.
        param[in]   position    current position of the mouse
        """
        if  position[0] > (self.position[0])\
        and position[0] < (self.position[0] + self.position[2])\
        and position[1] > (self.position[1])\
        and position[1] < (self.position[1] + self.position[3]):
            self.state = BUTTON_STATE_HOVERED
        else:
            self.state = BUTTON_STATE_DEFAULT

    def checkClicked(self, position):
        """
        Function Button.clicked(self, position):
        Determines if the clicked-event is used on a button, by comparing the mouse
        position to the position and the surface of each button used in the game.

        param[in]   position    current position of the mouse during a click-event
        """
        if self.state == BUTTON_STATE_HOVERED:
            self.state = BUTTON_STATE_CLICKED
            self.oneClickFunction()