from MVC.modele.simulation import Arene
from MVC.modele.vecteur import Vecteur
from MVC.controller.adaptateur_robot_simu import AdaptateurRobotSimu


def q11(arene : Arene): 
    obs1 = ObstacleRectangle(100, 170, Vecteur(50, 50), Vecteur(50, 50), color="orange")
    obs2 = ObstacleRectangle(150, 410, Vecteur(50, 50), Vecteur(50, 50), color="orange")
    obs3 = ObstacleRectangle(250, 100, Vecteur(50, 50), Vecteur(50, 50), color="orange")
    obs4 = ObstacleRectangle(340, 120, Vecteur(50, 50), Vecteur(50, 50), color="orange")
    obs5 = ObstacleRectangle(400, 340, Vecteur(50, 50), Vecteur(50, 50), color="orange")

    arene.add_obstacle(obs1)
    arene.add_obstacle(obs2)
    arene.add_obstacle(obs3)
    arene.add_obstacle(obs4)
    arene.add_obstacle(obs5)


def q14():
    """
    On suppose que Go_cap avance jusqu'à un obstacle
    """
    steps = [Go_cap(controller.adaptateur, 50, 50, tracer_parcours), TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
            Go_cap(controller.adaptateur, 50, 50, tracer_parcours), TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
            Go_cap(controller.adaptateur, 50, 50, tracer_parcours), TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
            Go_cap(controller.adaptateur, 50, 50, tracer_parcours), TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
            Go_cap(controller.adaptateur, 50, 50, tracer_parcours), TournerDeg(controller.adaptateur, 90, 50, tracer_parcours)]
    strategie = StrategieSequentielle(step)
    controller.add_strat(strategie)




