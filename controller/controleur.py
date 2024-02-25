from modele.robot import Robot, Vecteur
from view.affichage import Affichage
import math

class Strategie():
    def __init__(self):
        pass

    def calcul_dOM(self, robot: Robot, dt): 
        """ Calcul les dOM pour lezs utiliser lors de appel de go_dOM

        :param robot: Le robot qui va faire le deplacement 
        :param v_ang_d: La vitesse angulaire de la roue droite du robot en rad/s 
        :param v_ang_g: La vitesse angulaire de la roue gauche du robot en rad/s 
        :param dt: Le fps
        """
        dOM_theta = -robot.roue_droite.rayon*(robot.roue_droite.vitesse_angulaire+robot.roue_gauche.vitesse_angulaire)/robot.length * dt
        dOM_x = robot.vectDir.x*robot.vitesse()*dt #/robot.grille.echelle 
        dOM_y = robot.vectDir.y*robot.vitesse()*dt #/robot.grille.echelle 

        dOM = Vecteur(dOM_x, dOM_y)

        return dOM_theta, dOM_x, dOM_y, dOM

class Go(Strategie): 
    def __init__(self, robot: Robot, distance : int, v_ang_d, v_ang_g, dt) -> None:
        """/!!\\ robot ne comprends pas distance negative
        
        :param robot: Le robot qui va faire le deplacement 
        :param distance: La distance que le robot doit parcourir (float) 
        :param v_ang_d: La vitesse angulaire de la roue droite du robot en rad/s 
        :param v_ang_g: La vitesse angulaire de la roue gauche du robot en rad/s 
        :param dt: Le fps
        """
        super().__init__()  # Appel du constructeur de la classe parente 
        self.robot = robot
        self.distance = distance

        # Modifier les vitesses angulaire les roues
        self.robot.roue_droite.set_vitesse_angulaire(v_ang_d)  # Vitesse angulaire droite
        self.robot.roue_gauche.set_vitesse_angulaire(v_ang_g)  # Vitesse angulaire gauche

        self.v_ang_d, self.v_ang_g = v_ang_d, v_ang_g

        #compteur de distance deja parcouru
        self.parcouru = 0

        #le fps
        self.dt = dt

        #Calcul des dOM
        self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = super.calcul_dOM(self.robot, self.dt)

        print("x, y", robot.vectDir.x, robot.vectDir.y)
    
    def actualise(self, robot : Robot, dt):
        self.robot = robot
        self.dOM_x = robot.vectDir.x*robot.vitesse()*dt #/robot.grille.echelle 
        self.dOM_y = robot.vectDir.y*robot.vitesse()*dt #/robot.grille.echelle 
        self.dOM = Vecteur(self.dOM_x, self.dOM_y)

    def start(self):
        """ Commencer la strategie
        """
        #compteur de distance deja parcouru
        self.parcouru = 0      

    def stop(self):
        """ Savoir le parcour est fini ou non

        :return : Retourne vrai si on fini de parcourir la distance  
        """
        return self.parcouru > self.distance

    def step(self):
        """ Faire un deplacement de dOM 
        """
        #Incrémenter la distance parcourru
        self.parcouru += self.dOM.norme
        if self.stop(): return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            #Calcul des dOM
            self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = super.calcul_dOM(self.robot, self.dt)
            print(self.dOM_theta)

        self.robot.move_dOM(self.dOM_x, self.dOM_y, self.dOM_theta)


class Tourner_deg(Strategie): 
    def __init__(self, robot: Robot,  angle : int, v_ang, dt) -> None:
        """"
        :param robot: Le controleur qui donne l'ordre 
        :param angle: L'angle que le robot doit parcourir (float) 
        :param v_ang: La vitesse angulaire de la roue droite ou gauche du robot en rad/s 
        :param dt: Le fps
        """
        super().__init__()  # Appel du constructeur de la classe parente 
        self.angle = angle
        self.robot = robot

        # Modifier les vitesses angulaire les roues
        if angle > 0:
            self.robot.roue_droite.set_vitesse_angulaire(-v_ang)  # Vitesse angulaire droite
            self.robot.roue_gauche.set_vitesse_angulaire(0)  # Vitesse angulaire gauche
            self.v_ang_d, self.v_ang_g = -v_ang, 0
        else:
            self.robot.roue_droite.set_vitesse_angulaire(0)  # Vitesse angulaire droite
            self.robot.roue_gauche.set_vitesse_angulaire(v_ang) 
            self.v_ang_d, self.v_ang_g = 0, v_ang

        #compteur de distance deja parcouru
        self.parcouru = 0

        self.dt = dt

        #Calcul des dOM
        self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = super.calcul_dOM(self.robot, self.dt)
        print("x, y", robot.vectDir.x, robot.vectDir.y)

    def start(self):
        """ Commencer la strategie
        """
        #compteur de distance deja parcouru
        self.parcouru = 0      

    def stop(self):
        """ Savoir le parcours est fini ou non

        :return : Retourne vrai si on fini de parcourir la distance  
        """
        if self.angle > 0:
            return self.parcouru > self.angle
        else:
            return self.parcouru < self.angle

    def actualise(self, robot : Robot, dt):
        return     
       
    def step(self):
        """ Faire un deplacement de dOM 
        """
        #Incrémenter la distance parcourru
        self.parcouru += (-self.robot.roue_droite.rayon*(self.robot.roue_droite.vitesse_angulaire+self.robot.roue_gauche.vitesse_angulaire)/self.robot.length * self.dt)*180/math.pi

        if self.stop(): return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = super.calcul_dOM(self.robot, self.dt)

        self.robot.move_dOM(self.dOM_x, self.dOM_y, self.dOM_theta)

