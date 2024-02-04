import unittest
from simulation.robot import Roue

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
        
if __name__ == '__main__':
    unittest.main()