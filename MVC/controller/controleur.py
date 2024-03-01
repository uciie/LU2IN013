from MVC.modele.robot import Robot, Vecteur
from time import sleep
import math

def calcul_dOM(robot: Robot, dt): 
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

class Strategie():
    def __init__(self):
        pass
    
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
        
        self.v_ang_d, self.v_ang_g = v_ang_d, v_ang_g

        #compteur de distance deja parcouru
        self.parcouru = 0

        #le fps
        self.dt = dt
       #print("x, y", robot.vectDir.x, robot.vectDir.y)
    
    def actualise(self, robot : Robot, dt):
        self.robot = robot
        self.dOM_x = robot.vectDir.x*robot.vitesse()*dt #/robot.grille.echelle 
        self.dOM_y = robot.vectDir.y*robot.vitesse()*dt #/robot.grille.echelle 
        self.dOM = Vecteur(self.dOM_x, self.dOM_y)

    def start(self):
        """ Commencer la strategie
        """
        #compteur de distance deja parcouru
        # Modifier les vitesses angulaire les roues
        self.robot.roue_droite.set_vitesse_angulaire(self.v_ang_d)  # Vitesse angulaire droite
        self.robot.roue_gauche.set_vitesse_angulaire(self.v_ang_g)  # Vitesse angulaire gauche
        #Calcul des dOM
        self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)
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
        if self.stop(): 
            print("STOP")
            return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            #Calcul des dOM
            self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)
            #print(self.dOM_theta)

        self.robot.move_dOM(self.dOM_x, self.dOM_y, self.dOM_theta)

class Go_cap(Strategie): 
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
        
        self.v_ang_d, self.v_ang_g = v_ang_d, v_ang_g

        #compteur de distance deja parcouru
        self.parcouru = 0

        #le fps
        self.dt = dt
       #print("x, y", robot.vectDir.x, robot.vectDir.y)
    
    def actualise(self, robot : Robot, dt):
        self.robot = robot
        self.dOM_x = robot.vectDir.x*robot.vitesse()*dt #/robot.grille.echelle 
        self.dOM_y = robot.vectDir.y*robot.vitesse()*dt #/robot.grille.echelle 
        self.dOM = Vecteur(self.dOM_x, self.dOM_y)

    def start(self):
        """ Commencer la strategie
        """
        #compteur de distance deja parcouru
        # Modifier les vitesses angulaire les roues
        self.robot.roue_droite.set_vitesse_angulaire(self.v_ang_d)  # Vitesse angulaire droite
        self.robot.roue_gauche.set_vitesse_angulaire(self.v_ang_g)  # Vitesse angulaire gauche
        #Calcul des dOM
        self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)
        self.parcouru = 0  
        #Verification de detection d'un mur ou obstacle     
        self.danger = self.robot.arene.raytracing(self.robot) < 2 

    def stop(self):
        """ Savoir le parcour est fini ou non

        :return : Retourne vrai si on fini de parcourir la distance  
        """
        return self.parcouru > self.distance or self.danger

    def step(self):
        """ Faire un deplacement de dOM 
        """
        #Incrémenter la distance parcourru
        self.parcouru += self.dOM.norme
        #Verification de detection d'un mur ou obstacle 
        self.danger = self.robot.arene.raytracing(self.robot) < 2 

        if self.stop(): 
            print("STOP")
            return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            #Calcul des dOM
            self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)
            #print(self.dOM_theta)

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

        self.v_ang = v_ang #Vitesse angulaire 
        self.parcouru = 0 #compteur de distance deja parcouru
        self.angle = angle #angle à parcourir
        self.dt = dt

        #Calcul des dOM
        self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)
        #print("x, y", robot.vectDir.x, robot.vectDir.y)

    def start(self):
        """ Commencer la strategie
        """
        # Modifier les vitesses angulaire les roues
        if self.angle > 0:
            self.robot.roue_droite.set_vitesse_angulaire(-self.v_ang)  # Vitesse angulaire droite
            self.robot.roue_gauche.set_vitesse_angulaire(0)  # Vitesse angulaire gauche
            self.v_ang_d, self.v_ang_g = -self.v_ang, 0
        else:
            self.robot.roue_droite.set_vitesse_angulaire(0)  # Vitesse angulaire droite
            self.robot.roue_gauche.set_vitesse_angulaire(self.v_ang) 
            self.v_ang_d, self.v_ang_g = 0, self.v_ang

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

        if self.stop(): 
            print("STOP")
            return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            self.dOM_theta, self.dOM_x, self.dOM_y, self.dOM = calcul_dOM(self.robot, self.dt)

        self.robot.move_dOM(0, 0, self.dOM_theta)

