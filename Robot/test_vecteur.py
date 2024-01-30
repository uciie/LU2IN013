import unittest
from vecteur import Vecteur

class TestVecteur(unittest.TestCase):

    def setUp(self):
        #initialisation des vecteurs
        self.v1 = Vecteur(2, 3)
        self.v2 = Vecteur(1, 4)

    def test_add(self):
        #addition
        resultat_addition = self.v1.add(self.v2)
        self.assertEqual(resultat_addition.x, 3)
        self.assertEqual(resultat_addition.y, 7)

    def test_soustraction(self):
        #soustraction
        resultat_soustraction = self.v1.soustraction(self.v2)
        self.assertEqual(resultat_soustraction.x, 1)
        self.assertEqual(resultat_soustraction.y, -1)

    def test_rotation(self):
        #rotation
        vecteur_rotation = self.v1.rotation(90)
        self.assertEqual(vecteur_rotation.x, -3)
        self.assertEqual(vecteur_rotation.y, 2)

    def test_get_coordonnees(self):
        #récupération des coordonnées
        coordonnees = self.v1.getCoor()
        self.assertEqual(coordonnees, (2, 3))

    def test_produit_scalaire(self):
        #produit scalaire
        produit_scalaire = self.v1.produit_scalaire(self.v2)
        self.assertEqual(produit_scalaire, 14)

    def test_equals(self):
        #égalité de deux vecteurs
        are_equal = self.v1.equals(self.v2)
        self.assertFalse(are_equal)

if __name__ == '__main__':
    unittest.main()
