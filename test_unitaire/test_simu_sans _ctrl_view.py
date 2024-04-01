import threading

from src.modele.objets import Arene, ObstacleRectangle, SimuRobot
from src.modele.simulation import Simulation
from src.modele.utilitaire import Vecteur

def main():
    # Création du verrou
    lock_aff = threading.RLock()

    dt_controller = 1/100
    echelle = 5
    largeur, hauteur = 500, 500
    dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

    # Initialisation de l'_arene, robot, obstacle
    arene = Arene("Simulation de déplacement du robot", largeur, hauteur, echelle)
    robot = SimuRobot("R", int(largeur / 2), int(hauteur / 2), dim_robot_x, dim_robot_y, 10, 150, color="red")
    obs = ObstacleRectangle(200, 200, Vecteur(10, 0), Vecteur(0, 20), color="blue")

    # Ajouter un obstacle dans l'_arene
    arene.add_obstacle(obs)

    # Créer la simulation
    simu = Simulation("Simulation", dt_controller, robot, arene, lock_aff)

    # donner une vitesse au robot
    robot.set_vitesse_roue(0, 50)

    print(robot.info())
    # demarer la simulation
    simu.run()



if __name__ == '__main__':
    main()