class Tracer_carre(Strategie):
    def __init__(self, robot : Robot, distance : int, v_ang : float, dt):
        """Trace un carré
        :param robot: Le robot qui reçoit l'ordre
        :param distance: La distance que le robot parcours, dans notre cas longueur du carré
        :param vang: La vitesse angulaire des roues du robot
        :param dt: Le FPS
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
    def actualise(self, robot : Robot, dt):
        return   

    def start(self):
        """ Commencer la strategie
        """
        self.cur = -1

    def step(self):
        """Fait avancer le traçage du carré
        """
        if self.stop(): 
            print("STOP")
            return
        #Avance d'une étape
        if self.cur <0 or self.etapes[self.cur].stop():
            self.cur+=1
            self.etapes[self.cur].actualise(self.robot, self.dt)
            self.etapes[self.cur].start()
        self.etapes[self.cur].step()
    
    def stop(self):
        """Vérifie si toutes les étapes sont terminées
        """
        return self.cur == len(self.etapes)-1 and self.etapes[self.cur].stop()

class Test_collision(Strategie):
    def __init__(self, robot : Robot, posX, posY,  distance : int, v_ang : float, dt):
        """Trace un carré

        :param robot: Le robot qui reçoit l'ordre
        :param posX: position en x de depart du robot 
        :param posY: position en y de depart du robot 
        :param vang: La vitesse angulaire des roues du robot
        :param distance: La distance que le robot parcours, dans notre cas longueur du carré
        :param dt: Le FPS
        """
        super().__init__()  # Appel du constructeur de la classe parente 
        
        self.robot = robot
        self.dt =dt
        self.strat = Go_cap(self.robot, distance, -v_ang, v_ang, dt)

        #Les listes des positions
        self.list_pos = [(posX+distance, posY), (posX, posY-distance), (posX-distance, posY), (posX, posY+distance)]

        self.cur = -1

    def actualise(self, robot : Robot, dt):
        """
        """
        return

    def start(self):
        """ Commencer la strategie
        """
        self.robot.vectDir = Vecteur(0, -1)
        self.cur = -1

    def step(self):
        """Fait avancer le traçage du carré
        """
        if self.stop(): 
            print("STOP")
            return
        #Avance d'une étape
        if self.cur <0 or self.strat.stop():
            self.cur+=1
            self.robot.vectDir = self.robot.vectDir.rotation(90)
            self.robot.posX, self.robot.posY = self.list_pos[self.cur]
            self.strat.actualise(self.robot, self.dt)
            self.strat.start()

        self.strat.step()
    
    def stop(self):
        """Vérifie si toutes les étapes sont terminées
        """
        return self.cur == len(self.list_pos)-1 and self.strat.stop()
    
class Controleur:
    def __init__(self, robot: Robot, dt):
        """
        Initialise le contrôleur avec un robot, une vue et un intervalle de temps.

        :param robot: Le robot
        :param dt: Le fps
        """
        # Modèle
        self.robot = robot
        
        # Vues 
        self.view = None

        # liste strat
        self.liste_strat = []

        self.cur = -1
        # Le fps
        self.dt = dt

    def set_view(self, view):
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

    def add_strat(self, strat):
        """ Ajouter une strategie au conntroleur

        :param strat: Une strategie 
        """
        self.liste_strat.append(strat)

    def stop(self):
        """Vérifie si toutes les étapes sont terminées
        """
        if self.liste_strat == []: 
            return True
        return self.cur == len(self.liste_strat)-1 and self.liste_strat[self.cur].stop()
    
    def step(self):
        """Faire la commande suivante 
        """
        if self.stop(): 
            return
        #Faire la strtégie suivante 
        if self.cur <0 or self.liste_strat[self.cur].stop():
            self.cur+=1
            self.liste_strat[self.cur].actualise(self.robot, self.dt)
            self.liste_strat[self.cur].start()
        print(self.cur)
        self.liste_strat[self.cur].step()
