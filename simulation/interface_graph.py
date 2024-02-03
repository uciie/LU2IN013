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

    def draw_roue(self, Roue: Any) -> None:
        """Dessine une roue sur le canevas de l'interface.

        :param Roue: Roue à dessiner.
        """
        self.canvas.create_line(
            Roue.posX, Roue.posY,
            Roue.posX + Roue.vectDir.x * 5, Roue.posY + Roue.vectDir.y * 5,
            arrow=tk.LAST)

    def draw_obj(self, Objet: Any) -> int:
        """Dessine un objet sur le canevas de l'interface.

        :param Objet: Objet à dessiner.
        :return: Identifiant unique de l'objet sur le canevas.
        """
        # Coordonnées des sommets du polygone
        x1, y1 = Objet.posX - Objet.width/2, Objet.posY - Objet.length/2
        x2, y2 = Objet.posX + Objet.width/2, Objet.posY - Objet.length/2
        x3, y3 = Objet.posX + Objet.width/2, Objet.posY + Objet.length/2
        x4, y4 = Objet.posX - Objet.width/2, Objet.posY + Objet.length/2

        poly_coords = [x1, y1, x2, y2, x3, y3, x4, y4]

        poly_id = self.canvas.create_polygon(poly_coords, fill=Objet.color)

        if hasattr(Objet, 'vectDir'):
            arrow_id = self.canvas.create_line(
                Objet.posX, Objet.posY,
                Objet.posX + Objet.vectDir.x * Objet.length, Objet.posY + Objet.vectDir.y * Objet.length,
                arrow=tk.LAST)

            return poly_id, arrow_id
        else:
            return poly_id

    
    def draw_parcours(self, Objet: Any) -> int:
        """ Trace le parcours de l'objet

        :param Objet: Objet 
        :return: Identifiant unique de l'objet sur le canevas.
        """
        return self.canvas.create_line(Objet.lastPosX,Objet.lastPosY,Objet.posX,Objet.posY,fill='blue', width=3)

    def delete_draw(self, *obj_ids: int) -> None:
        """Supprime un ou plusieurs dessins de l'interface.

        :param obj_ids: Identifiants des objets à supprimer du canevas.
        """
        for obj_id in obj_ids:
            if obj_id:
                self.canvas.delete(obj_id)
    
    
    def creer_button(self, name: str, command: callable) -> tk.Button:
        """Crée un bouton dans l'interface.

        :param name: Nom du bouton.
        :param command: Fonction à exécuter lorsque le bouton est cliqué.
        :returns: Objet tk.Button créé.
        """
        return tk.Button(self.root, text=name, command=command)
