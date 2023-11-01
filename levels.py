# -- IMPORTS --------------------------------------------------------
from globals import *

# Description of levels
LEVEL_0_COORD = [(0,0),                      (4,0),
		         (0,1),	(1,1), (2,1), (3,1), (4,1),
		         (0,2),        (2,2),        (4,2),
		         (0,3),                      (4,3)]

LEVEL_0_START = [P1,              P2,
				 P1,  N,  N,  N,  P2,
				 P1,      N,      P2,
				 P1,              P2]

LEVEL_0_GOAL = [P2,              P1,
				P2,  N,  N,  N,  P1,
				P2,      N,      P1,
				P2,              P1]

LEVEL_0 = (LEVEL_0_COORD, LEVEL_0_START, LEVEL_0_GOAL)

# Array of levels
LEVELS = [LEVEL_0]