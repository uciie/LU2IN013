import unittest
from .simulation/robot import Robot

class TestRobot(unittest.TestCase):

    def setUp(self) :
        """Initialisation du robot"""
        r = Robot("r", 5, 5, 2, 2, "red")