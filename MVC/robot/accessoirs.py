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


