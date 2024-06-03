from MVC.controller.ai import Go, StrategieSequentielle, TournerDeg


def test(controller):
    """ Tester le tourner deg avec -45 deg puis 90 """
    tracer_parcours = True
    liste = [TournerDeg(controller.adaptateur, -45, 50, True),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours)
             ]

    strat = StrategieSequentielle(controller.adaptateur, liste)
    controller.add_strat(strat)


def test_avec_sans_tracer(controller):
    liste = []
    for i in range(4):
        liste.append(Go(controller.adaptateur, 50, 50, 50, i % 2 == 0))
        liste.append(TournerDeg(controller.adaptateur, 90, 50, True))
    strat = StrategieSequentielle(controller.adaptateur, liste)
    controller.add_strat(strat)

def rencontre5Obs(controller):
    toucherObs = 0
    tracer_parcours = True
    for obstacle in self._arene.liste_Obstacles:
        if (obstacle.test_collision(self._robot) & (toucherObs<5)):
            self._robot.TournerDeg(controller.adaptateur, 90, 1000, tracer_parcours)
            toucherObs+1
            
        else : sys.exit()


def test_strat_seq_carre(controller):
    tracer_parcours = True
    steps = [Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours),
             Go(controller.adaptateur, 50, 50, 50, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, 50, tracer_parcours)
             ]
    strat = StrategieSequentielle(controller.adaptateur, steps)
    controller.add_strat(strat)


def test_go_sans_tracer(controller):
    tracer_parcours = False
    strat = Go(controller.adaptateur, 50, 50, 50, tracer_parcours)
    controller.add_strat(strat)


def test_go_avec_tracer(controller):
    tracer_parcours = True
    strat = Go(controller.adaptateur, 50, 50, 50, tracer_parcours)
    controller.add_strat(strat)
