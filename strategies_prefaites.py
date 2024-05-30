from src.controller.ai import Go, StrategieSequentielle, TournerDeg, StrategieIf, Stop, Strategie, StrategieWhile, StrategieFor

def test_while(controller) -> Strategie:
    """ Fonction qui execute une strategie for contenant une strategie while
    :param controller: Controleur
    :return: Strategie
    """
    distance = 5
    vitesse = 50
    angle = 90
    tracer_parcours = True
    seuil_collision = controller.adaptateur.rayon

    strat_go = Go(controller.adaptateur, distance, vitesse, vitesse, tracer_parcours)
    strat_tourner = TournerDeg(controller.adaptateur, angle, vitesse, tracer_parcours)
    # tant que la distance > seuil_collision faire lastrategie
    strat_while = StrategieWhile(controller.adaptateur, strat_go, seuil_collision)
    strat_seq = StrategieSequentielle(controller.adaptateur, [strat_while, strat_tourner])

    return StrategieFor(controller.adaptateur, strat_seq, 4)


def test_if(controller) -> Strategie:
    """ Fonction qui execute une strategie sequentielle contenant une strategie if
    :param controller: Controleur
    :return: StrategieSequentielle
    """
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
    """ Fonction qui execute une strategie sequentielle qui combine avec et sans tracer le parcours
    :param controller: Controleur
    :return: StrategieSequentielle
    """
    liste = []
    for i in range(4):
        liste.append(Go(controller.adaptateur, 50, 50, 50, i % 2 == 0))
        liste.append(TournerDeg(controller.adaptateur, 90, 50, True))
    strat = StrategieSequentielle(controller.adaptateur, liste)
    return strat


def test_strat_seq_carre(controller) -> StrategieFor:
    """ Fonction qui execute la tracage du carre 
    :param controller: Controleur
    :return: StrategieFor
    """
    tracer_parcours = True
    vitesse = 100
    distance = 200
    angle = 90
    strat_seq = StrategieSequentielle(controller.adaptateur, 
                                      [Go(controller.adaptateur, distance, vitesse, vitesse, tracer_parcours),
                                       TournerDeg(controller.adaptateur, 90, vitesse, tracer_parcours)]
    )

    return StrategieFor(controller.adaptateur, strat_seq, 4)

def test_tourner90(controller)->Strategie:
    """ Fonction qui execute une rotation de 90 degres
    :param controller: Controleur
    :return: Strategie
    """
    strat = TournerDeg(controller.adaptateur, 90, 50)
    return strat

def test_go_sans_tracer(controller) -> Strategie:
    """ Fonction qui execute la strategie Go sans tracer le parcours
    :param controller: Controleur
    :return: Strategie
    """
    strat = Go(controller.adaptateur, 10, 100, 100)
    return strat


def test_go_avec_tracer(controller) -> Strategie:
    """ Fonction qui execute la strategie Go avec tracer le parcours
    :param controller: Controleur
    :return: Strategie
    """
    tracer_parcours = True
    strat = Go(controller.adaptateur, 50, 50, 50, tracer_parcours)
    return strat
