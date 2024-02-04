import unittest
from simulation.grille import Grille

class TestGrille(unittest.TestCase) :
    
    def setUp(self):
        """Initialiasation de la grille
        """
        self.g = Grille(5, 5, 1)

    def test_affiche(self):
        """Teste l'affichage
        """
        self.g.affiche()

if __name__ == '__main__':
    unittest.main()