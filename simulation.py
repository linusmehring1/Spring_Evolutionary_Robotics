import time

import pybullet as p
import pybullet_data

import constants as c
from robot import ROBOT
from world import WORLD


class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.GRAVITY_X, c.GRAVITY_Y, c.GRAVITY_Z)

        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        for t in range(c.SIMULATION_STEPS):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Act(t)
            time.sleep(c.SLEEP_TIME)

    def __del__(self):
        if p.isConnected():
            p.disconnect()
