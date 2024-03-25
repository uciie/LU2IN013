import threading

from MVC.controller.adaptateur_robot_simu import AdaptateurRobotSimu
from MVC.controller.controleur import Controleur
from MVC.controller.ai import Go, StrategieSequentielle
from MVC.modele.objets import Arene, ObstacleRectangle, SimuRobot
from MVC.modele.simulation import Simulation
from MVC.modele.vecteur import Vecteur
from MVC.view.affichage import Affichage


class Demo():
    def __init__(self):
        lock_aff = threading.RLock()
        lock_sim = threading.RLock()

        dt_simu = 1 / 27000
        dt_controller = 1 / 3000000
        dt_affichage = 1 / 300000
        echelle = 5
        largeur, hauteur = 500, 500
        dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

        # Initialisation de l'arene, robot, obstacle
        self.arene = Arene("Simulation de déplacement du robot", largeur, hauteur, echelle)
        self.robot = SimuRobot("R", int(largeur / 2), int(hauteur / 2), dim_robot_x, dim_robot_y, 10, 150, color="red")

        # Créer la simulation
        simu = Simulation("Simulation", dt_simu, self.robot, self.arene, lock_sim)

        # Créer l'adaptateur
        self.adaptateur = AdaptateurRobotSimu(self.robot, simu)

        # Création du module View
        self.view = Affichage(simu, dt_affichage, lock_aff)

        # Création du module Controller
        self.controller = Controleur(self.adaptateur, dt_controller)

        # Ajout du lien de communication entre view et controller
        self.view.controller = self.controller

        # demarrage des threads
        view_thread = threading.Thread(target=self.view.run)

        view_thread.start()
        simu.start()
        self.controller.start()

        # Ajout du lien de communication entre view et controller
        self.view.controller = self.controller

demo = Demo()
def q1_1(demo: Demo):
    # Obstacle
    obs1 = ObstacleRectangle(40, 40, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs2 = ObstacleRectangle(400, 400, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs3 = ObstacleRectangle(400, 40, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs4 = ObstacleRectangle(40, 400, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs5 = ObstacleRectangle(demo.robot.pos_x, 40, Vecteur(10, 10), Vecteur(20, 20), color="blue")

    # Ajouter obstacle dans l'arene
    demo.arene.add_obstacle(obs1)
    demo.arene.add_obstacle(obs2)
    demo.arene.add_obstacle(obs3)
    demo.arene.add_obstacle(obs4)
    demo.arene.add_obstacle(obs5)

def q1_2(liste_obs : list[ObstacleRectangle]):
    for obs in liste_obs:
        obs.color = "#FFA500"

def q1_3(demo):
    # dessine(bool: b) = activer_tracer_parcours(True) fonction deja presente dans le code
    demo.robot.activer_tracer_parcours(True)
    liste_strat = []
    liste_strat.append(Go(demo.controller.adaptateur, 50, 50, 50, demo.robot.tracer_parcours))
    demo.robot.activer_tracer_parcours(False)
    liste_strat.append(Go(demo.controller.adaptateur, 50, 50, 50, demo.robot.tracer_parcours))

    strat_seq = StrategieSequentielle(demo.controller.adaptateur, liste_strat)
    demo.controller.add_strat(strat_seq)



#q1_1(demo)
#q1_2(demo.arene.liste_Obstacles)
#q1_3(demo)