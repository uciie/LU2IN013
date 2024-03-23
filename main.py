import threading

from MVC.controller.adaptateur_robot_simu import AdaptateurRobotSimu
from MVC.controller.ai import Go, StrategieSequentielle, TournerDeg
from MVC.controller.controleur import Controleur
from MVC.modele.objets import Arene, ObstacleRectangle, SimuRobot
from MVC.modele.simulation import Simulation
from MVC.modele.vecteur import Vecteur
from MVC.view.affichage import Affichage


def main():
    # Création du verrou
    lock_aff = threading.RLock()
    lock_ctrl = threading.RLock()
    lock_sim = threading.RLock()

    dt_simu = 1 / 24000
    dt_controller = 1 / 3000000
    dt_affichage = 1 / 300000
    echelle = 5
    largeur, hauteur = 500, 500
    dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

    # Initialisation de l'arene, robot, obstacle
    arene = Arene("Simulation de déplacement du robot", largeur, hauteur, echelle)
    robot = SimuRobot("R", int(largeur / 2), int(hauteur / 2), dim_robot_x, dim_robot_y, 10, 150, color="red")
    obs = ObstacleRectangle(100, 100, Vecteur(10, 10), Vecteur(20, 20), color="blue")

    # Ajouter un obstacle dans l'arene
    arene.add_obstacle(obs)

    # Créer la simulation
    simu = Simulation("Simulation", dt_simu, robot, arene, lock_sim)

    # Créer l'adaptateur
    adaptateur = AdaptateurRobotSimu(robot, simu)

    # Création du module View
    view = Affichage(simu, dt_affichage, lock_aff)

    # Création du module Controller
    controller = Controleur(adaptateur, dt_controller, lock_aff)

    # Ajout du lien de communication entre view et controller
    view.controller = controller
    steps = [Go(controller.adaptateur, 50, 50,50, controller.dt),
            TournerDeg(controller.adaptateur, 90, 50, controller.dt),
            Go(controller.adaptateur, 50, 50,50, controller.dt),
            TournerDeg(controller.adaptateur, 90, 50, controller.dt),
            Go(controller.adaptateur, 50, 50,50, controller.dt),
            TournerDeg(controller.adaptateur, 90, 50, controller.dt),
            Go(controller.adaptateur, 50, 50,50, controller.dt),
            TournerDeg(controller.adaptateur, 90, 50, controller.dt)
            ]
    strat = StrategieSequentielle(controller.adaptateur, steps, dt_controller)
    controller.add_strat(strat)

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
