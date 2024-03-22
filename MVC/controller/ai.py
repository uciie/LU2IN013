import math

from ..controller.controleur import Strategie, Adaptateur

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Go(Strategie):
    def __init__(self, adaptateur: Adaptateur, distance: float, v_ang_d: float, v_ang_g: float, dt: float) -> None:
        """
        Fait avancer le robot d'une certaine distance
        :param adaptateur: Le robot qui va faire le deplacement
        :param distance: La distance que le robot doit parcourir (float)
        :param v_ang_d: La vitesse angulaire de la roue droite du robot en rad/s
        :param v_ang_g: La vitesse angulaire de la roue gauche du robot en rad/s
        :param dt: Le dt
        """
        super().__init__()  # Appel du constructeur de la classe parente
        self.adaptateur = adaptateur

        self.pos_ini = None
        self.distance = distance

        self.v_ang_d, self.v_ang_g = v_ang_d, v_ang_g

        # compteur de distance deja parcouru
        self.parcouru = 0.

        # le dt
        self.dt = dt

    def start(self):
        """ Commencer la strategie
        """
        # Modifier les vitesses angulaires les roues
        self.adaptateur.set_vitesse_roue(self.v_ang_d, self.v_ang_g)  # Vitesse angulaire droite/gauche

        # Position initiale du robot avant de commencer
<<<<<<< HEAD
        self.pos_ini = 1. * self.adaptateur.distance_parcourue
=======
        self.pos_ini = self.adaptateur.distance_parcourue
>>>>>>> test_robot_irl

        # compteur de distance deja parcouru
        self.parcouru = 0.

    def stop(self):
        """ Savoir le parcours est fini ou non

        :return : Retourne vrai si on a fini de parcourir la distance
        """
        v_roue_d, v_roue_g = self.adaptateur.vitesse_ang_roues
<<<<<<< HEAD
        print("parcouru", self.parcouru , "distance", self.distance)
=======
>>>>>>> test_robot_irl
        return math.fabs(self.parcouru) >= math.fabs(self.distance)  # or (v_roue_d == 0 and v_roue_g == 0)

    def step(self):
        """ Faire un deplacement de dOM
        """
        # Incrémenter la distance parcourue
        self.parcouru += self.adaptateur.distance_parcourue
        if self.stop():
<<<<<<< HEAD
            print("STOP")
=======
>>>>>>> test_robot_irl
            # Mettre à 0 les vitesses

            self.adaptateur.stop()
            return

        #self.adaptateur.actualiser()


class TournerDeg(Strategie):
    def __init__(self, adaptateur: Adaptateur, angle: float, v_ang: float, dt: float) -> None:
        """
        Fait avancer le robot d'un certain angle
        :param adaptateur: Le robot qui va faire le deplacement
        :param angle: L'angle que le robot doit tourner en degree
        :param v_ang: La vitesse angulaire du robot en rad/s
        :param dt: Le dt
        """
        super().__init__()  # Appel du constructeur de la classe parente
        self.pos_ini = None
        self.adaptateur = adaptateur

        self.angle, self.v_ang = angle, v_ang

        # compteur de distance deja parcouru
        self.parcouru = 0.

        # le dt
        self.dt = dt

    def start(self):
        """ Commencer la strategie
        """
        # Modifier les vitesses angulaires les roues
        # Tourner à droite
        if self.angle > 0:
            self.v_ang_d, self.v_ang_g = self.v_ang, -self.v_ang
            self.adaptateur.set_vitesse_roue(self.v_ang, -self.v_ang)  # Vitesse angulaire droite/gauche
        # Tourner à gauche
        else:
            self.v_ang_d, self.v_ang_g = -self.v_ang, self.v_ang
            self.adaptateur.set_vitesse_roue(-self.v_ang, self.v_ang)  # Vitesse angulaire droite/gauche

        # Position initiale du robot avant de commencer
        self.pos_ini = 1. * self.adaptateur.angle_parcourue

        # compteur de distance deja parcouru
        self.parcouru = 0.

    def stop(self) -> bool:
        """ Savoir le parcours est fini ou non

        :return : Retourne vrai si on a fini de parcourir l'angle
        """
<<<<<<< HEAD
        print("parcouru", self.parcouru, "angle", self.angle)
=======
        #print(self.parcouru)
>>>>>>> test_robot_irl
        return math.fabs(self.parcouru) >= math.fabs(self.angle)

    def step(self):
        """ Faire un deplacement de dOM
        """
        # Incrémenter l'angle parcouru
        self.parcouru += self.adaptateur.angle_parcourue
        if self.stop():
<<<<<<< HEAD
            print("STOP")
=======
>>>>>>> test_robot_irl
            # Mettre à 0 les vitesses
            self.adaptateur.stop()
            return

        #self.adaptateur.actualiser()


class TracerCarre(Strategie):
    def __init__(self, adaptateur: Adaptateur, distance_cote: float, v_ang: float, dt: float) -> None:
        """
        Tracer un carre
        :param adaptateur: Le robot qui va faire le deplacement
        :param distance_cote: La distance du cote du carre
        :param v_ang: La vitesse angulaire du robot en rad/s
        :param dt: Le dt
        """
        super().__init__()  # Appel du constructeur de la classe parente
        self.adaptateur = adaptateur

        self.pos_ini = None
        self.distance_cote = distance_cote
        self.v_ang = v_ang
        # compteur de distance deja parcouru
        self.parcouru = 0.
        # le dt
        self.dt = dt
        # Liste d'etapes pour tracer un carre
        self.steps = [
            Go(adaptateur, distance_cote, v_ang, v_ang, dt),
            TournerDeg(adaptateur, 90, v_ang, dt),
            Go(adaptateur, distance_cote, v_ang, v_ang, dt),
            TournerDeg(adaptateur, 90, v_ang, dt),
            Go(adaptateur, distance_cote, v_ang, v_ang, dt),
            TournerDeg(adaptateur, 90, v_ang, dt),
            Go(adaptateur, distance_cote, v_ang, v_ang, dt)
        ]

        self.current_step = 0

    def start(self):
        """ Commencer la strategie
        """
        self.current_step = 0
        self.steps[self.current_step].start()

    def stop(self) -> bool:
        """ Savoir le parcours est fini ou non

        :return : Retourne vrai si on a fini son carre
        """
        return self.current_step >= len(self.steps) or self.steps[self.current_step].stop()

    def step(self):
        """Effectue une étape de la séquence de traçage du carré."""
        if self.stop():
            return
        self.steps[self.current_step].step()
        if self.steps[self.current_step].stop():
            self.current_step += 1
            if self.current_step < len(self.steps):
                self.steps[self.current_step].start()