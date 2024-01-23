from Robot_v2_no_fini import *
from Grille_v2_no_fini import *
from Obstacle import *


def main():
    g = Grille(9,9)
    r = Robot("Dexter", 2, 2, 1, 1, g)
    o = Obstacle(2,1,0,0,g)