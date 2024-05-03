from src.controller.ai import Go, StrategieSequentielle, TournerDeg, StrategieIf, Stop, Strategie, StrategieWhile

def test_while(controller) -> Strategie:
    tracer_parcours = True
    valeur = controller.adaptateur.rayon
    print (valeur)
    strat_go = Go(controller.adaptateur, 3, 50, 50, tracer_parcours)
    strat_tourner = TournerDeg(controller.adaptateur, 90, 50, tracer_parcours)
    # tant que la distance > valeur faire strategie
    strat = [StrategieSequentielle(controller,[StrategieWhile(controller.adaptateur, strat_go, 10), strat_tourner])
             for _ in range(4)]

    return StrategieSequentielle(controller, strat)


def test_if(controller) -> Strategie:
    stop = Stop(controller.adaptateur)
    strat_go = test_go_avec_tracer(controller)
    strat_carre = test_strat_seq_carre(controller)
    # faire strat_go si la distance >200 sinon rien faire
    # puis rien faire si distance >200 sinon faire carre
    liste_strat = [StrategieIf(controller.adaptateur, strat_go, stop, 200), StrategieIf(controller.adaptateur, stop, strat_carre, 200)]
    strat = StrategieSequentielle(controller.adaptateur, liste_strat)
    return strat


def test(controller) -> Strategie:
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
    return strat


def test_avec_sans_tracer(controller) -> StrategieSequentielle:
    liste = []
    for i in range(4):
        liste.append(Go(controller.adaptateur, 50, 50, 50, i % 2 == 0))
        liste.append(TournerDeg(controller.adaptateur, 90, 50, True))
    strat = StrategieSequentielle(controller.adaptateur, liste)
    return strat


def test_strat_seq_carre(controller) -> StrategieSequentielle:
    tracer_parcours = True
    vitesse = 100
    distance = 200
    steps = [Go(controller.adaptateur, distance, vitesse, vitesse, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, vitesse, tracer_parcours),
             Go(controller.adaptateur, distance, vitesse, vitesse, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, vitesse, tracer_parcours),
             Go(controller.adaptateur, distance, vitesse, vitesse, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, vitesse, tracer_parcours),
             Go(controller.adaptateur, distance, vitesse, vitesse, tracer_parcours),
             TournerDeg(controller.adaptateur, 90, vitesse, tracer_parcours)
             ]
    strat = StrategieSequentielle(controller.adaptateur, steps)
    return strat

def test_tourner90(controller)->Strategie:
    strat = TournerDeg(controller.adaptateur, 90, 50)
    return strat

def test_go_sans_tracer(controller) -> Strategie:
    strat = Go(controller.adaptateur, 10, 100, 100)
    return strat


def test_go_avec_tracer(controller) -> Strategie:
    tracer_parcours = True
    strat = Go(controller.adaptateur, 50, 50, 50, tracer_parcours)
    return strat
