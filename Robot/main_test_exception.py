from Grille_v2_no_fini import *
from Robot_v2_no_fini import *
import time

nb_dir = 4

def main():
  list_dir = ["DOWN", "UP", "RIGHT", "LEFT"]
  grille = Grille(8,8,1)

  #Test de la borne LEFT
  print("Test de la borne LEFT")
  robot1 = Robot("R1", 9, 0, 1, 1, grille)
  print ("Robot 1 :" + str(robot1.getCurrPos()))
  grille.affiche()
  
  #Test de la borne DOWN
  print("Test de la borne DOWN")
  robot2 = Robot("R2", 0, 9, 1, 1, grille)
  print ("Robot 2 :" + str(robot2.getCurrPos()))
  grille.affiche()

  #Test de la borne UP
  print("Test de la borne UP")
  robot3 = Robot("R3", 0, -1, 1, 1, grille)
  print ("Robot 3 :" + str(robot3.getCurrPos()))
  grille.affiche()

  #Test de la borne RIGHT
  print("Test de la borne RIGHT")
  robot4 = Robot("R4", -1, 0, 1, 1, grille)
  print ("Robot 4 :" + str(robot3.getCurrPos()))
  grille.affiche()

  ###### MARCHER LE ROBOT #####
  g = Grille(5,5,1)
  r = Robot("Dexter", 0, 0, 1, 1, g)
  
  print("Etat initial : " + str(r.getCurrPos()))  
  g.affiche()
  time.sleep(2)
  dis = 2
  for i in range(nb_dir):
    print(list_dir[i] + " de " + str(dis))
    r.go(list_dir[i], 0, dis)
    print("Robot est desormais en " + str(r.getCurrPos()))
    time.sleep(3)

main()