from vecteur import *

def main():
    """Création de deux vecteurs
    """
    v1 = Vecteur(5, -10)
    v2 = Vecteur(2, 1)

    """Produit scalaire entre ces deux vecteurs
    """
    print("Produit scalaire : " + str(v1.produit_scalaire(v2)))

    """Nouveau vecteur
    """
    v3 = Vecteur(7,1)

    """Produit scalaire entre v1 et v2
    """
    print("Produit scalaire : " + str(v1.produit_scalaire(v3)))
main()
