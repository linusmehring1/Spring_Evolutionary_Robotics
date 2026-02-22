import pybullet as p
import pyrosim.pyrosim as pyrosim

from motor import MOTOR
from sensor import SENSOR


class ROBOT:
    def __init__(self):
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for motor in self.motors.values():
            motor.Set_Value(self.robot, t)

    def Save_Sensor_Values(self):
        for sensor in self.sensors.values():
            sensor.Save_Values()

    def Save_Motor_Values(self):
        for motor in self.motors.values():
            motor.Save_Values()
