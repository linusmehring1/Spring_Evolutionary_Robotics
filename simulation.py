import time

import pybullet as p
import pybullet_data

import constants as c
from robot import ROBOT
from world import WORLD


class SIMULATION:
    def __init__(self, directOrGUI, solutionID, fitnessMode):
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        self.fitnessMode = fitnessMode
        
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.GRAVITY_X, c.GRAVITY_Y, c.GRAVITY_Z)

        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def Run(self):
        for t in range(c.SIMULATION_STEPS):
            p.stepSimulation()
            self.robot.Record_Height(t)
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            if self.directOrGUI == "GUI":
                time.sleep(c.SLEEP_TIME)

    def Get_Fitness(self, solutionID):
        self.robot.Get_Fitness(solutionID, self.fitnessMode)

    def __del__(self):
        if p.isConnected():
            p.disconnect()

