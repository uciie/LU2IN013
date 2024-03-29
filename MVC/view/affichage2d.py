import logging
import threading
import time
import tkinter as tk
from threading import Thread
from typing import Any

from ..controller.ai import Go, StrategieSequentielle, TournerDeg
from ..controller.controleur import Controleur
from ..modele.simulation import Simulation


# , Go_cap, Tourner_deg, Test_collision


class Affichage2D(Thread):
    """Classe view qui permet d'afficher l'interface graphique"""
    def __init__(self, simu: Simulation, dt: float, lock: threading.RLock):
        """Initialise un Affichage2D graphique.

        :param simu : L'arène qui sera affichée
        """
        super(Affichage2D, self).__init__()

        # Configure logging
        logging.basicConfig(level=logging.DEBUG, filename='ai.log', filemode='w',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Désactiver les messages de journalisation pour le module spécifié
        # logging.getLogger('MVC.view.affichage').setLevel(logging.WARNING)

        self.logger = logging.getLogger(__name__)

        self._running = False
        self._simu = simu
        self.dt = dt
        self.lock = lock

        self.last_pos_y = self._simu.robot.last_pos_y
        self.last_pos_x = self._simu.robot.last_pos_x

        # set the controller
        self._controller = None
        self.root = None

        # Les valeurs initiales des variables
        self.initial_v_ang_d = 50
        self.initial_v_ang_g = 50
        self.initial_v_ang = 50
        self.initial_angle = 90
        self.initial_distance = 50
        self.initial_position = (self._simu.robot.pos_x, self._simu.robot.pos_y)
        self.liste_id_draw = []
        self.initial_vectDir = self._simu.robot.vectDir

        # Les variables
        self.v_ang_d_var = None
        self.v_ang_g_var = None
        self.v_ang_var = None
        self.angle_var = None
        self.distance_var = None
        self.activer_trace_var = None

        self.robot_frame = None
        self.pos_label = None
        self.roueD_label = None
        self.roueG_label = None
        self.vectDir_label = None
        self.command_frame = None

        # Vitesses engulaires des roues
        self.v_ang_d_label = None
        self.v_ang_d_var_entry = None
        self.v_ang_g_label = None
        self.v_ang_g_var_entry = None

        # Distance
        self.distance_label = None
        self.distance_var_entry = None

        self.turn_frame = None
        self.angle_var_label = None
        self.angle_var_entry = None
        self.v_ang_var_label = None
        self.v_ang_var_entry = None
        self.message_label = None

        # Boutons
        self.turn_button = None
        self.go_button = None
        self.go_cap_button = None
        self.tracer_carre_button = None
        self.test_collision_button = None
        self.go_cap_max_button = None
        self.reset_button = None
        self.activer_trace_button = None

        self.canvas = None

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
        """ Remettre à zero l'interface graphique
        """
        # Efface les stratégies
        self._controller.strat = None
        self._simu.robot.roue_droite.vitesse_angulaire = 0
        self._simu.robot.roue_gauche.vitesse_angulaire = 0
        self._simu.robot.vectDir = self.initial_vectDir
        # Remettre le robot a la position initial
        self._simu.robot.pos_x, self._simu.robot.pos_y = self.initial_position
        self._simu.robot.last_pos_x, self._simu.robot.last_pos_y = self.initial_position
        # Suppression des parcours
        self.delete_parcours(self.liste_id_draw)
        self.canvas.delete("all")

    def check_value(self, val: float, var_entry: tk.Entry, nom_var: str):
        """ Verifie si les valeurs saisies sont valides selon la commande demandée
        :param val: La valeur
        :param var_entry: Le champ d'entrée
        :param nom_var: Le nom de la variable
        :return bool: True si la valeur est valide, False sinon
        """
        if val < 0.:
            error = f'Robot comprend pas ' + nom_var + ' négative'
            self.show_error(var_entry, error)
            raise ValueError(error)
        return True

    def go_button_clicked(self):
        """ Handle go button click
        """
        if self._controller is not None:
            if self.check_value(self.distance_var.get(), self.distance_var_entry, 'distance'):
                strat = Go(self._controller.adaptateur, self.distance_var.get(), self.v_ang_d_var.get(),
                           self.v_ang_g_var.get(), self.activer_trace_var.get())
                self._controller.add_strat(strat)

    def go_cap_button_clicked(self):
        """ Handle go button click
        """
        pass

    def turn_button_clicked(self):
        """ Handle turn button click
        """
        if self._controller is not None:
            strat = TournerDeg(self._controller.adaptateur, self.angle_var.get(), self.v_ang_var.get(),
                               self.activer_trace_var.get())
            self._controller.add_strat(strat)

    def tracer_carre_button_clicked(self):
        """ Handle tracer_carre button click
        """
        if self._controller is not None:
            steps = [
                Go(self._controller.adaptateur, self.distance_var.get(), self.v_ang_var.get(), self.v_ang_var.get(),
                   self.activer_trace_var.get()),
                TournerDeg(self._controller.adaptateur, 90, self.v_ang_var.get(), self.activer_trace_var.get()),
                Go(self._controller.adaptateur, self.distance_var.get(), self.v_ang_var.get(), self.v_ang_var.get(),
                   self.activer_trace_var.get()),
                TournerDeg(self._controller.adaptateur, 90, self.v_ang_var.get(), self.activer_trace_var.get()),
                Go(self._controller.adaptateur, self.distance_var.get(), self.v_ang_var.get(), self.v_ang_var.get(),
                   self.activer_trace_var.get()),
                TournerDeg(self._controller.adaptateur, 90, self.v_ang_var.get(), self.activer_trace_var.get()),
                Go(self._controller.adaptateur, self.distance_var.get(), self.v_ang_var.get(), self.v_ang_var.get(),
                   self.activer_trace_var.get()),
                TournerDeg(self._controller.adaptateur, 90, self.v_ang_var.get(), self.activer_trace_var.get())]
            strat = StrategieSequentielle(self._controller.adaptateur, steps)
            self._controller.add_strat(strat)

    def test_collision_button_clicked(self):
        """ Handle tracer_carre button click
        """
        pass

    def go_cap_max_button_clicked(self):
        """ Handle go_cap_max button click
        """
        pass

    @staticmethod
    def reset_entry_color(var_entry: tk.Entry):
        """ Réinitialise la couleur du champ d'entrée à sa valeur par défaut

        :param var_entry: Le champ d'entrée à réinitialiser
        """
        var_entry['foreground'] = 'black'

    def show_error(self, var_entry: tk.Entry, message: str):
        """ Affiche les erreurs sur l'interface graphique

        :param var_entry: La valeur de saisie
        :param message: Le message d'erreur
        :return void:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)
        var_entry['foreground'] = 'red'
        var_entry.after(3000, lambda: self.reset_entry_color(var_entry))

    def hide_message(self):
        """ Hide the message
        """
        self.message_label['text'] = ''

    def draw_obj(self, objet: Any) -> 'int | tuple[int, int]':
        """Dessine un objet sur le canevas de l'Affichage2D.

        :param objet: objet à dessiner.
        :returns: Identifiant unique de l'objet sur le canevas.
        """
        poly_coords = objet.coins

        poly_id = self.canvas.create_polygon(poly_coords, fill=objet.color)

        if hasattr(objet, 'vectDir'):
            arrow_id = self.canvas.create_line(
                objet.pos_x, objet.pos_y,
                objet.pos_x + objet.vectDir.x * objet.length, objet.pos_y + objet.vectDir.y * objet.length,
                arrow=tk.LAST)

            return poly_id, arrow_id
        else:
            return poly_id

    def draw_parcours(self, objet: Any):
        """ Trace le parcours de l'objet

        :param objet: objet
        :returns: Identifiant unique de l'objet sur le canevas.
        """
        line_id = self.canvas.create_line(self.last_pos_x, self.last_pos_y, objet.pos_x, objet.pos_y, fill='blue',
                                          width=3)
        self.last_pos_x = objet.pos_x
        self.last_pos_y = objet.pos_y
        self.liste_id_draw.append(line_id)

    def delete_parcours(self, parcours: list[int]):
        """ Supprime le parcours
        :param parcours: liste des parcours
        """
        for pas in parcours:
            self.delete_draw(pas)

    def delete_draw(self, *obj_ids: int):
        """Supprime un ou plusieurs dessins de l'Affichage2D.

        :param obj_ids: Identifiants des objets à supprimer du canevas.
        """
        for obj_id in obj_ids:
            self.canvas.delete(obj_id)

    def on_closing(self):
        """ Lors de la fermetura de la fenetre graphique """
        self._running = False
        self._simu.stop()
        self._controller._running = False
        self.root.quit()
        exit()

    def update_donnee_robot(self):
        """ Mettre à jour l'affichage des infos du robot
        """
        self.pos_label.config(text=f"Position: ({self._simu.robot.pos_x:.2f}, {self._simu.robot.pos_y:.2f})")
        self.roueD_label.config(text=f"Roue droite : {self._simu.robot.roue_droite.vitesse_angulaire: .2f} rad/s")
        self.roueG_label.config(text=f"Roue gauche : {self._simu.robot.roue_gauche.vitesse_angulaire: .2f} rad/s")
        self.vectDir_label.config(
            text=f"Vecteur directeur : ({self._simu.robot.vectDir.x:.2f}, {self._simu.robot.vectDir.y:.2f}) ")

    def update(self):
        """Mettre à jour le modele
        """

        self.update_donnee_robot()
        with self.lock:
            if self._simu.robot.rect_id and self._simu.robot.arrow_id:
                self.delete_draw(self._simu.robot.arrow_id, self._simu.robot.rect_id)  # effacer le robot
                # Effacer les obstacles
                for obstacle in self._simu.arene.liste_Obstacles:
                    self.delete_draw(obstacle)

            if self._simu.robot.tracer_parcours:
                self.draw_parcours(self._simu.robot)
            else:
                self.last_pos_x = self._simu.robot.pos_x
                self.last_pos_y = self._simu.robot.pos_y
            self._simu.robot.rect_id, self._simu.robot.arrow_id = self.draw_obj(self._simu.robot)
            # Dessiner les obstacles
            for obstacle in self._simu.arene.liste_Obstacles:
                self.draw_obj(obstacle)

            self.root.update()

    def run(self):
        """Demarrage de l'interface graphique"""
        self.root = tk.Tk()
        self.root.title(self._simu.name)

        # Créer des variables Tkinter pour la vitesse et la distance
        self.v_ang_d_var = tk.DoubleVar(value=self.initial_v_ang_d)
        self.v_ang_g_var = tk.DoubleVar(value=self.initial_v_ang_g)
        self.v_ang_var = tk.DoubleVar(value=self.initial_v_ang)
        self.angle_var = tk.DoubleVar(value=self.initial_angle)
        self.distance_var = tk.DoubleVar(value=self.initial_distance)
        self.activer_trace_var = tk.BooleanVar(value=True)  # bouton activation du trace

        # Creation du cadre pour les données du robot
        self.robot_frame = tk.LabelFrame(self.root, text=" Données du robot ")
        self.robot_frame.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        # Données du robot en temps réel
        self.pos_label = tk.Label(self.robot_frame,
                                  text=f"Position: ({self._simu.robot.pos_x:.2f}, {self._simu.robot.pos_y:.2f})")
        self.pos_label.grid(row=1, column=0, sticky="w", padx=5)
        self.roueD_label = tk.Label(self.robot_frame,
                                    text=f"Roue droite : {self._simu.robot.roue_droite.vitesse_angulaire} rad/s")
        self.roueD_label.grid(row=2, column=0, sticky="w", padx=5)
        self.roueG_label = tk.Label(self.robot_frame,
                                    text=f"Roue gauche : {self._simu.robot.roue_gauche.vitesse_angulaire} rad/s")
        self.roueG_label.grid(row=3, column=0, sticky="w", padx=5)
        self.vectDir_label = tk.Label(self.robot_frame,
                                      text=f"Vecteur directeur : ({self._simu.robot.vectDir.x:.2f}, {self._simu.robot.vectDir.y:.2f})")
        self.vectDir_label.grid(row=4, column=0, sticky="w", padx=5)

        # Create the activer_trace
        self.activer_trace_button = tk.Checkbutton(self.root, text="Activer Tracage", variable=self.activer_trace_var)
        self.activer_trace_button.grid(row=1, column=0, sticky="w", padx=5, pady=8)

        # Creation du cadre pour la commande basic
        self.command_frame = tk.LabelFrame(self.root, text=" Commande Basic ")
        self.command_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

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
        self.distance_label = tk.Label(self.command_frame, text="Distance : ")
        self.distance_var_entry = tk.Entry(self.command_frame, textvariable=self.distance_var)
        self.distance_label.grid(row=3, column=0, sticky="e", pady=5)
        self.distance_var_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Cadre pour la commande pour tourner
        self.turn_frame = tk.LabelFrame(self.root, text=" Commande pour Tourner ")
        self.turn_frame.grid(row=4, column=0, padx=5, pady=5, sticky="new")

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
        self.turn_button = tk.Button(self.turn_frame, text="Tourner", command=self.turn_button_clicked)
        self.turn_button.grid(row=3, column=1, pady=5)

        # Creation du label message erreur
        self.message_label = tk.Label(self.root, text='', foreground='red')
        self.message_label.grid(row=5, column=0, sticky="w", padx=5)

        # Creation du button Tracer Carre
        self.tracer_carre_button = tk.Button(self.root, text="Tracer carre", command=self.tracer_carre_button_clicked)
        self.tracer_carre_button.grid(row=6, column=0, sticky="wsn", padx=5, pady=8)

        # Creation du boutton Go
        self.go_button = tk.Button(self.root, text="Go", command=self.go_button_clicked)
        self.go_button.grid(row=7, column=0, sticky="wsn", padx=5, pady=8)

        # Creation du boutton Go avec un capteur de distance
        # self.go_cap_button = tk.Button(self.root, text="Go avec Capteur", command=self.go_cap_button_clicked)
        # self.go_cap_button.grid(row=8, column=0, sticky="wsn", padx=5, pady=8)

        # Creation du boutton Test osbtacle avec un capteur de distance
        # self.test_collision_button = tk.Button(self.root, text="Test de collision avec diff angle",
        #                                       command=self.test_collision_button_clicked)
        # self.test_collision_button.grid(row=9, column=0, sticky="wsn", padx=5, pady=8)

        # Creation du bouton Go cap max
        # self.go_cap_max_button = tk.Button(self.root, text="Go avec Capteur et Vmax",
        #                                   command=self.go_cap_max_button_clicked)
        # self.go_cap_max_button.grid(row=10, column=0, sticky="wsn", padx=5, pady=8)

        # Creation du button Reset
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_button_clicked)
        self.reset_button.grid(row=11, column=0, sticky="wsn", padx=5, pady=8)

        self.canvas = tk.Canvas(self.root, width=self._simu.arene.max_x, height=self._simu.arene.max_y,
                                bg=self._simu.arene.color)
        self.canvas.grid(row=0, column=1, rowspan=100, padx=10, pady=5)

        # Définir l'étirement des colonnes et des lignes
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self._running = True
        while self._running:
            self.update()
            time.sleep(self.dt)
