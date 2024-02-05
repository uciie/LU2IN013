import unittest
from simulation.robot import Roue,Robot, Vecteur

class TestRoue(unittest.TestCase):

    def setUp(self):
        """
        Initialisation des roues pour les tests.
        """
        self.roue1 = Roue(10)
        self.roue2 = Roue(5)

    def test_set_vitesse_angulaire(self):
        """
        Initialisation des roues pour les tests.
        """
        self.roue1.set_vitesse_angulaire(20)
        self.assertEqual(self.roue1.vitesse_angulaire, 20)
        self.assertEqual(self.roue2.vitesse_angulaire, 0)

class TestRobot(unittest.TestCase):

    def setUp(self):
        """Initialisation du robot"""
        self.r = Robot("r", 5, 5 ,2, 2, Vecteur(1,1) ,10, "red")
    
    def test_getCurrPos(self):
        """Teste les coordonnées actuelles du robot
        """
        resultat_pos = self.r.getCurrPos()
        self.assertEqual(resultat_pos, (self.r.posX, self.r.posY))
    
    def test_move_dOm(self):
        """Teste le mouvement du robot
        """
        mouvement = (self.r.posX + 1, self.r.posY + 1)
        resultat_move = self.r.move_dOM(1,1)
        self.assertEqual((self.r.posX, self.r.posY), mouvement)

    def test_getLasPos(self):
        """Teste les anciennes coordonnées du robot
        """
        ancienne_pos = (self.r.posX, self.r.posY)
        self.r.move_dOM(1,1)
        resultat_getLastPos = self.r.getLastPos()
        self.assertEqual(resultat_getLastPos, ancienne_pos)
    
if __name__ == '__main__':
    unittest.main()
        
if __name__ == '__main__':
    unittest.main()