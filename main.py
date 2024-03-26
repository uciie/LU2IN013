import threading

from MVC.controller.adaptateur_robot_simu import AdaptateurRobotSimu
from MVC.controller.controleur import Controleur
from MVC.modele.objets import Arene, ObstacleRectangle, SimuRobot
from MVC.modele.simulation import Simulation
from MVC.modele.vecteur import Vecteur
from MVC.view.affichage import Affichage

from strategies_prefaites import test_if


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

        # Initialisation de l'arene, robot, obstacle
        arene = Arene("Simulation de déplacement du robot", largeur, hauteur, echelle)
        self.robot = SimuRobot("R", int(largeur / 2), int(hauteur / 2), dim_robot_x, dim_robot_y, 10, 150, color="red")
        obs = ObstacleRectangle(100, 100, Vecteur(10, 10), Vecteur(20, 20), color="blue")

        # Ajouter un obstacle dans l'arene
        arene.add_obstacle(obs)

        # Créer la simulation
        simu = Simulation("Simulation", dt_simu, self.robot, arene, lock_sim)

        # Créer l'adaptateur
        self.adaptateur = AdaptateurRobotSimu(self.robot, simu)

        # Création du module View
        view = Affichage(simu, dt_affichage, lock_aff)

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
    print(demo.adaptateur.get_distance)
    demo.controller.add_strat(test_if(demo.controller))