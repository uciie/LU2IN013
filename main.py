import threading

from src.controller.adaptateur_robot_simu import AdaptateurRobotSimu
from src.controller.ai import (Go, StrategieFor, StrategieSequentielle,
                               StrategieTrouverBalise, StrategieWhile,
                               TournerDeg)
from src.controller.controleur import Controleur
from src.modele.objets import Arene, ObstacleRectangle, SimuRobot
from src.modele.simulation import Simulation
from src.modele.utilitaire import Vecteur
from src.view.affichage2d import Affichage2D
from src.view.class_3d import Affichage3D
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

        # Obstacle
        obs1 = ObstacleRectangle(40, 40, Vecteur(10, 10), Vecteur(20, 20), color="red")
        obs2 = ObstacleRectangle(400, 400, Vecteur(10, 10), Vecteur(20, 20), color="green")
        obs3 = ObstacleRectangle(400, 40, Vecteur(10, 10), Vecteur(20, 20), color="blue")
        obs4 = ObstacleRectangle(70, 400, Vecteur(10, 10), Vecteur(20, 20), color="yellow")
        obs5 = ObstacleRectangle(self.robot.pos_x, 40, Vecteur(10, 10), Vecteur(20, 20), color="purple")

        # Ajouter obstacle dans l'_arene
        self.arene.add_obstacle(obs1)
        self.arene.add_obstacle(obs2)
        self.arene.add_obstacle(obs3)
        self.arene.add_obstacle(obs4)
        self.arene.add_obstacle(obs5)

        # Créer la simulation
        simu = Simulation("Simulation", dt_simu, self.robot, self.arene, lock_sim)

        # Créer l'adaptateur
        self.adaptateur = AdaptateurRobotSimu(self.robot, simu)

        # Création du module Controller
        self.controller = Controleur(self.adaptateur, dt_controller)

        simu.start()
        self.controller.start()


        #Choix entre la 2D et la 3D
        self.choix = input("0 : 2D      1 : 3D      2 : 2D et 3D\n")

        if (self.choix == "0" or self.choix == "2"):
            # Création du module View
            view = Affichage2D(simu, dt_affichage, lock_aff)
            # Ajout du lien de communication entre view et controller
            view.controller = self.controller
            
            # demarrage des threads
            view_thread = threading.Thread(target=view.run)
            
            view_thread.start()
            
            # Ajout du lien de communication entre view et controller
            view.controller = self.controller

        if (self.choix == "1" or self.choix == "2"):
            # Création du module View3D
            self.view3D = Affichage3D(simu)
            
            # Ajouter l'affichage 3D dans l'adaptateur
            self.adaptateur.set_affichage3d(self.view3D)

if __name__ == '__main__':
    demo = Demo()
    #variable pour les strategies
    distance = 50
    vitesse = 10
    angle = 90
    seuil_collision = 50
    activer_tracer = True
    nb_repetition = 4

    # strategies pour aller vers obstacle et à chaque rencontre tourner de 90 degres
    avancer = Go(demo.adaptateur, distance, vitesse, vitesse, activer_tracer)
    avancer_jusqua = StrategieWhile(demo.adaptateur, avancer, seuil_collision)
    touner = TournerDeg(demo.adaptateur, angle, vitesse, activer_tracer)
    strat_repeter = StrategieSequentielle(demo.adaptateur, [avancer_jusqua, touner])
    tracer_carre = StrategieFor(demo.adaptateur, strat_repeter, nb_repetition)
    balise = StrategieTrouverBalise(demo.adaptateur)
    #ajout de la strategie
    demo.controller.add_strat(balise)
    if (demo.choix == "1" or demo.choix == "2"):
        demo.view3D.run()