class Tracer_carre(Strategie):
    def __init__(self, robot : Robot, distance : int, v_ang : float, dt):
        """Trace un carré
        :param robot: Le robot qui reçoit l'ordre
        :param distance: La distance que le robot parcours, dans notre cas longueur du carré
        :param vang: La vitesse angulaire des roues du robot
        """
        super().__init__()  # Appel du constructeur de la classe parente 
        #Longueur/Distance du carré
        self.distance = distance
        self.robot = robot
        self.dt =dt
        #Vitesse angulaire des roues pour tracer le carré
        self.v_ang = v_ang

        #Les étapes à faire
        self.etapes = [Go(self.robot, distance, -v_ang, v_ang, dt),Tourner_deg(self.robot, 90, v_ang, dt),
                    Go(self.robot, distance, -v_ang, v_ang, dt),Tourner_deg(self.robot, 90, v_ang, dt),
                    Go(self.robot, distance, -v_ang, v_ang, dt),Tourner_deg(self.robot, 90, v_ang, dt),
                    Go(self.robot, distance, -v_ang, v_ang, dt),Tourner_deg(self.robot, 90, v_ang, dt)]
        self.cur = -1

    def start(self):
        """ Commencer la strategie
        """
        self.cur = -1

    def step(self):
        """Fait avancer le traçage du carré
        """
        if self.stop(): return
        #Avance d'une étape
        if self.cur <0 or self.etapes[self.cur].stop():
            self.cur+=1
            self.etapes[self.cur].start()
            self.etapes[self.cur].actualise(self.robot, self.dt)
        self.etapes[self.cur].step()
    
    def stop(self):
        """Vérifie si toutes les étapes sont terminées
        """
        return self.cur == len(self.etapes)-1 and self.etapes[self.cur].stop()

class Controleur:
    def __init__(self, robot: Robot, listeStrat: list[Strategie], dt):
        """
        Initialise le contrôleur avec un robot, une vue et un intervalle de temps.

        :param robot: Le robot
        :param dt: Le fps
        """
        # Modèle
        self.robot = robot
        
        # Vues 
        self.view = None

        #Liste des Strategie 
        self.listeStrat = listeStrat
        #position de la commande à faire
        self.cur = -1

        self.dt = dt

    def set_view(self, view: Affichage):
        """ L'ajout du View dans le controller
        
        :param view: Le module View
        """
        if self.view : 
            self.reset_robot()
            self.view.root.destroy()  # Destroy the current window
        self.view = view
        self.view.set_controller(self)

    def reset_robot(self):
        """ Mettre robot au mileu du plan
        """
        self.robot.vectDir = Vecteur(0, -1)
        self.robot.posX, self.robot.posY = self.view.arene.maxX/2, self.view.arene.maxY /2

    def remove_strat(self):
        """ enlever la stratégie fini de la liste, ie le premier element de la liste
        """
        self.listeStrat.pop(0)

    def stop(self):
        """Vérifie si toutes les étapes sont terminées
        """
        return self.cur == len(self.listeStrat)-1 and self.listeStrat[self.cur].stop()
    
    def step(self):
        """Faire la commande suivante 
        """
        if self.stop(): return
        #Avance d'une étape
        if self.cur <0 or self.listeStrat[self.cur].stop():
            self.cur+=1
            self.listeStrat[self.cur].start()
            self.listeStrat[self.cur].actualise(self.robot, self.dt)
        self.listeStrat[self.cur].step()
