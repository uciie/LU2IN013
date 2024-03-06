import tkinter as tk
from typing import Any
from MVC.modele.arene import Arene
from MVC.controller.controleur import Controleur, Go, Go_cap, Tourner_deg, Test_collision

class Affichage():
    def __init__(self, arene:Arene, dt: float):
        """Initialise un Affichage graphique.

        :param arene : L'arène qui sera affichée
        """
        self.arene = arene
        self.dt = dt
        self.root = tk.Tk()
        self.root.title(arene.name)

        # Set the initial values for the variables
        self.initial_v_ang_d = 50
        self.initial_v_ang_g = 50
        self.initial_v_ang = 50
        self.initial_angle = 90
        self.initial_distance = 50
        self.initial_position = (self.arene.robot.posX, self.arene.robot.posY)
        self.liste_id_draw = []

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
        self.vectDir_label = tk.Label(self.robot_frame, text=f"Vecteur directeur : ({self.arene.robot.vectDir.x:.2f}, {self.arene.robot.vectDir.y:.2f})")
        self.vectDir_label.grid(row=4, column=0, sticky="w", padx=5)
        

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
        
        # Creation du label message erreur
        self.message_label = tk.Label(self.root, text='', foreground='red')
        self.message_label.grid(row=4, column=0, sticky = "w", padx=5)
        
        # Creation du button Tracer Carre
        self.tracer_carre = tk.Button(self.root, text = "Tracer carre", command=self.tracer_carre_button_clicked)
        self.tracer_carre.grid(row=5, column = 0,sticky = "wsn", padx=5, pady=8)

        # Creation du boutton Go
        self.go_button = tk.Button(self.root, text = "Go", command=self.go_button_clicked)
        self.go_button.grid(row = 6, column = 0, sticky = "wsn", padx=5, pady=8)

        # Creation du boutton Go avec un capteur de distance 
        self.go_cap_button = tk.Button(self.root, text = "Go avec Capteur", command=self.go_cap_button_clicked)
        self.go_cap_button.grid(row = 7, column = 0, sticky = "wsn", padx=5, pady=8)

        # Creation du boutton Test osbtacle avec un capteur de distance 
        self.test_collision_button = tk.Button(self.root, text = "Test de collision avec diff angle", command=self.test_collision_button_clicked)
        self.test_collision_button.grid(row = 8, column = 0, sticky = "wsn", padx=5, pady=8)

        # Creation du bouton Go cap max
        self.go_cap_max_button = tk.Button(self.root, text= "Go avec Capteur et Vmax", command=self.go_cap_max_button_clicked)
        self.go_cap_max_button.grid(row = 9, column = 0, sticky = "wsn", padx=5, pady=8)

        #Creation du button Reset
        self.reset_button = tk.Button(self.root, text = "Reset", command=self.reset_button_clicked)
        self.reset_button.grid(row = 10, column = 0, sticky = "wsn", padx=5, pady=8)

        self.canvas = tk.Canvas(self.root, width=self.arene.maxX, height=self.arene.maxY, bg=self.arene.color)
        self.canvas.grid(row=0, column=1, rowspan=100, padx=10, pady=5,sticky="nsew")
        
        # Définir l'étirement des colonnes et des lignes
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        # set the controller
        self._controller = None

    @property
    def controller(self):
        """Renvoie le contrôleur associé."""
        return self._controller

    @controller.setter
    def controller(self, controller: Controleur):
        """Définit le contrôleur associé.
        :param controller : Le contrôleur associé
        """
        self._controller = controller

    def reset_button_clicked(self):
        """ remettre à zero l'interface graphique 
        """
        # Efface les stratégies
        self._controller.liste_strat = []
        self._controller.cur = -1
        # Remettre le robot a la position initial
        self.arene.robot.posX,self.arene.robot.posY = self.initial_position
        self.arene.robot.lastPosX,self.arene.robot.lastPosY = self.initial_position
        # Suppresion des parcours
        self.delete_draw(self.liste_id_draw)
        self.canvas.delete("all")
        
    def checkValue(self, val: float, var_entry: tk.Entry, nom_var: str):
        """ Verifie si les valeurs saisies sont valides selon la commande demandée
        :param val: La valeur
        :param var_entry: Le champ d'entrée
        :nom_var: Le nom de la variable
        :return bool:
        """
        if val < 0.:
            error = f'Robot comprend pas ' + nom_var + ' négative'
            self.show_error(var_entry, error)
            raise ValueError(error)
        return True

    def go_button_clicked(self):
        """ Handle go button click
        """
        if self.controller is not None :
            print("reception\n")
            if self.checkValue(self.distance_var.get(), self.distance_var_entry, 'distance'):
                strat = Go(self.controller.robot, self.distance_var.get(), -self.v_ang_d_var.get(), self.v_ang_g_var.get(), self.controller.dt)
                self.controller.add_strat(strat)

    def go_cap_button_clicked(self):
        """ Handle go button click
        """
        if self.controller is not None :
            print("reception\n")
            if self.checkValue(self.distance_var.get(), self.distance_var_entry,'distance'):
                strat = Go_cap(self.controller.robot, self.distance_var.get(), -self.v_ang_d_var.get(), self.v_ang_g_var.get(), self.controller.dt)
                self.controller.add_strat(strat)

    def turn_button_clicked(self):
        """ Handle turn button click
        """
        if self.controller is not None :
            print("reception\n")
            if self.checkValue(self.v_ang_var.get(), self.v_ang_var_entry, 'vitesse'):
                strat = Tourner_deg(self.controller.robot, self.angle_var.get(), self.v_ang_var.get(), self.controller.dt)
                self.controller.add_strat(strat)
    
    def tracer_carre_button_clicked(self):
        """ Handle tracer_carre button click
        """
        if self.controller is not None :
            print("reception\n")
            self.controller.tracer_carre(self.distance_var.get(), self.v_ang_var.get(), self.controller.dt)

    def test_collision_button_clicked(self):
        """ Handle tracer_carre button click
        """
        if self.controller is not None :
            print("reception\n")
            posX, posY = self.arene.liste_Obstacles[0].posX, self.arene.liste_Obstacles[0].posY
            strat = Test_collision(self.controller.robot, posX, posY, self.distance_var.get(), self.v_ang_var.get(), self.controller.dt)
            self.controller.add_strat(strat)

    def go_cap_max_button_clicked(self):
        """ Handle go_cap_max button click
        """
        if self.controller is not None :
            print("reception\n")
            if self.checkValue(self.distance_var.get(), self.distance_var_entry,'distance'):
                self.controller.go_cap_vmax(self.distance_var.get(), self.controller.dt)

    def draw_obj(self, Objet: Any) -> int:
        """Dessine un objet sur le canevas de l'Affichage. 


        :param Objet: Objet à dessiner.
        :returns: Identifiant unique de l'objet sur le canevas.
        """
        poly_coords = Objet.coins

        poly_id = self.canvas.create_polygon(poly_coords, fill=Objet.color)

        if hasattr(Objet, 'vectDir'):
            arrow_id = self.canvas.create_line(
                Objet.posX, Objet.posY,
                Objet.posX + Objet.vectDir.x * Objet.length, Objet.posY + Objet.vectDir.y * Objet.length,
                arrow=tk.LAST)

            return poly_id, arrow_id
        else:
            return poly_id

    def draw_parcours(self, Objet: Any):
        """ Trace le parcours de l'objet

        :param Objet: Objet 
        :returns: Identifiant unique de l'objet sur le canevas.
        """
        line_id = self.canvas.create_line(Objet.lastPosX, Objet.lastPosY, Objet.posX, Objet.posY, fill='blue', width=3)
        self.liste_id_draw.append(line_id)
    
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
        self.vectDir_label.config(text=f"Vecteur directeur : ({self.arene.robot.vectDir.x:.2f}, {self.arene.robot.vectDir.y:.2f}) ")
    
    def update(self):
        """Mettre à jour le modele
        """
        self.update_donnee_robot()
        if self.arene.robot.rect_id and self.arene.robot.arrow_id: 
            self.delete_draw(self.arene.robot.rect_id, self.arene.robot.arrow_id)
            self.delete_draw(self.arene.liste_Obstacles[0])
        self.draw_parcours(self.arene.robot)
        self.arene.robot.rect_id, self.arene.robot.arrow_id = self.draw_obj(self.arene.robot)
        self.draw_obj(self.arene.liste_Obstacles[0])
        
        self.root.after(int(1/self.dt))
        self.root.update()
        

    def reset_entry_color(self, var_entry: tk.Entry):
        """ Réinitialise la couleur du champ d'entrée à sa valeur par défaut
            
        :param var_entry: Le champ d'entrée à réinitialiser
        :return:s
        """
        var_entry['foreground'] = 'black'

    def show_error(self, var_entry: tk.Entry, message: str):
        """ Affiche les erreurs sur l'interface graphique 
        
        :param var_entry: La valeur de saisie
        :param message: Le message d'erreur
        :return void:
        """
        print("show")
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)
        var_entry['foreground'] = 'red'
        var_entry.after(3000, lambda: self.reset_entry_color(var_entry))

    def hide_message(self):
        """ Hide the message
        :return:
        """
        self.message_label['text'] = ''
        
