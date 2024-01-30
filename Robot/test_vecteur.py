from Robot import Robot
from Grille import Grille
from Vecteur import Vecteur

def main():
    
    #On definit deux vecteurs
    v1 = Vecteur(2,3)
    v2 = Vecteur(1,4)

    print("Coordonnées du vecteur 1 :", vecteur1.getCoor())
    print("Coordonnées du vecteur 2 :", vecteur2.getCoor())

    #Addition de deux vecteurs
    resultat_addition = vecteur1.add(vecteur2)
    print("Résultat de l'addition :", resultat_addition.getCoor())

    #Soustraction de deux vecteurs
    resultat_soustraction = vecteur1.soustraction(vecteur2)
    print("Résultat de la soustraction :", resultat_soustraction.getCoor())

    #Rotation d'un vecteur
    vecteur_rotation = vecteur1.rotation(90)
    print("Résultat de la rotation de 90 degrés :", vecteur_rotation.getCoor())

    #Retourne les coordonnee d'un vecteur
    v = v1.getCoor()
    print("les coordonnee d'un vecteur:", v)
    
    # Produit scalaire de deux vecteurs
    produit_scalaire = vecteur1.produit_scalaire(vecteur2)
    print("produit scalaire entre les deux vecteurs :", produit_scalaire)

    #Vérification si deux vecteurs sont égaux
    are_equal = vecteur1.equals(vecteur2)
    print("Est-ce que les vecteur sont egaux ?", are_equal)

if __name__ == "__main__":
    main()
