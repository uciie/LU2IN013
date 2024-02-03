# @authors Équipe HELMS

# Bibliothèque des couleurs pour l'affichage
from colorama import init, Fore 
init(autoreset=True) # Initialisation pour la couleur

# On admettra que la dimension de la grille est forcément plus grande que celle du robot.
# Une grille peut contenir au moins un robot.

class Grille:
    def __init__(self, maxX: int, maxY: int, echelle: int):
        """Initialisation de l'environnement.

        :param maxX: Longueur x de la grille.
        :param maxY: Largeur y de la grille.
        :param echelle: Correspondance entre une case de la grille et sa taille réelle.
        :returns: Retourne la grille générée.
        """

        self.echelle = echelle
        self.maxX = int(maxX)  # Taille maximale en x de la fenêtre.
        self.maxY = int(maxY)  # Taille maximale en y de la fenêtre.
        self.grille = [["0" for case in range(self.maxY)] for ligne in range(self.maxX)]

    def affiche(self):
        """Affiche la grille avec son contenu (obstacles, robots, etc.).
        """
        print("-" * (self.maxX + 2))

        for ligne in self.grille:
            print("|", end='')
            for contenu in ligne:
                if contenu == "R":  # Affiche le robot en rouge.
                    print(Fore.RED + contenu, end='')
                else:
                    print(contenu, end='')
            print("|")

        print("-" * (self.maxX + 2))
