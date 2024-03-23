from MVC.controller.ai import Go, StrategieSequentielle, TournerDeg

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
    strat = StrategieSequentielle(controller.adaptateur, steps, tracer_parcours)
    controller.add_strat(strat)


def test_go_sans_tracer(controller):
    tracer_parcours = False
    strat = Go(controller.adaptateur, 50, 50, 50, tracer_parcours)
    controller.add_strat(strat)


def test_go_avec_tracer(controller):
    tracer_parcours = True
    strat = Go(controller.adaptateur, 50, 50, 50, tracer_parcours)
    controller.add_strat(strat)