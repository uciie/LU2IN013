
from grille import *
from robot import *
from vecteur import *

import pygame
import sys

pygame.init()

# Initialisation de la fenêtre
largeur, hauteur = 600, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Simulation de déplacement du robot")

# Couleurs
blanc = (255, 255, 255)
rouge = (255, 0, 0)


# Position initiale du robot
x_robot, y_robot = int(largeur / 3), int(hauteur / 3)

# Assurez-vous que la grille est correctement initialisée
grille = Grille(largeur, hauteur, 1)

# Créez un objet Robot avec la grille correcte
robot = Robot("r", x_robot, y_robot, x_robot, y_robot, grille, Vecteur(1, 1), fenetre, blanc, rouge )

vitesse = 1
distance = 50
angle = 90
occ1 = 0
# Boucle principale
while True :
    #permet de fermer la fenetre 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

    robot.vectDir = robot.vectDir.rotation(angle)

    # Appel correct de la méthode go2
    if occ1 == 0: 
      for i in range(4):
        #print(robot.vectDir.x,robot.vectDir.y)
        robot.go(90, distance, vitesse)
        #print(robot.vectDir.x,robot.vectDir.y)
      occ1 += 1

    # Effacer l'écran
    fenetre.fill(blanc)

    # Dessiner le robot
    pygame.draw.rect(fenetre, rouge, (robot.posX, robot.posY, robot.length, robot.width))

    # Mettre à jour l'affichage
    pygame.display.flip()