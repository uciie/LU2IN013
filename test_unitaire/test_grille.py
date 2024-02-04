import unittest
from simulation.grille import Grille

class TestGrille(unittest.TestCase) :
    
    def setUp(self):
        """Initialiasation de la grille
        """
        self.g = Grille(20, 20, 1)

    def test_affiche():
        """Teste l'affichage
        """