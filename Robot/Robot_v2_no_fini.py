# @autors equipe HELMS
#import Exceptions


class Robot:
  def __init__(self, name, posX, posY, dimLength, dimWidth,grille):
    """ str x double x double x Grille-> Robot
    Precondition: dimLength % 2 = 1 and dimWidth % 2 = 1
    Initialisation du robot 
    """
    # Nom du robot
    self.name = name 

    #Position du robot
    self.posX = posX
    self.posY = posY

    #Ancienne position du robot
    #Initilise l'ancienne position à la position actuelle
    self.lastPosX = posX 
    self.lastPosY = posY

    # Direction
    self.direction = "UP" #on suppose qu'au debut le robot est dirigé vers le haut 
    self.angle = 0 # angle en degre

    #Dimention du robot
    self.length = dimLength 
    self.width = dimWidth

    #Composant du robot
    #self.roue_r = Roue("right") #Roue droite du robot
    #self.roue_l = Roue("left") #Roue left du robot

    #Environnement du robot
    self.grille = grille
    self.grille.addRobot(self)

    self.vitesse = 0.

    ## A IGNORER POUR L'INSTANT###
    #self.batteries = batteries
    #self.camera = camera
    #self.capteurD = capteurD
    #self.accelerometre = accelerometre
  
  def getCurrPos(self):
    """-> Tuple(double, double)
    Renvoie la position actuelle du robot
    """
    return (self.posX,self.posY)
  
  def getLastPos(self):
    """-> Tuple(double, double)
    Renvoie la position actuelle du robot
    """
    return (self.lastPosX,self.lastPosY)
  
  def update(self, new_x, new_y):
    """ -> None
    Mettre à jour la grille et la position du robot
    """
    #mise à jour les positions
    self.lastPosX = self.posX
    self.lastPosY = self.posY

    self.posX = new_x
    self.posY = new_y

    #mise à jour de la grille
    self.grille.viderCase(self.lastPosX, self.lastPosY) 
    self.grille.setCase(self.posX,self.posY, "R")

  
  def move_one(self, direction, angle): 
    """ str x double -> None
    Bouge d'une case selon d'une direction
    """
    try : 
      new_x, new_y = self.posX, self.posY
      if direction == "UP" and self.grille.isEmptyCase(self.posX, self.posY - 1) :
        new_y -= 1
      elif direction == "DOWN" and self.grille.isEmptyCase(self.posX, self.posY + 1) :
        new_y += 1
      elif direction == "LEFT" and self.grille.isEmptyCase(self.posX - 1, self.posY) :
        new_x -= 1
      elif direction == "RIGHT" and self.grille.isEmptyCase(self.posX + 1, self.posY) :
        new_x += 1
      else : 
        print ("La saisie n'etait pas correcte")
        return 
    except IndexError as e:
      print("Mur touché") 
    #update 
    self.update(new_x, new_y)

  def go(self, direction, angle, distance):
    """ str x double x int -> None
    Precondition : distance >= 0
    Avancer d'une distance
    """
    i = 0
    
    #Tant qu'il n'y a pas d'obstacle à la case suivante et qu'on n'est pas arrivée à la nvlle position
    while i != distance:
      self.move_one(direction, angle) 
      self.grille.affiche()
      i += 1
      
  
  def goToPos(self, posX, posY):
    """
    Se deplacer à la position (x,y) 
    """
    
