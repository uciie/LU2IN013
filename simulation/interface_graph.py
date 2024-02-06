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

        # Créer des variables Tkinter pour la vitesse et la distance
        self.vitesse_var = tk.DoubleVar(value=100)
        self.distance_var = tk.DoubleVar(value=100)
        self.angle_var = tk.DoubleVar(value=90)

        # Entrée pour la vitesse
        self.vitesse_label = tk.Label(self.root, text="Vitesse:")
        self.vitesse_entry = tk.Entry(self.root, textvariable=self.vitesse_var)
        self.vitesse_label.grid(row=0, column=0)
        self.vitesse_entry.grid(row=0, column=1)

        # Entrée pour la distance
        self.distance_label = tk.Label(self.root, text="Distance:")
        self.distance_entry = tk.Entry(self.root, textvariable=self.distance_var)
        self.distance_label.grid(row=1, column=0)
        self.distance_entry.grid(row=1, column=1)

        # Entrée pour l'angle
        self.angle_label = tk.Label(self.root, text="Angle:")
        self.angle_entry = tk.Entry(self.root, textvariable=self.angle_var)
        self.angle_label.grid(row=2, column=0)
        self.angle_entry.grid(row=2, column=1)
        
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=color)
        self.canvas.grid(row=4, column=0, columnspan=2)
        #self.canvas.pack()

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
        :returns: Identifiant unique de l'objet sur le canevas.
        """
        # Coordonnées des sommets du polygone
        u_x = Objet.vectDir.rotation(90).multiplication(Objet.width/2)
        u_y = Objet.vectDir.multiplication(Objet.length/2)

        OA = u_x.multiplication(-1).soustraction(u_y)
        OB = u_x.multiplication(-1).add(u_y)
        OC = u_x.add(u_y)
        OD = u_x.soustraction(u_y)

        x1, y1 = Objet.posX + OA.x , Objet.posY + OA.y
        x2, y2 = Objet.posX + OB.x , Objet.posY + OB.y
        x3, y3 = Objet.posX + OC.x , Objet.posY + OC.y
        x4, y4 = Objet.posX + OD.x , Objet.posY + OD.y

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
        :returns: Identifiant unique de l'objet sur le canevas.
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
    
    def creer_var_tk(self, value: int) -> tk.DoubleVar:
        """ Crée une variable Tkinter

        :param value: La valeur initiale de la variable 
        :returns: Variable tk.DoubleVar cree
        """
        return tk.DoubleVar(value=value)
    


