import threading

from MVC.controller.controleur import Controleur, AdaptateurRobotSimu
from MVC.modele.objets import Arene, SimuRobot, ObstacleRectangle
from MVC.modele.simulation import Simulation
from MVC.modele.vecteur import Vecteur
from MVC.view.affichage import Affichage


def main():
    # Création du verrou
    lock_aff = threading.RLock()
    lock_ctrl = threading.RLock()

    dt_simu = 1/10000
    dt_controller = 1/100000
    dt_affichage = 1
    echelle = 5
    largeur, hauteur = 500, 500
    dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

    # Initialisation de l'arene, robot, obstacle
    arene = Arene("Simulation de déplacement du robot", largeur, hauteur, echelle)
    robot = SimuRobot("R", int(largeur / 2), int(hauteur / 2), dim_robot_x, dim_robot_y, 10, 200, color="red")
    obs = ObstacleRectangle(100, 100, Vecteur(10, 10), Vecteur(20, 20), color="blue")

    # Ajouter un obstacle dans l'arene
    arene.add_obstacle(obs)

    # Créer la simulation
    simu = Simulation("Simulation", dt_simu, robot, arene, lock_aff)

    # Créer l'adaptateur
    adaptateur = AdaptateurRobotSimu(robot, simu)
    # adaptateur.set_vitesse_roue(50, 50)

    # Création du module View
    view = Affichage(simu, dt_affichage, lock_aff)

    # Création du module Controller
    controller = Controleur(adaptateur, dt_controller, lock_aff)

    # Ajout du lien de communication entre view et controller
    view.controller = controller

    # demarrage des threads
    view_thread = threading.Thread(target=view.run)

    view_thread.start()
    simu.start()
    controller.start()

    # Attendre que les threads se terminent
    view_thread.join()
    simu.join()
    controller.join()


if __name__ == '__main__':
    main()
