import tkinter as tk
from simulation.vecteur import *
from simulation.robot import *
from simulation.grille import *

def main():
    """ Teste de simulation du robot en mouvement continue
    """
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
    robot = Robot("R", int(largeur/2), int(hauteur/2), dim_robot_x, dim_robot_y, grille, Vecteur(0, -1), canvas,color="red")

    def start_simulation():
        """
        Le robot trace un carre 
        """
        distance = 1 # metre
        angle = 5
        vitesse = 100 # m/s
        for i in range(100):
            robot.go(angle, distance, vitesse)
    
    start_button = tk.Button(root, text="Démarrer la simulation", command=start_simulation)
    start_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
