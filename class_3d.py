from src.modele.simulation import Simulation

# bibliotheque pour la 3d
import os
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Filename, Vec4
from panda3d.core import DirectionalLight, AmbientLight
from panda3d.core import TransparencyAttrib
from panda3d.core import WindowProperties
from panda3d.core import CollisionTraverser, CollisionNode, CollisionBox, CollisionRay, CollisionHandlerQueue
from direct.gui.OnscreenImage import OnscreenImage

path = Filename.fromOsSpecific(os.path.dirname(os.path.realpath(__file__))).getFullpath()
loadPrcFile(path + "/src/view/modeles_3d/config.prc")

class Affichage3D(ShowBase):
    """ Classe pour l'affichage 3D de la simulation"""
    def __init__(self):#, simu: Simulation):
        #self.simu = simu
        self.max_x = 100
        self.max_y = 100
        self.echelle = 1
        ShowBase.__init__(self)
        
        self.loadModels() # Chargement des modeles 3D
        self.setupLights() # Configuration des lumières
        self.generateTerrain() # Génération de l'arene
        self.setupSkybox() # Configuration du ciel
        self.setupCamera() # Configuration de la caméra
        self.captureMouse() # Capture de la souris
        self.setupControls() # Configuration des controles

        self.taskMgr.add(self.update, 'update') # Mise à jour de la simulation

    def update(self, task):
        """Mise à jour de la simulation"""
        if self.cameraSwingActivated: # Si la caméra est activée
            dt = globalClock.getDt()
            md = self.win.getPointer(0) # Récupère la position de la souris
            mouse_x = md.getX()
            mouse_y = md.getY()

            mouse_dx = mouse_x - self.last_mouse_x
            mouse_dy = mouse_y - self.last_mouse_y

            self.cameraSwingFactor = 10 # Facteur de rotation de la caméra

            currentH, currentP, currentR = self.camera.getHpr() # Récupère l'angle de la caméra
            # Rotation de la caméra
            self.camera.setHpr(
                currentH - mouse_dx * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouse_dy * dt * self.cameraSwingFactor)),
                0
            )

            # mise à jour de l'ancienne position de la souris
            self.last_mouse_x = mouse_x
            self.last_mouse_y = mouse_y
        return task.cont

    def setupControls(self):
        """Configure les controles de la simulation"""
        
        
        # Définition des touches de contrôles
        #self.accept('arrow_up', self.changeHeight, [1]) # Augmenter la hauteur
        #self.accept('arrow_down', self.changeHeight, [-1]) # Diminuer la hauteur
        #self.accept('arrow_left', self.rotate, [-1]) # Rotation vers la gauche
        #self.accept('arrow_right', self.rotate, [1]) # Rotation vers la droite
        #self.accept('d', self.move, [1]) # Avancer
        #self.accept('q', self.move, [-1]) # Reculer

        self.accept('escape', self.releaseMouse) # Libère la souris
        self.accept('mouse1', self.captureMouse) # Capture la souris

    def captureMouse(self):
        """Capture la souris"""
        self.cameraSwingActivated = True
        md = self.win.getPointer(0) # Récupère la position de la souris
        self.last_mouse_x = md.getX()
        self.last_mouse_y = md.getY()

        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(props)

    def releaseMouse(self):
        """Libère la souris"""
        self.cameraSwingActivated = False

        props = WindowProperties()
        props.setCursorHidden(False)
        props.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(props)
    
    def setupSkybox(self):
        """Configure le ciel de la simulation"""
        skybox = self.loader.loadModel(path + "/src/view/modeles_3d/skybox/skybox.egg")
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.render)

    def setupCamera(self):
        """Configure la caméra de la simulation"""
        self.disableMouse()
        self.camera.setPos(0, 0, 3)

        crosshairs = OnscreenImage(
            image = path + '/src/view/modeles_3d/crosshairs.png',
            pos = (0, 0, 0),
            scale = 0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    self.createNewBlock(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                        'grass' if z == 0 else 'dirt'
                    )

    #def generateTerrain(self):
        #"""Génère l'arene """
        #for y in range(self.max_y):
            #for x in range(self.max_x):
                #self.createNewBlock(
                    #x - self.max_x,
                    #y - self.max_y,
                    #0,
                    #'grass' #if z == 0 else 'dirt'
                #)

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
        # Charger le modèle du robot
        self.robot = self.loader.loadModel(path + "/src/view/modeles_3d/robot_metale.glb")
        #self.robot.setScale(.5)  # Redimensionne le modèle 
        self.robot.reparentTo(self.render)
        self.robot.setPos(-self.max_x/2, -self.max_y/2, -2)  # Positionne le modèle

        # Charger les modèles du sol
        self.solBlock = self.loader.loadModel(path + "/src/view/modeles_3d/sol-block.glb")
        self.grassBlock = self.loader.loadModel(path + "/src/view/modeles_3d/grass-block.glb")
        self.dirtBlock = self.loader.loadModel(path + "/src/view/modeles_3d/dirt-block.glb")
        
        # Point the camera at the robot
        #self.camera.lookAt(self.robot)

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
    app = Affichage3D()
    app.run()
