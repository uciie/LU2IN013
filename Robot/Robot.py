# @autors equipe HELMS

from exceptions import *
from vecteur import *
from math import atan2, degrees, cos, sin
import sys
import tkinter as tk


# Supposons que les robot sont en forme de rectangle/carre
# Supposons que la position du robot (x,y) correspond a l'extremite en haut à gauche

#FPS
dt = 1 / 30

class Robot:
  def __init__(self, name, posX, posY, dimLength, dimWidth, vectDirecteur, color ):
    """Initialisation du robot 
    :param name: nom du robot
    :param posX: coordonnee x du robot 
    :param posY: coordonnee y du robot
    :param dimLength: longueur de la piece en m
    :param dimWidth: largeur de la piece en m
    :param vecteurDirecteur: vecteur directeur du robot
    :param color: couleur du robot
    :returns: Retourne une instance de la classe Robot
    """
    # Nom du robot
    self.name = name 

    # Fenetre graphique 
    self.rect = None # le robot 
    self.arrow = None # vecteur directeur
    self.color = color # couleur du robot 

    #Dimention du robot sur la fenetre 
    self.length = dimLength #/self.grille.echelle
    self.width = dimWidth #/self.grille.echelle


    #Ancienne position du robot
    #Initilise l'ancienne position à la position actuelle
    self.lastPosX = posX 
    self.lastPosY = posY

    # Direction
    self.vectDir = vectDirecteur#on suppose qu'au debut le robot est dirigé vers le haut 
    self.angle = 0 # angle en degre
    
    # Vitesse
    self.vitesse = 5.0 # m/s

  def getCurrPos(self):
    """Renvoie la position actuelle du robot
    :reuturns: Renvoie les coordonnées du robot
    """
    return (self.posX,self.posY)
  
  def getLastPos(self):
    """Renvoie l'ancienne position du robot
    :returns: Renvoie l'avant dernière coordonnée du robot
    """
    return (self.lastPosX,self.lastPosY)
