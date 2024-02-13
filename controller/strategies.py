from modele.robot import * 

class Go(): 
    def __init__(self, robot: Robot, distance : int, v_ang_d, v_ang_g, dt) -> None:
        """/!!\\ robot ne comprends pas distance negative
        
        :param robot: Le robot qui va faire le deplacement 
        :param distance: La distance que le robot doit parcourir (float) 
        :param v_ang_d: La vitesse angulaire de la roue droite du robot en rad/s 
        :param v_ang_g: La vitesse angulaire de la roue gauche du robot en rad/s 
        :param dt: Le fps
        """
        self.robot = robot
        self.distance = distance

        # Modifier les vitesses angulaire les roues
        self.robot.roue_droite.set_vitesse_angulaire(v_ang_d)  # Vitesse angulaire droite
        self.robot.roue_gauche.set_vitesse_angulaire(v_ang_g)  # Vitesse angulaire gauche

        self.v_ang_d, self.v_ang_g = v_ang_d, v_ang_g

        #compteur de distance deja parcouru
        self.parcouru = 0

        #Coordonnee de vecteur de deplacement 
        self.dOM_x = robot.vectDir.x*robot.vitesse()*dt #/robot.grille.echelle 
        self.dOM_y = robot.vectDir.y*robot.vitesse()*dt #/robot.grille.echelle 

        self.dOM = Vecteur(self.dOM_x, self.dOM_y)

        self.dt = dt
        print("x, y", robot.vectDir.x, robot.vectDir.y)
        print(self.distance, self.v_ang_d, self.v_ang_g, self.dOM_x, self.dOM_y)

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
            self.dOM_theta = -self.robot.roue_droite.rayon*(self.v_ang_g+self.v_ang_d)/self.robot.length * self.dt
            self.dOM_x = self.robot.vectDir.x*self.robot.vitesse()*self.dt #/robot.grille.echelle 
            self.dOM_y = self.robot.vectDir.y*self.robot.vitesse()*self.dt #/robot.grille.echelle 

            self.dOM = Vecteur(self.dOM_x, self.dOM_y)

            print(self.dOM_theta)
        self.robot.move_dOM(self.dOM_x, self.dOM_y, self.dOM_theta)


class Tourner_deg(): 
    def __init__(self, robot: Robot,  angle : int, v_ang, dt) -> None:
        """"
        :param robot: Le controleur qui donne l'ordre 
        :param angle: L'angle que le robot doit parcourir (float) 
        :param v_ang: La vitesse angulaire de la roue droite ou gauche du robot en rad/s 
        :param dt: Le fps
        """
        self.angle = angle
        self.robot = robot

        # Modifier les vitesses angulaire les roues
        if angle > 0:
            self.robot.roue_droite.set_vitesse_angulaire(v_ang)  # Vitesse angulaire droite
            self.robot.roue_gauche.set_vitesse_angulaire(0)  # Vitesse angulaire gauche
            self.v_ang_d, self.v_ang_g = v_ang, 0
        else:
            self.robot.roue_droite.set_vitesse_angulaire(0)  # Vitesse angulaire droite
            self.robot.roue_gauche.set_vitesse_angulaire(v_ang) 
            self.v_ang_d, self.v_ang_g = 0, v_ang

        #compteur d'angle deja parcouru
        self.parcouru = 0

        #Coordonnee de vecteur de deplacement 
        self.dOM_x = self.robot.vectDir.x*robot.vitesse()*dt #/robot.grille.echelle 
        self.dOM_y = self.robot.vectDir.y*robot.vitesse()*dt #/robot.grille.echelle 

        self.dOM = Vecteur(self.dOM_x, self.dOM_y)

        self.dt = dt
        print("x, y", robot.vectDir.x, robot.vectDir.y)
        print(self.angle, self.v_ang_d, self.v_ang_g, self.dOM_x, self.dOM_y)

    def stop(self):
        """ Savoir le parcours est fini ou non

        :return : Retourne vrai si on fini de parcourir la distance  
        """
        return self.parcouru > self.angle

    def step(self):
        """ Faire un deplacement de dOM 
        """
        #Incrémenter la distance parcourru
        self.parcouru += self.dOM_theta
        if self.stop(): return
        
        self.dOM_theta = 0
        #Bouger le robot d'un dOM
        if -self.v_ang_d != self.v_ang_g: #si veut tourner 
            self.dOM_theta = -self.robot.roue_droite.rayon*(self.v_ang_g+self.v_ang_d)/self.robot.length * self.dt
            self.dOM_x = self.robot.vectDir.x*self.robot.vitesse()*self.dt #/robot.grille.echelle 
            self.dOM_y = self.robot.vectDir.y*self.robot.vitesse()*self.dt #/robot.grille.echelle 

            self.dOM = Vecteur(self.dOM_x, self.dOM_y)

            print(self.dOM_theta)
        self.robot.move_dOM(self.dOM_x, self.dOM_y, self.dOM_theta)

class Tracer_carre():
    def __init__(self, robot : Robot, distance : int, v_ang : float):
        """Trace un carré
        :param robot: Le robot qui reçoit l'ordre
        :param distance: La distance que le robot parcours, dans notre cas longueur du carré
        :param vang: La vitesse angulaire des roues du robot
        """