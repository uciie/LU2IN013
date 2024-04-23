import logging
# bibliotheque pour la 3d
import os
import threading
import time

from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import Sequence
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (AmbientLight, CollisionBox, CollisionHandlerQueue,
                          CollisionNode, CollisionRay, CollisionTraverser,
                          DirectionalLight, Filename, PandaNode, Point3,
                          TransparencyAttrib, Vec4, WindowProperties,
                          loadPrcFile)

from ..modele.simulation import Simulation

path = Filename.fromOsSpecific(os.path.dirname(os.path.realpath(__file__))).getFullpath()
loadPrcFile(path + "/modeles_3d/config.prc")

class Affichage3D(ShowBase):
    """ Classe pour l'affichage 3D de la simulation"""
    def __init__(self, vitesse: float, simu: Simulation):
        self.simu = simu
        self.max_x =  self.simu._arene.max_y
        self.max_y = self.simu._arene.max_x
        self.echelle = 1/4
        ShowBase.__init__(self)
        #configuraiton du logging 
        self.logger = logging.getLogger(__name__)

        
        self.loadModels() # Chargement des modeles 3D
        self.setupLights() # Configuration des lumières
        self.generateArene() # Génération de l'arene
        self.setupSkybox() # Configuration du ciel
        self.setupCamera() # Configuration de la caméra
        self.setupControls() # Configuration des controles

        self.taskMgr.add(self.update, 'update') # Mise à jour de la simulation
        #self.move_robot()

    def update(self, task):
        """Mise à jour de la simulation"""
 
            # Déplacement 
        if self.dico_cles['vers_haut']:
            # Incliner la caméra de 1 degré
            self.camera.setP(self.camera.getP() + 1)
            self.logger.info(f"Camera vers le haut: {self.camera.getP()}")
        elif self.dico_cles['vers_bas']:
            self.camera.setP(self.camera.getP() - 1)
            self.logger.info(f"Camera vers le bas: {self.camera.getP()}")
        
        #Mise à jour des coordonnées du robot
        self.robot_node.setY((self.simu.robot.pos_x  - self.max_x//2)* self.echelle)
        self.robot_node.setX((self.simu.robot.pos_y - self.max_y//2) * self.echelle)
        self.robot_node.setH(self.simu.robot._theta + 90)
        #self.robot_node.setPos(self.pos_x, self.pos_y, 5)
        self.logger.info(f"Robot position: {self.robot_node.getX()}, {self.robot_node.getY()}")

        # Mettre à jour la position de la caméra
        self.camera.setPos(self.robot_node.getX(), self.robot_node.getY(), self.camera.getZ())  # Place la caméra derrière et légèrement au-dessus du robot
        self.camera.setH(self.robot_node.getH() )  # Oriente la caméra vers le robot
        


        return task.cont

    def setupControls(self):
        """Configure les controles de la simulation"""
        self.dico_cles= {
            'vers_haut': False, # Augmenter la hauteur
            'vers_bas': False, # Diminuer la hauteur
            'vers_gauche': False, # Rotation vers la gauche
            'vers_droite': False, # Rotation vers la droite
            'avancer': False, # Avancer
            'reculer': False, # Reculer
            'vue_3D': True # Changer de vue3d en 2d (vue de dessus)
        }
        
        # Définition des touches de contrôles
        self.accept('arrow_up',self.updateDico_cles, ['vers_haut',True])
        self.accept('arrow_up-up',self.updateDico_cles, ['vers_haut',False])
        self.accept('arrow_down',self.updateDico_cles, ['vers_bas',True])
        self.accept('arrow_down-up',self.updateDico_cles, ['vers_bas',False])
        self.accept('arrow_left',self.updateDico_cles, ['vers_gauche',True])
        self.accept('arrow_left-up',self.updateDico_cles, ['vers_gauche',False])
        self.accept('arrow_right',self.updateDico_cles, ['vers_droite',True])
        self.accept('arrow_right-up',self.updateDico_cles, ['vers_droite',False])


        # changer de point de vue 
        self.accept('escape', self.changeView)

    def changeView(self):
        """Changer de point de vue"""
        # Passer en 2d
        if self.dico_cles['vue_3D']:
            self.dico_cles['vue_3D'] = False
            self.camera.setPos(0, 0, 30)
            self.camera.setHpr(0, -90, 0)
        else: # Passer en 3d
            self.dico_cles['vue_3D'] = True
            self.camera.setPos(0, 0, 5)
            self.camera.setHpr(0, 0, 0)

    def updateDico_cles(self, key, value):
        """Met à jour le dictionnaire de touches"""
        if key in self.dico_cles:
            self.dico_cles[key] = value
    
    def setupSkybox(self):
        """Configure le ciel de la simulation"""
        skybox = self.loader.loadModel(path + "/modeles_3d/skybox/skybox.egg")
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def setupCamera(self):
        """Configure la caméra de la simulation"""
        self.disableMouse()
        self.camera.setPos((self.simu.robot.pos_x  - self.max_x) * self.echelle , (self.simu.robot.pos_y  - self.max_y) * self.echelle, 5)  # Place la caméra derrière et légèrement au-dessus du robot

        crosshairs = OnscreenImage(
            image = path + '/modeles_3d/crosshairs.png',
            pos = (0, 0, 0),
            scale = 0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

    def generateArene(self):
        """Génère l'arene' de la simulation"""
        for y in range(int(self.max_y*self.echelle)):
            for x in range(int((self.max_x//2)*self.echelle)):
                self.createNewBlock(
                    x*2 - int((self.max_x//2)*self.echelle),
                    y*2 - int((self.max_y//2)*self.echelle),
                    0,
                    'grass'
                )

    def createNewBlock(self, x, y, z, type):
        """Crée un nouveau bloc à la position spécifiée"""
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)

        if type == 'grass':
            self.grassBlock.instanceTo(newBlockNode)
        elif type == 'dirt':
            self.dirtBlock.instanceTo(newBlockNode)
        elif type == 'sol':
            self.solBlock.instanceTo(newBlockNode)

        blockSolid = CollisionBox((-1, -1, -1), (1, 1, 1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)
                
    def loadModels(self):
        """Telecharge les modeles 3D et les ajoute a la scene"""
        # Créer un noeud pour robot
        self.robot_node = self.render.attachNewNode(PandaNode("RobotNode"))
        # Charger le modèle du robot
        self.robot = self.loader.loadModel(path + "/modeles_3d/robot_3roues.glb")
        self.robot.reparentTo(self.robot_node)
        self.robot.setPos((self.simu.robot.pos_y - self.max_y//2) * self.echelle ,(self.simu.robot.pos_x - self.max_x//2) * self.echelle, 2)  # Positionne le modèle
        self.robot.setH(self.simu.robot._theta + 180)
        self.robot.setP(90)
        # Charger les modèles du sol
        self.solBlock = self.loader.loadModel(path + "/modeles_3d/sol-block.glb")
        self.grassBlock = self.loader.loadModel(path + "/modeles_3d/grass-block.glb")
        self.dirtBlock = self.loader.loadModel(path + "/modeles_3d/dirt-block.glb")
        self.solBlock.setP(90)
        self.grassBlock.setP(90)
        self.dirtBlock.setP(90)
    def setupLights(self):
        """Configure les lumières de la scène"""
        # Créer une nouvelle lumière ambiante
        self.alight = AmbientLight('alight')
        self.alight.setColor(Vec4(1, 1, 1, 1))  # Définir la couleur de la lumière
        self.alnp = self.render.attachNewNode(self.alight)

        # Ajouter la lumière à la scène
        self.render.setLight(self.alnp)

        # Créer une nouvelle lumière directionnelle
        self.dir_light_left = DirectionalLight('dir_light_left')
        self.dir_light_left.setColor(Vec4(1, 1, 1, 10))
        self.dir_light_node_left = self.render.attachNewNode(self.dir_light_left)
        self.dir_light_node_left.setHpr(30, -60, 0)

        # Ajouter la lumière à la scène
        self.render.setLight(self.dir_light_node_left)


if __name__ == "__main__":
    app = Affichage3D(10)
    app.run()
