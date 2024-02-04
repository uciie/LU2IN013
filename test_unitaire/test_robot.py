import unittest
from simulation import Robot

class TestRobot(unittest.TestCase):

    def setUp(self):
        """Initialisation du robot"""
        r = Robot("r", 5, 5, 2, 2, "red")
    
    def test_getCurrPos(self):
        """Teste les coordonnées actuelles du robot
        """
        resultat_pos = self.r.getCurrPos()
        self.assertEqual(resultat_pos.x, (self.r.posX, self.r.posY))
    
    def test_move_dOm(self):
        """Teste le mouvement du robot
        """
        mouvement = (self.r.posX + 1, self.r.posY + 1)
        resultat_move = self.r.move_dOM(1,1)
        self.assertEqual((self.r.posX, self.r.posY), mouvement)

    def test_getLasPos(self):
        """Teste les anciennes coordonnées du robot
        """
        ancienne_pos = (self.r.posX; self.r.posY)
        self.r.move_dOM(1,1)
        resultat_getLastPos = self.r.getLastPos()
        self.assertEqual(resultat_getLastPos, ancienne_pos)
    
if __name__ == '__main__':
    unittest.main()