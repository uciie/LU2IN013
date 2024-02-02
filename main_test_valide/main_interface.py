from interface_graph import * 
from robot import *
from grille import *



if __name__ == "__main__":
    # Dimension de la fenetre 
    largeur, hauteur = 300, 300
    bg = "white"
    interface = Interface("Simulation de déplacement du robot", largeur, hauteur, bg)

    def start_simulation():
        print("hello")
        interface.draw_obj(robot)


    # Position initiale du robot
    dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

    # Assurez-vous que la grille est correctement initialisée
    grille = Grille(largeur, hauteur, 5)
    
    #Creation du robot 
    robot = Robot("R", int(largeur/2), int(hauteur/2), dim_robot_x, dim_robot_y, grille, Vecteur(0, -1), interface.canvas,color="red")


    start_button = interface.creer_button("Démarrer la simulation", start_simulation)
    start_button.pack()

    interface.root.mainloop()