import unittest
from MVC.modele.vecteur import Vecteur

class TestVecteur(unittest.TestCase):

    def setUp(self):
        """
        Initialisation des vecteurs pour les tests.
        """
        self.v1 = Vecteur(2, 3)
        self.v2 = Vecteur(1, 4)

    def test_add(self):
        """
        Teste l'addition de deux vecteurs.
        """
        resultat_addition = self.v1.add(self.v2)
        self.assertEqual(resultat_addition.x, 3)
        self.assertEqual(resultat_addition.y, 7)

    def test_soustraction(self):
        """
        Teste la soustraction de deux vecteurs.
        """
        resultat_soustraction = self.v1.soustraction(self.v2)
        self.assertEqual(resultat_soustraction.x, 1)
        self.assertEqual(resultat_soustraction.y, -1)

    def test_multiplication(self):
        """
        Teste la soustraction de deux vecteurs.
        """
        resultat_multiplication = self.v1.multiplication(2)
        self.assertEqual(resultat_multiplication.x, 4)
        self.assertEqual(resultat_multiplication.y, 6)

    def test_rotation(self):
        """
        Teste la rotation d'un vecteur.
        """
        vecteur_rotation1 = self.v1.rotation(90)
        self.assertEqual(vecteur_rotation1.x, 3)
        self.assertAlmostEqual(vecteur_rotation1.y, -2)

        vecteur_rotation2 = self.v2.rotation(0)
        self.assertEqual(vecteur_rotation2.x, 1)
        self.assertEqual(vecteur_rotation2.y, 4)

    def test_equals(self):
        """
        Teste l'égalité de deux vecteurs.
        """
        are_equal = self.v1.equals(self.v2)
        self.assertFalse(are_equal)

if __name__ == '__main__':
    unittest.main()
