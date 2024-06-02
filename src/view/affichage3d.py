import logging
# bibliotheque pour la 3d
import os
import cv2
from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import Sequence
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (AmbientLight, CollisionBox, CollisionHandlerQueue,
                          CollisionNode, CollisionRay, CollisionTraverser,
                          DirectionalLight, Filename, PandaNode, Point3,
                          TransparencyAttrib, Vec4, WindowProperties,
                          loadPrcFile, NodePath, TextNode)

from src.modele.objets import ObstacleRectangle
from src.modele.simulation import Simulation
from src.modele.utilitaire import check_directory
import os

path = Filename.fromOsSpecific(os.path.dirname(os.path.realpath(__file__))).getFullpath()
loadPrcFile(path + "/modeles_3d/config.prc")

class Affichage3D(ShowBase):
    """ Classe pour l'affichage 3D de la simulation"""
    def __init__(self, simu: Simulation):
        self.simu = simu
        self.max_x =  self.simu._arene.max_y
        self.max_y = self.simu._arene.max_x
        self.echelle = 1/4
        ShowBase.__init__(self)
        #configuraiton du logging 
        self.logger = logging.getLogger(__name__)
        check_directory() # Vérifier si le répertoire de sauvegarde des images existe
        self.recording = False
        self.image = None
        self.loadModels() # Chargement des modeles 3D
        self.setupLights() # Configuration des lumières
        self.generateArene() # Génération de l'arene
        self.generateObstacles() # Génération des obstacles
        self.generateBalise() # Génération de la balise
        self.setupSkybox() # Configuration du ciel
        self.setupCamera() # Configuration de la caméra
        self.setupControls() # Configuration des controles
        self.setupInstructions() # Configuration des instructions

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
        elif self.dico_cles['vers_gauche']:
            self.camera.setH(self.camera.getH() + 1)
            self.logger.info(f"Camera vers la gauche: {self.camera.getH()}")
        elif self.dico_cles['vers_droite']:
            self.camera.setH(self.camera.getH() - 1)
            self.logger.info(f"Camera vers la droite: {self.camera.getH()}")
        
        
        #Mise à jour des coordonnées du robot
        self.robot_node.setY((self.simu.robot.pos_x  - self.max_x//2)* self.echelle)
        self.robot_node.setX((self.simu.robot.pos_y - self.max_y//2) * self.echelle)
        self.robot_node.setH(self.simu.robot._theta + 90)
        #self.robot_node.setPos(self.pos_x, self.pos_y, 5)
        self.logger.info(f"Robot position: {self.robot_node.getX()}, {self.robot_node.getY()}")

        # Mettre à jour la position de la caméra
        self.camera.setPos(self.robot_node.getX(), self.robot_node.getY(), self.camera.getZ())  # Place la caméra derrière et légèrement au-dessus du robot
        self.camera.setH(self.camera.getH())
        
        # enregistrement de l'image si l'enregistrement est activé
        if self.recording:
            self.screenshot("enregistrement_image/image.png", False)
            self.image = cv2.imread("enregistrement_image/image.png")

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
            'vue_3D': False # Changer de vue3d en 2d (vue de dessus)
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
        #
        self.accept('s', lambda: self.screenshot("enregistrement_image/image.png", False))

    def changeView(self):
        """Changer de point de vue"""
        # Passer en 2d
        if self.dico_cles['vue_3D']:
            self.dico_cles['vue_3D'] = False
            self.camera.setPos(0, 0, 25)
            self.camera.setHpr(0, -15, 0)
        else: # Passer en 3d
            self.dico_cles['vue_3D'] = True
            self.camera.setPos(0, 0, 50*5)
            self.camera.setHpr(0, -90, 0)

    def updateDico_cles(self, key, value):
        """Met à jour le dictionnaire de touches"""
        if key in self.dico_cles:
            self.dico_cles[key] = value

    def setupInstructions(self):
        """Configure les instructions de la simulation"""
        instructions_text = (
            "Haut/Bas: Inclinaison de la caméra\n"
            "Gauche/Droite: Rotation de la caméra\n"
            "Appuyez sur 's' pour prendre une capture d'écran\n"
            "Appuyez sur 'ESC' pour changer de vue (2D/3D)"
        )
        self.instructions = OnscreenText(
            text=instructions_text,
            pos=(-1.3, 0.9),  # Position sur l'écran
            scale=0.05,       # Échelle du texte
            fg=(1, 1, 1, 1),  # Couleur du texte (blanc)
            align=TextNode.ALeft,  # Alignement du texte à gauche
            shadow=(0, 0, 0, 1),  # Couleur de l'ombre du texte (noir)
            shadowOffset=(0.05, 0.05),  # Décalage de l'ombre
            mayChange=False  # Si False, le texte ne changera pas
        )
    
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
        self.camera.setPos((self.simu.robot.pos_x  - self.max_x) * self.echelle , (self.simu.robot.pos_y  - self.max_y) * self.echelle, 5*5)  # Place la caméra derrière et légèrement au-dessus du robot
        self.camera.setHpr(self.robot_node.getH()+90, -15, 0)

        crosshairs = OnscreenImage(
            image = path + '/modeles_3d/crosshairs.png',
            pos = (0, 0, 0),
            scale = 0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

    def generateArene(self):
        """Génère l'arene' de la simulation"""
        for y in range(int(self.max_y//2*self.echelle)):
            for x in range(int(self.max_x//2*self.echelle)):
                self.createNewBlock(
                    x*2 - int((self.max_x//2)*self.echelle),
                    y*2 - int((self.max_y//2)*self.echelle),
                    0,
                    'grass',
                    1,
                    1,
                    1
                )

    def generateObstacles(self):
        """Génère les obstacles de la simulation"""
        cpt = 0 
        self.logger.info(f"Nb Obstacle {len(self.simu.arene.liste_Obstacles)} a ajouter")
        for obstacle in self.simu.arene.liste_Obstacles:
            if isinstance(obstacle, ObstacleRectangle):
                for i in range(7):
                    c1 = obstacle._coin1._x
                    c2 = obstacle._coin2._x
                    self.createNewBlock(
                        (obstacle.pos_y - self.max_y//2)* self.echelle,
                        (obstacle.pos_x - self.max_x//2)* self.echelle,
                        i,
                        'dirt',
                        c2 * self.echelle,
                        c1*self.echelle,
                        1   
                    )
                    
                cpt += 1
                self.logger.info(f"Obstacle {cpt} rectangle ajouté ")
                
    def generateBalise(self):
        """Génère la balise de la simulation"""
        # Créer un noeud pour balise
        self.createNewBlock(
                            -50, 
                            -10,
                            10,
                            'balise',
                            10,
                            10,
                            10
                            )
        
            
    def createNewBlock(self, x, y, z, type, scale_x, scale_y, scale_z):
        """Crée un nouveau bloc à la position spécifiée"""
        newBlockNode = self.render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x, y, z)
        newBlockNode.setScale(scale_x,scale_y,scale_z)
        if type == 'grass':
            self.grassBlock.instanceTo(newBlockNode)
        elif type == 'dirt':
            self.dirtBlock.instanceTo(newBlockNode)
        elif type == 'sol':
            self.solBlock.instanceTo(newBlockNode)
        elif type == 'balise':
            self.balise.instanceTo(newBlockNode)
            self.balise.setHpr(180, 0, 90) 
        
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
        self.robot.setScale(5,5,5)
        
        # Charger le modèle de balise 
        self.balise = self.loader.loadModel(path + "/modeles_3d/balise.glb")
    
        # Charger les modèles du sol
        self.solBlock = self.loader.loadModel(path + "/modeles_3d/sol-block.glb")
        self.grassBlock = self.loader.loadModel(path + "/modeles_3d/grass-block.glb")
        self.dirtBlock = self.loader.loadModel(path + "/modeles_3d/dirt-block.glb")
        
        # rotation des blocs
        self.solBlock.setP(90)
        self.grassBlock.setP(90)
        self.dirtBlock.setP(90)
        self.balise.setP(90)

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
