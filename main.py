from controleur import Controleur
from view.affichage import Affichage
from .modele.arene import Arene

def main():
    arene = Arene()
    view = Affichage()
    simulation = Controleur(arene, view)

    simulation.run()

main()