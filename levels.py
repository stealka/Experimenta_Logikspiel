# -- IMPORTS --------------------------------------------------------
from globals import *

# Description of levels

# Level 0
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

# Level 1
LEVEL_1_COORD = [(0,0),                      (4,0),                      (8,0),
		         (0,1),	(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1),
		         (0,2),        (2,2),        (4,2),        (6,2),        (8,2),
		         (0,3),                      (4,3),                      (8,3)]

LEVEL_1_START = [P1,              P2,              P3,
				 P1,  N,  N,  N,  P2,  N,  N,  N,  P3,
				 P1,      N,      P2,      N,      P3,
				 P1,              P2,              P3]

LEVEL_1_GOAL = [P3,              P1,              P2,
				P3,  N,  N,  N,  P1,  N,  N,  N,  P2,
				P3,      N,      P1,      N,      P2,
				P3,              P1,              P2]

LEVEL_1 = (LEVEL_1_COORD, LEVEL_1_START, LEVEL_1_GOAL)

# Level 2
LEVEL_2_COORD = [(0,0),        (2,0),        (4,0),
		         (0,1),	(1,1), (2,1), (3,1), (4,1),
		         (0,2),        (2,2),        (4,2),
		         (0,3),                      (4,3)]

LEVEL_2_START = [P1,      N,      P2,
				 P1,  N,  N,  N,  P2,
				 P1,      N,      P2,
				 P1,              P2]

LEVEL_2_GOAL = [P2,      N,      P1,
				P2,  N,  N,  N,  P1,
				P2,      N,      P1,
				P2,              P1]

LEVEL_2 = (LEVEL_2_COORD, LEVEL_2_START, LEVEL_2_GOAL)
# Array of levels
LEVELS = [LEVEL_0, LEVEL_1, LEVEL_2]