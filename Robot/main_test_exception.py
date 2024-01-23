from Grille_v2_no_fini import *
from Robot_v2_no_fini import *
import time

nb_dir = 4

def main():
  list_dir = ["DOWN", "UP", "RIGHT", "LEFT"]
  

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