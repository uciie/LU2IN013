import tkinter as tk
from typing import Any
from modele.arene import Arene
from controller.controleur import Go, Go_cap, Tourner_deg, Tracer_carre, Test_collision

class Affichage():
    def __init__(self, arene:Arene):
        """Initialise un Affichage graphique.

        :param name: Nom de l'Affichage.
        :param width: Largeur de l'Affichage.
        :param height: Hauteur de l'Affichage.
        :param color: Couleur de fond de l'Affichage.
        """
        self.arene = arene

        self.root = tk.Tk()
        self.root.title(arene.name)

        # Set the initial values for the variables
        self.initial_v_ang_d = 50
        self.initial_v_ang_g = 50
        self.initial_v_ang = 50
        self.initial_angle = 90
        self.initial_distance = 50

        # Créer des variables Tkinter pour la vitesse et la distance
        self.v_ang_d_var = tk.DoubleVar(value=self.initial_v_ang_d)
        self.v_ang_g_var = tk.DoubleVar(value=self.initial_v_ang_g)
        self.v_ang_var = tk.DoubleVar(value=self.initial_v_ang)
        self.angle_var = tk.DoubleVar(value=self.initial_angle)
        self.distance_var = tk.DoubleVar(value=self.initial_distance)

        # Creation du cadre pour les données du robot
        self.robot_frame = tk.LabelFrame(self.root, text = " Données du robot ")
        self.robot_frame.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        # Données du robot en temps réel
        self.pos_label = tk.Label(self.robot_frame, text=f"Position: ({self.arene.robot.posX:.2f}, {self.arene.robot.posY:.2f})")
        self.pos_label.grid(row=1, column=0, sticky="w", padx=5)
        self.roueD_label = tk.Label(self.robot_frame, text=f"Roue droite : {self.arene.robot.roue_droite.vitesse_angulaire} rad/s")
        self.roueD_label.grid(row=2, column=0, sticky="w", padx=5)
        self.roueG_label = tk.Label(self.robot_frame, text=f"Roue gauche : {self.arene.robot.roue_gauche.vitesse_angulaire} rad/s")
        self.roueG_label.grid(row=3, column=0, sticky="w", padx=5)

        # Creation du cadre pour la commande basic
        self.command_frame = tk.LabelFrame(self.root, text = " Commande Basic ")
        self.command_frame.grid(row=1, column=0, padx = 5, pady = 5, sticky = "ew")
        
        # Entrée pour la vitesse angulaire de roue droit
        self.v_ang_d_label = tk.Label(self.command_frame, text="Roue droite : ")
        self.v_ang_d_var_entry = tk.Entry(self.command_frame, textvariable=self.v_ang_d_var)
        self.v_ang_d_label.grid(row=1, column=0, sticky='e')
        self.v_ang_d_var_entry.grid(row=1, column=1, sticky='w', padx=5)

        # Entrée pour la vitesse angulaire de roue gauche
        self.v_ang_g_label = tk.Label(self.command_frame, text="Roue gauche : ")
        self.v_ang_g_var_entry = tk.Entry(self.command_frame, textvariable=self.v_ang_g_var)
        self.v_ang_g_label.grid(row=2, column=0, sticky='e')
        self.v_ang_g_var_entry.grid(row=2, column=1, sticky='w', padx=5)

        # Entree pour la distance de parcours
        self.distance_label = tk.Label(self.command_frame, text = "Distance : " )
        self.distance_var_entry = tk.Entry(self.command_frame, textvariable=self.distance_var)
        self.distance_label.grid(row = 3, column= 0, sticky = "e", pady = 5)
        self.distance_var_entry.grid(row = 3, column=1, sticky = "w", padx = 5, pady = 5)

        # Cadre pour la commande pour tourner
        self.turn_frame = tk.LabelFrame(self.root, text=" Commande pour Tourner ")
        self.turn_frame.grid(row=3, column=0, padx=5, pady=5, sticky="new")
        
        # Entree pour l'angle de parcours
        self.angle_var_label = tk.Label(self.turn_frame, text="Angle : ")
        self.angle_var_entry = tk.Entry(self.turn_frame, textvariable=self.angle_var)
        self.angle_var_label.grid(row=1, column=0, sticky="e", padx=5)
        self.angle_var_entry.grid(row=1, column=1, sticky="w", padx=5)
        
        # Entree pour la vitesse lors d'une rotation
        self.v_ang_var_label = tk.Label(self.turn_frame, text="Vitesse : ")
        self.v_ang_var_entry = tk.Entry(self.turn_frame, textvariable=self.v_ang_var)
        self.v_ang_var_label.grid(row=2, column=0, sticky="e", padx=5)
        self.v_ang_var_entry.grid(row=2, column=1, sticky="w", padx=5)

        # Creation du boutton Tourner 
        self.turn_button = tk.Button(self.turn_frame, text = "Tourner", command=self.turn_button_clicked)
        self.turn_button.grid(row = 3, column=1, pady = 5)
        
        # Creation du button Tracer Carre
        self.tracer_carre = tk.Button(self.root, text = "Tracer carre", command=self.tracer_carre_button_clicked)
        self.tracer_carre.grid(row=4, column = 0,sticky = "wsn", padx=5, pady=8)

        # Creation du boutton Go
        self.go_button = tk.Button(self.root, text = "Go", command=self.go_button_clicked)
        self.go_button.grid(row = 5, column = 0, sticky = "wsn", padx=5, pady=8)

        # Creation du boutton Go avec un capteur de distance 
        self.go_cap_button = tk.Button(self.root, text = "Go avec Capteur", command=self.go_cap_button_clicked)
        self.go_cap_button.grid(row = 6, column = 0, sticky = "wsn", padx=5, pady=8)

        # Creation du boutton Test osbtacle avec un capteur de distance 
        self.test_collision_button = tk.Button(self.root, text = "Test de collision avec diff angle", command=self.test_collision_button_clicked)
        self.test_collision_button.grid(row = 7, column = 0, sticky = "wsn", padx=5, pady=8)

        #Creation du button Reset

        self.canvas = tk.Canvas(self.root, width=self.arene.maxX, height=self.arene.maxY, bg=self.arene.color)
        self.canvas.grid(row=0, column=1, rowspan=100, padx=10, pady=5,sticky="nsew")
        
        # Définir l'étirement des colonnes et des lignes
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
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
        if self.controller is not None :
            print("reception\n")
            strat = Go(self.controller.robot, self.distance_var.get(), -self.v_ang_d_var.get(), self.v_ang_g_var.get(), self.controller.dt)
            self.controller.add_strat(strat)

    def go_cap_button_clicked(self):
        """ Handle go button click
        """
        if self.controller is not None :
            print("reception\n")
            strat = Go_cap(self.controller.robot, self.distance_var.get(), -self.v_ang_d_var.get(), self.v_ang_g_var.get(), self.controller.dt)
            self.controller.add_strat(strat)

    def turn_button_clicked(self):
        """ Handle turn button click
        """
        if self.controller is not None :
            print("reception\n")
            strat = Tourner_deg(self.controller.robot, self.angle_var.get(), self.v_ang_var.get(), self.controller.dt)
            self.controller.add_strat(strat)
    
    def tracer_carre_button_clicked(self):
        """ Handle tracer_carre button click
        """
        if self.controller is not None :
            print("reception\n")
            strat = Tracer_carre(self.controller.robot,self.distance_var.get(), self.v_ang_var.get(), self.controller.dt)
            self.controller.add_strat(strat)

    def test_collision_button_clicked(self):
        """ Handle tracer_carre button click
        """
        if self.controller is not None :
            print("reception\n")
            strat = Test_collision(self.controller.robot, self.controller.robot.posX, self.controller.robot.posY, self.distance_var.get(), self.v_ang_var.get(), self.controller.dt)
            self.controller.add_strat(strat)


    def draw_obj(self, Objet: Any) -> int:
        """Dessine un objet sur le canevas de l'Affichage. 


        :param Objet: Objet à dessiner.
        :returns: Identifiant unique de l'objet sur le canevas.
        """
        poly_coords = Objet.getCoins()

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
    
    def update_donnee_robot(self):
        """ Mettre à jour l'affichage des info du robot 
        """
        self.pos_label.config(text=f"Position: ({self.arene.robot.posX:.2f}, {self.arene.robot.posY:.2f})")
        self.roueD_label.config(text=f"Roue droite : {-self.arene.robot.roue_droite.vitesse_angulaire: .2f} rad/s")
        self.roueG_label.config(text=f"Roue gauche : {self.arene.robot.roue_gauche.vitesse_angulaire: .2f} rad/s")
    
    

    def update(self):
        """Mettre à jour le modele
        """
        self.update_donnee_robot()
        if self.arene.robot.rect_id and  self.arene.robot.arrow_id: 
            self.delete_draw(self.arene.robot.rect_id, self.arene.robot.arrow_id)
        self.draw_parcours(self.arene.robot)
        self.arene.robot.rect_id, self.arene.robot.arrow_id = self.draw_obj(self.arene.robot)
        self.draw_obj(self.arene.liste_Obstacles[0])
        
        self.root.update()
