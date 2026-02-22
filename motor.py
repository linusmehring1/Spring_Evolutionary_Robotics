import os

import numpy
import pybullet as p
import pyrosim.pyrosim as pyrosim

import constants as c


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.DEFAULT_MOTOR_AMPLITUDE
        self.frequency = c.DEFAULT_MOTOR_FREQUENCY
        self.offset = c.DEFAULT_MOTOR_OFFSET

        if self._joint_name_text() == c.HALF_FREQUENCY_JOINT_NAME:
            self.frequency = self.frequency * c.HALF_FREQUENCY_SCALE

        self.motorValues = self.amplitude * numpy.sin(
            self.frequency * c.MOTOR_COMMAND_TIMES + self.offset
        )

    def Set_Value(self, robot, t):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=self.motorValues[t],
            maxForce=c.MAX_MOTOR_FORCE,
        )

    def Save_Values(self):
        os.makedirs(c.DATA_DIRECTORY, exist_ok=True)
        filename = f"{c.DATA_DIRECTORY}/{self._joint_name_text()}MotorValues.npy"
        numpy.save(filename, self.motorValues)

    def _joint_name_text(self):
        if isinstance(self.jointName, bytes):
            return self.jointName.decode("utf-8")

        return self.jointName
