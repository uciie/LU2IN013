import unittest
from simulation import Robot

class TestRobot(unittest.TestCase):

    def setUp(self):
        """Initialisation du robot"""
        r = Robot("r", 5, 5, 2, 2, "red")
    
    def test_getCurrPos(self):
        """Teste les coordonées actuelles du robot
        """
        resultat_pos = self.r.getCurrPos()
        self.assertEqual(resultat_pos.x, (r.posX, r.posY))
    
    def test_move_dOm(self):
        """Teste le mouvement du robot
        """
        mouvement = (r.posX + 1, r.posY + 1)
        resultat_move = self.r.move_dOM(1,1)
        self.assertEqual((r.posX, r.posY), mouvement)

    