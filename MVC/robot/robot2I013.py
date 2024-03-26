from MVC.controller.ai import Go, StrategieSequentielle, TournerDeg, StrategieIf, Stop, Strategie


def test_if(controller) -> StrategieIf:
    stop = Stop(controller.adaptateur)
    strat_a = test_go_avec_tracer(controller)
    strat_b = test_strat_seq_carre(controller)

    strat = StrategieIf(controller.adaptateur, strat_a, stop, 200)#, StrategieIf(controller.adaptateur, strat_b, stop, 200)]

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
    return strat


def test_go_sans_tracer(controller) -> Strategie:
    tracer_parcours = False
    strat = Go(controller.adaptateur, 50, 50, 50, tracer_parcours)
    return strat


def test_go_avec_tracer(controller) -> Strategie:
    tracer_parcours = True
    strat = Go(controller.adaptateur, 50, 50, 50, tracer_parcours)
    return strat
