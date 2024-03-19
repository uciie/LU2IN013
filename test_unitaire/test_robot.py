import unittest
from MVC.modele.robot.robot import Roue
from MVC.modele.robot.simu_robot import Robot

class TestRoue(unittest.TestCase):

    def setUp(self):
        """
        Initialisation des roues pour les tests.
        """
        self.roue1 = Roue(10, 100)
        self.roue2 = Roue(5, 100)

    def test_set_vitesse_angulaire(self):
        """
        Initialisation des roues pour les tests.
        """
        self.roue1.vitesse_angulaire = 20
        # Verifie si vitesse_angulaire ne depasse pas vmax_ang
        self.roue2.vitesse_angulaire = 200 
        self.assertEqual(self.roue1.vitesse_angulaire, 20)
        self.assertEqual(self.roue2.vitesse_angulaire, 100)

class TestRobot(unittest.TestCase):

    def setUp(self):
        """Initialisation du robot"""
        self.r = Robot("r", 5, 5 ,2, 2, 10, 10, "red")
    
    def test_getCurrPos(self):
        """Teste les coordonnées actuelles du robot
        """
        resultat_pos = self.r.curr_pos
        self.assertEqual(resultat_pos, (self.r.posX, self.r.posY))

    def test_getLasPos(self):
        """Teste les anciennes coordonnées du robot
        """
        ancienne_pos = (self.r.posX, self.r.posY)
        self.r.move_dOM(1,1)
        resultat_last_pos = self.r.last_pos
        self.assertEqual(resultat_last_pos, ancienne_pos)

    def test_vitesse(self):
        """Teste la vitesse du robot
        """
        self.assertEqual(self.r.vitesse, 0.)

    def test_getVitesse_angulaire(self):
        """Teste la vitesse angulaire du robot
        """
        self.r.roue_droite.vitesse_angulaire = -1
        self.r.roue_gauche.vitesse_angulaire = 1
        # initialise les vitesses roues
        vitesse_ang = self.r.vitesse_angulaire
        self.assertEqual(vitesse_ang, -10)
    
    def test_move_dOm(self):
        """Teste le mouvement du robot
        """
        mouvement = (self.r.posX + 1, self.r.posY + 1)
        resultat_move = self.r.move_dOM(1,1)
        self.assertEqual((self.r.posX, self.r.posY), mouvement)

    
if __name__ == '__main__':
    unittest.main()
        