import tkinter as tk
from tkinter import ttk
from typing import Any
from modele.arene import Arene
from threading import Thread

class Affichage():
    def __init__(self, arene : Arene) -> None:
        """Initialise un Affichage graphique.

        :param name: Nom de l'Affichage.
        :param width: Largeur de l'Affichage.
        :param height: Hauteur de l'Affichage.
        :param color: Couleur de fond de l'Affichage.
        """
        self.arene = arene
        self.robot = arene.robot

        self.root = tk.Tk()
        self.root.title(arene.name)

        # Set the initial values for the variables
        self.initial_v_ang_d = -50
        self.initial_v_ang_g = 50
        self.initial_v_ang = 50
        self.initial_angle = 90
        self.initial_distance = 50

        # Créer des variables Tkinter pour la vitesse et la distance
        self.v_ang_d_var = tk.DoubleVar(value=self.initial_v_ang_d)
        self.v_ang_g_var = tk.DoubleVar(value=self.initial_v_ang_g)
        self.v_ang = tk.DoubleVar(value=self.initial_v_ang)
        self.angle = tk.DoubleVar(value=self.initial_angle)
        self.distance_var = tk.DoubleVar(value=self.initial_distance)

        # Entrée pour la vitesse angulaire de roue droit
        self.v_ang_d_label = tk.Label(self.root, text="Vitesse angulaire Droite:")
        self.v_ang_d_var_entry = tk.Entry(self.root, textvariable=self.v_ang_d_var)
        self.v_ang_d_label.grid(row=0, column=0)
        self.v_ang_d_var_entry.grid(row=0, column=1)

        # Entrée pour la vitesse angulaire de roue gauche
        self.v_ang_g_label = tk.Label(self.root, text="Vitesse angulaire Gauche:")
        self.v_ang_g_var_entry = tk.Entry(self.root, textvariable=self.v_ang_g_var)
        self.v_ang_g_label.grid(row=1, column=0)
        self.v_ang_g_var_entry.grid(row=1, column=1)

        #Entrée pour la vitesse de rotation
        self.v_ang_label = tk.Label(self.root, text = "Vitesse angulaire pour la rotation:")
        self.v_ang_var_entry = tk.Entry(self.root, textvariable=self.v_ang)
        self.v_ang_label.grid(row=3, column=0)
        self.v_ang_var_entry.grid(row=3, column=1)

        #Entrée pour l'angle
        self.angle = tk.Label(self.root, text="Angle")
        self.angle_entry = tk.Entry(self.root, textvariable=self.angle)
        self.angle.grid(row=5, column=2)
        self.angle_entry.grid(row=5, column=3)

        # Entrée pour la distance
        self.distance_label = tk.Label(self.root, text="Distance:")
        self.distance_entry = tk.Entry(self.root, textvariable=self.distance_var)
        self.distance_label.grid(row=2, column=0)
        self.distance_entry.grid(row=2, column=1)

        # Go Button 
        self.go_button = tk.Button(self.root, text="Go", command=self.go_button_clicked)
        self.go_button.grid(row=5, column=0)

        # Bouton tourner en angle
        self.turn_button = tk.Button(self.root, text="Tourner", command=self.go_button_clicked)
        self.turn_button.grid(row=5,column=1)

        # Reset Button 
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_button_clicked)
        self.reset_button.grid(row=6, column=0)

        self.canvas = tk.Canvas(self.root, width=self.arene.maxX, height=self.arene.maxY, bg=self.arene.color)
        self.canvas.grid(row=4, column=0, columnspan=2)
        #self.canvas.pack()

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        """ Set le controleur

        :param controller: Le controleur
        :return:
        """
        self.controller = controller

    def reset_button_clicked(self):
        """ remettre à zero l'interface graphique 
        """
        new_affichage = Affichage(self.arene)
        self.controller.set_view(new_affichage)

    def go_button_clicked(self):
        """ Handle go button click
        """
        if self.controller:
            print("reception\n")
            self.controller.go(self.distance_var.get(), self.v_ang_d_var.get(), self.v_ang_g_var.get())

    def draw_obj(self, Objet: Any) -> int:
        """Dessine un objet sur le canevas de l'Affichage. 


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
        """Supprime un ou plusieurs dessins de l'Affichage.

        :param obj_ids: Identifiants des objets à supprimer du canevas.
        """
        for obj_id in obj_ids:
            if obj_id:
                self.canvas.delete(obj_id)
    
    def update(self):
        if self.robot.rect_id and  self.robot.arrow_id: 
            self.delete_draw(self.robot.rect_id, self.robot.arrow_id)
        self.draw_parcours(self.robot)
        self.robot.rect_id, self.robot.arrow_id = self.draw_obj(self.robot)
        self.root.update()
