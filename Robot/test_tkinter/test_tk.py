import tkinter as tk
from vecteur import *
from robot import *
from grille import *
from Exceptions.borneException import *

def main():
    root = tk.Tk()
    root.title("Simulation de déplacement du robot")

    #Dimension de la fenetre 
    largeur, hauteur = 300, 300
    
    canvas = tk.Canvas(root, width=largeur, height=hauteur, bg="white")
    canvas.pack()

    # Position initiale du robot
    dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

    # Assurez-vous que la grille est correctement initialisée
    grille = Grille(largeur, hauteur, 5)
    
    #Creation du robot 
    robot = Robot("R", int(largeur/2), int(hauteur/2), dim_robot_x, dim_robot_y, grille, Vecteur(1, 1), canvas,color="red")

    def tracer_carre():
        """
        Le robot trace un carre 
        """
        distance = 500 # metre
        angle = 90
        vitesse = 100 # m/s
        for i in range(4):
            robot.go(angle, distance, vitesse)
    
    #tracer_carre(distance)
    carre_button = tk.Button(root, text="Tracer un carre", command=tracer_carre)
    carre_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
