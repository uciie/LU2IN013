#### TESTER LES OPERATIONS ELEMENTAIRE DE DU VECTEURS ###
from Vecteur import *

def main():
    """
    Soit deux point x, y ayant comme coord (x_a,x_b) et (x_b,y_b)
    """
    x_b, y_b= 2.0,2.5
    v1 = Vecteur("vect_dir", (x_b, y_b))
    v2 = Vecteur("vect_dir", (x_b-2, y_b+1))

    print(v1.nom)
    print("Composantes : " + str (v1.composantes))
    print("Norme : " + str(v1.norme))

    print(v2.nom)
    print("Composantes : " + str (v2.composantes))
    print("Norme : " + str(v2.norme))

    v3 = v1.add(v2)
    print(v3.nom)
    print("Composantes : " + str (v1.composantes))
    print("Norme : " + str(v1.norme))
    print()
    
main()

    