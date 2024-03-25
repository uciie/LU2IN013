import threading

from MVC.controller.adaptateur_robot_simu import AdaptateurRobotSimu
from MVC.controller.controleur import Controleur
from MVC.modele.objets import Arene, ObstacleRectangle, SimuRobot
from MVC.modele.simulation import Simulation
from MVC.modele.vecteur import Vecteur
from MVC.view.affichage import Affichage

def q1_1():
    lock_aff = threading.RLock()
    lock_sim = threading.RLock()

    dt_simu = 1 / 27000
    dt_controller = 1 / 3000000
    dt_affichage = 1 / 300000
    echelle = 5
    largeur, hauteur = 500, 500
    dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

    # Initialisation de l'arene, robot, obstacle
    arene = Arene("Simulation de déplacement du robot", largeur, hauteur, echelle)
    robot = SimuRobot("R", int(largeur / 2), int(hauteur / 2), dim_robot_x, dim_robot_y, 10, 150, color="red")

    # Obstacle
    obs1 = ObstacleRectangle(40, 40, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs2 = ObstacleRectangle(400, 400, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs3 = ObstacleRectangle(400, 40, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs4 = ObstacleRectangle(40, 400, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs5 = ObstacleRectangle(int(largeur / 2), 40, Vecteur(10, 10), Vecteur(20, 20), color="blue")

    # Ajouter obstacle dans l'arene
    arene.add_obstacle(obs1)
    arene.add_obstacle(obs2)
    arene.add_obstacle(obs3)
    arene.add_obstacle(obs4)
    arene.add_obstacle(obs5)

    # Créer la simulation
    simu = Simulation("Simulation", dt_simu, robot, arene, lock_sim)

    # Créer l'adaptateur
    adaptateur = AdaptateurRobotSimu(robot, simu)

    # Création du module View
    view = Affichage(simu, dt_affichage, lock_aff)

    # Création du module Controller
    controller = Controleur(adaptateur, dt_controller)

    # Ajout du lien de communication entre view et controller
    view.controller = controller

    # demarrage des threads
    view_thread = threading.Thread(target=view.run)

    view_thread.start()
    simu.start()
    controller.start()

    # Ajout du lien de communication entre view et controller
    view.controller = controller

q1_1()