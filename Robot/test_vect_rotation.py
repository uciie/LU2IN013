#### TESTER LA ROTATION DE DU VECTEURS ###
from vecteur import Vecteur



def main():
    """
    Soit soit un vecteur (1,1) testons la rotation
    """
    x_a = 0
    y_a = 1
    v1 = Vecteur(x_a, y_a)

    
    #Rotation de 90deg de v1
    v2 = v1.rotation(90)
    print("90°")
    print("Composantes : ", v2.getCoor())
    print("Norme : " + str(v2.norme))
    print()

    #Rotation de 60 deg de v1
    v3 = v1.rotation(60)
    print("60°")
    print("Composantes : ", v3.getCoor())
    print("Norme : " + str(v3.norme))
    print()

    #Rotation de 45 deg de v1
    v4 = v1.rotation(45)
    print("45°")
    print("Composantes : ", v4.getCoor())
    print("Norme : " + str(v4.norme))
    print()

    #Rotation de -30 deg de v1
    v5 = v1.rotation(-30)
    print("-30°")
    print("Composantes : ", v5.getCoor())
    print("Norme : " + str(v5.norme))
    print()

    
main()