import unittest
import threading
from MVC.controller.controleur import Controleur
from MVC.controller.adaptateur_robot_simu import AdaptateurRobotSimu
from MVC.modele.objets import Arene, SimuRobot, ObstacleRectangle
from MVC.modele.simulation import Simulation
from MVC.modele.vecteur import Vecteur
from strategies_prefaites import test_go_sans_tracer

class TestSansView(unittest.TestCase):
    def test_simulation_sans_vue(self):
        # Création du verrou
        lock_sim = threading.RLock()

        dt_simu = 1 / 24000
        dt_controller = 1 / 3000000
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

        # Créer le module Controller
        controller = Controleur(adaptateur, dt_controller)

        # Démarrer la simulation et le contrôleur
        simu.start()
        controller.start()

        # Attendre que les threads se terminent
        simu.join()
        controller.join()

        test_go_sans_tracer(controller)
        simu.stop()

        # Vérifier que la simulation s'est terminée normalement
        self.assertFalse(simu.is_alive())

if __name__ == '__main__':
    unittest.main()

