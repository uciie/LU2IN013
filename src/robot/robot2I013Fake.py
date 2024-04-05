import math
import random
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='logs/robot2I013.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Désactiver les messages de journalisation pour le module spécifié
# logging.getLogger('src.robot.robot2I013').setLevel(logging.WARNING)

class Robot2IN013:
    """
    Classe d'encapsulation du robot et des senseurs.
    Constantes disponibles :
    LED (controle des LEDs) :  LED_LEFT_EYE, LED_RIGHT_EYE, LED_LEFT_BLINKER, LED_RIGHT_BLINKER, LED_WIFI
    MOTEURS (gauche et droit) : MOTOR_LEFT, MOTOR_RIGHT
    et les constantes ci-dessous qui definissent les elements physiques du robot

    """

    WHEEL_BASE_WIDTH = 117  # distance (mm) de la roue gauche a la roue droite.
    WHEEL_DIAMETER = 66.5  # diametre de la roue (mm)
    WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi  # perimetre du cercle de rotation (mm)
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi  # perimetre de la roue (mm)

    MOTOR_LEFT = 1 # moteur gauche
    MOTOR_RIGHT = 2 # moteur droit
    
    position_moteurs = [0, 0] # positions des moteurs entre 0 (0°) et 1 (360°)

    v_ang_roue_d = 0 # vitesse angulaire de la roue droite
    v_ang_roue_g = 0 # vitesse angulaire de la roue gauche

    def __init__(self, nb_img=10, fps=25, resolution=None, servoPort="SERVO1", motionPort="AD1"):
        """
            Initialise le robot
            :resolution: resolution de la camera
            :servoPort: port du servo (SERVO1 ou SERVO2)
            :motionPort: port pour l'accelerometre (AD1 ou AD2)
        """
        self.fps = fps
        self._img_queue = None
        self.nb_img = nb_img
        
        self._recording = False
        self._thread = None
        self.start_recording()
        self.logger = logging.getLogger(__name__)

    def stop(self):
        """ Arrete le robot """
        self.v_ang_roue_d , self.v_ang_roue_g = 0, 0

    def get_image(self):
        try:
            return self._img_queue[-1][0]
        except Exception as e:
            pass

    def get_images(self):
        try:
            return list(reversed(self._img_queue))
        except Exception as e:
            pass

    def set_motor_dps(self, port, dps):
        """
        Fixe la vitesse d'un moteur en nombre de degres par seconde

        :port: une constante moteur,  MOTOR_LEFT ou MOTOR_RIGHT (ou les deux MOTOR_LEFT+MOTOR_RIGHT).
        :dps: la vitesse cible en nombre de degres par seconde
        """
        self.logger.info(f"Set moteur : {port}, vitesse : {dps}")
        if (port == self.MOTOR_LEFT):
            self.vit_roue_gauche = dps
        elif (port == self.MOTOR_RIGHT):
            self.vit_roue_droite = dps
        else:
            self.vit_roue_gauche = dps
            self.vit_roue_droite = dps

    def get_motor_position(self):
        """
        Lit les etats des moteurs en degre.
        :return: couple du  degre de rotation des moteurs
        """
        # Simule la variation des positions des moteurs en fonction de leurs vitesses
        if self.v_ang_roue_g >= 0:
            self.position_moteurs[0] += random.randint(0, 1)  # Ajoute un changement aléatoire entre 0 et 5 degrés
        else:
            self.position_moteurs[0] -= random.randint(0, 1)  # Soustrait un changement aléatoire entre 0 et 5 degrés

        if self.v_ang_roue_d >= 0:
            self.position_moteurs[1] += random.randint(0, 1)  # Ajoute un changement aléatoire entre 0 et 5 degrés
        else:
            self.position_moteurs[1] -= random.randint(0, 1)  # Soustrait un changement aléatoire entre 0 et 5 degrés
        
        # les positions des moteurs restent dans la plage [0, 1]
        self.position_moteurs = [max(0, min(1, position)) for position in self.position_moteurs]
        
        # Retourne les positions simulées des moteurs
        return self.position_moteurs

    def offset_motor_encoder(self, port, offset):
        """
        Fixe l'offset des moteurs (en degres) (permet par exemple de reinitialiser a 0 l'etat
        du moteur gauche avec offset_motor_encode(self.MOTOR_LEFT,self.read_encoders()[0])

        :port: un des deux moteurs MOTOR_LEFT ou MOTOR_RIGHT (ou les deux avec +)
        :offset: l'offset de decalage en degre.

        Zero the encoder by offsetting it by the current position
        """
        if port == self.MOTOR_LEFT :
            self.position_moteurs[0] = offset
        elif port == self.MOTOR_RIGHT :
            self.position_moteurs[1] = offset
        elif port == self.MOTOR_LEFT+ self.MOTOR_RIGHT :
            self.position_moteurs[0] = offset
            self.position_moteurs[1] = offset

    def get_distance(self):
        """
        Lit le capteur de distance (en mm).
        :returns: entier distance en millimetre.
            1. L'intervalle est de **5-8,000** millimeters.
            2. Lorsque la valeur est en dehors de l'intervalle, le retour est **8190**.
        """
        if random.random() > 0.5:
            return 8190
        return random.randint(5, 8000)

    def servo_rotate(self, position):
        """
        Tourne le servo a l'angle en parametre.
        :param int position: Angle de rotation, de **0** a **180** degres, 90 pour le milieu.
        """
        #self.servo.rotate_servo(position)
        pass

    def start_recording(self):
        #if self._recording or self._thread is not None:
        #    self._stop_recording()
        #self._recording = True
        #self._thread = threading.Thread(target=self._start_recording)
        #self._thread.start()
        pass

    def _stop_recording(self):
        self._recording = False
        self._thread.join()
        self._thread = None

    def _start_recording(self):
        #try:
            #self._img_queue = deque(maxlen=self.nb_img)
            #with  picamera.PiCamera() as camera:
                #camera.resolution = self.resolution
                #camera.framerate = 24
                #camera.start_preview()
                #i = 0
                #while self._recording:
                    #time.sleep(1 / self.fps_camera)
                    #out = np.zeros((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
                    #camera.capture(out, 'rgb', use_video_port=True)
                    #self._img_queue.append((out, time.time()))
        #except Exception as e:
            #print("Camera not found", e)
        pass

    def __getattr__(self, attr):
        """ Méthodes héritées de GPG :
        * set_led(self, led, red = 0, green = 0, blue = 0)
            Allume une led.

            :led: une des constantes LEDs (ou plusieurs combines avec +) : LED_LEFT_EYE, LED_RIGHT_EYE, LED_LEFT_BLINKER, LED_RIGHT_BLINKER, LED_WIFI.
            :red: composante rouge (0-255)
            :green:  composante verte (0-255)
            :blue: composante bleu (0-255)
        """
        #return self._gpg.__getattribute__(attr)
        pass

