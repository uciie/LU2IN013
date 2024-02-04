import unittest
from .simulation/robot import Robot

class TestRobot(unittest.TestCase):

    def setUp(self) :
        """Initialisation du robot"""
        r = Robot("r", 5, 5, 2, 2, "red")
    
    def test_getCurrPos(self):
        """Teste les coordonées actuelles du robot
        """
        resultat_pos = getCurrPos(r)
        self.assertEqual(resultat_pos.x, (r.posX, r.posY))