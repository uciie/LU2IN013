from ..modele.vecteur import Vecteur


class Roue:
    def __init__(self, rayon: float, vmax_ang: float):
        """Initialisation d'une roue

        :param rayon: Le rayon de la roue
        :param vmax_ang: La vitesse angulaire maximale de la roue
        """
        self._rayon = rayon  # m
        self._vmax_ang = vmax_ang  # rad/s
        self._vitesse_angulaire = 0.0  # rad/s

    @property
    def rayon(self) -> float:
        """Obtient le rayon de la roue."""
        return self._rayon

    @property
    def vmax_ang(self) -> float:
        """Obtient la vitesse angulaire maximale de la roue."""
        return self._vmax_ang

    @property
    def vitesse_angulaire(self) -> float:
        """Obtient la vitesse angulaire actuelle de la roue."""
        return self._vitesse_angulaire

    @vitesse_angulaire.setter
    def vitesse_angulaire(self, value: float) -> None:
        """Modifie la vitesse angulaire de la roue, en s'assurant qu'elle ne dépasse pas la vitesse maximale.

        :param value: Nouvelle vitesse angulaire de la roue.
        """
        self._vitesse_angulaire = min(value, self._vmax_ang)


class Capteur:
    def __init__(self, vecteur: Vecteur):
        """Initialisation du capteur

        :param vecteur : Vecteur directeur envoyé
        :returns : Retourne une instance de la classe Capteur
        """
        # Vecteur directeur
        self._vecteur = vecteur
        self._deg_max = 10
        self._active = False

    @property
    def vecteur(self):
        """Propriété pour l'attribut vecteur"""
        return self._vecteur

    @property
    def deg_max(self) -> float:
        """Propriété pour l'attribut deg_max
        :returns : Le degree maximale du capteur
        """
        return self._deg_max

    @property
    def active(self) -> bool:
        """Propriété pour l'attribut active
        :return: True si le capteur est active et False sinon
        """
        return self._active

    @active.setter
    def active(self, value: bool):
        self._active = value
