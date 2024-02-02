import tkinter as tk
from typing import Any

class Interface:
    def __init__(self, name: str, width: int, height: int, color: str) -> None:
        """Initialise une interface graphique.

        :param name: Nom de l'interface.
        :param width: Largeur de l'interface.
        :param height: Hauteur de l'interface.
        :param color: Couleur de fond de l'interface.
        """
        self.root = tk.Tk()
        self.root.title(name)
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=color)
        self.canvas.pack()

    def draw_obj(self, Objet: Any) -> None:
        """ Dessine un objet sur le canevas de l'interface.

        :param Objet: Objet à dessiner.
        """
        self.canvas.create_rectangle( 
            Objet.posX - Objet.width/2, Objet.posY - Objet.length/2, 
            Objet.posX + Objet.width/2, Objet.posY + Objet.length/2, fill=Objet.color)
        
        if hasattr(Objet, 'vectDir') :
            self.canvas.create_line(
                Objet.posX, Objet.posY,
                Objet.posX + Objet.vectDir.x * Objet.length, Objet.posY + Objet.vectDir.y * Objet.length,
                arrow=tk.LAST)

    def draw_roue(self, Roue: Any) -> None:
        """Dessine une roue sur le canevas de l'interface.

        :param Roue: Roue à dessiner.
        """
        self.canvas.create_line(
            Roue.posX, Roue.posY,
            Roue.posX + Roue.vectDir.x * 5, Roue.posY + Roue.vectDir.y * 5,
            arrow=tk.LAST)

    def delete_draw(self, Objet: Any) -> None:
        """Supprime un dessin de l'interface.

        :param Objet: Objet à supprimer du canevas.
        """
        if Objet:
            self.canvas.delete(Objet)
    
    def creer_button(self, name: str, command: callable) -> tk.Button:
        """Crée un bouton dans l'interface.

        :param name: Nom du bouton.
        :param command: Fonction à exécuter lorsque le bouton est cliqué.
        :returns: Objet tk.Button créé.
        """
        return tk.Button(self.root, text=name, command=command)
