#### TESTER LES OPERATIONS ELEMENTAIRE DE DU VECTEURS ###
from vecteur import *



def main():
    x_a, y_a = (1,1)
    x_b, y_b = (1.5,3)
    v1 = Vecteur(x_a, y_a)
    v2 = Vecteur(x_b, y_b)

    print("v1")
    print("Composantes :", v1.getCoor())
    print("Norme : " + str(v1.norme))

    print("v2")
    print("Composantes : (", v2.getCoor())
    print("Norme : " + str(v2.norme))

    v3 = v1.add(v2)
    print("v3")
    print("Composantes : ", v3.getCoor())
    print("Norme : " + str(v3.norme))
    print()

    v4 = v1.soustraction(v2)
    print("v4")
    print("Composantes : ", v4.getCoor())
    print("Norme : " + str(v4.norme))
    print()
    
    
main()
