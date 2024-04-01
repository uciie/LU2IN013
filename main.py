import threading

from src.controller.adaptateur_robot_simu import AdaptateurRobotSimu
from src.controller.controleur import Controleur
from src.modele.objets import Arene, ObstacleRectangle, SimuRobot
from src.modele.simulation import Simulation
from src.modele.utilitaire import Vecteur
from src.view.affichage2d import Affichage2D

from strategies_prefaites import test_if, test_while


class Demo:
    """Demonstration du jour """

    def __init__(self):
        # Création du verrou
        lock_aff = threading.RLock()
        lock_sim = threading.RLock()

        dt_simu = 1 / 27000
        dt_controller = 1 / 3000000
        dt_affichage = 1 / 300000
        echelle = 5
        largeur, hauteur = 500, 500
        dim_robot_x, dim_robot_y = int(largeur / 10), int(hauteur / 10)

        # Initialisation de l'self._arene, robot, obstacle
        self.arene = Arene("Simulation de déplacement du robot", largeur, hauteur, echelle)
        self.robot = SimuRobot("R", int(largeur / 2), int(hauteur / 2), dim_robot_x, dim_robot_y, 10, 150, color="red")
        obs = ObstacleRectangle(100, 100, Vecteur(10, 10), Vecteur(20, 20), color="blue")

        # Ajouter un obstacle dans l'_arene
        #self._arene.add_obstacle(obs)

        # Créer la simulation
        simu = Simulation("Simulation", dt_simu, self.robot, self.arene, lock_sim)

        # Créer l'adaptateur
        self.adaptateur = AdaptateurRobotSimu(self.robot, simu)

        # Création du module View
        view = Affichage2D(simu, dt_affichage, lock_aff)

        # Création du module Controller
        self.controller = Controleur(self.adaptateur, dt_controller)

        # Ajout du lien de communication entre view et controller
        view.controller = self.controller

        # demarrage des threads
        view_thread = threading.Thread(target=view.run)

        view_thread.start()
        simu.start()
        self.controller.start()

        # Ajout du lien de communication entre view et controller
        view.controller = self.controller


if __name__ == '__main__':
    demo = Demo()
    # Obstacle
    obs1 = ObstacleRectangle(40, 40, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs2 = ObstacleRectangle(400, 400, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs3 = ObstacleRectangle(400, 40, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs4 = ObstacleRectangle(40, 400, Vecteur(10, 10), Vecteur(20, 20), color="blue")
    obs5 = ObstacleRectangle(demo.robot.pos_x, 40, Vecteur(10, 10), Vecteur(20, 20), color="blue")

    # Ajouter obstacle dans l'_arene
    demo.arene.add_obstacle(obs1)
    demo.arene.add_obstacle(obs2)
    demo.arene.add_obstacle(obs3)
    demo.arene.add_obstacle(obs4)
    demo.arene.add_obstacle(obs5)

    demo.controller.add_strat(test_while(demo.controller))