import os
import numpy
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c

from motor import MOTOR
from sensor import SENSOR


class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.robot = p.loadURDF("body" + str(solutionID) + ".urdf")
        self.torsoHeights = numpy.zeros(c.SIMULATION_STEPS)
        pyrosim.Prepare_To_Simulate(self.robot)
        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")
        os.system("rm body" + str(solutionID) + ".urdf")
        os.system("rm brain" + str(solutionID) + ".nndf")

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

    def Think(self):
        self.nn.Update()

    def Record_Height(self, t):
        torsoState = p.getLinkState(self.robot, 0)
        torsoPosition = torsoState[0]
        self.torsoHeights[t] = torsoPosition[2]

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robot, desiredAngle)

    def Get_Fitness(self, solutionID, fitnessMode="A"):
        # Access touch sensor values from all four lower legs
        # Touch sensor values: -1 = foot off ground, +1 = foot on ground
        frontLowerLegValues = self.sensors["FrontLowerLeg"].values
        backLowerLegValues = self.sensors["BackLowerLeg"].values
        leftLowerLegValues = self.sensors["LeftLowerLeg"].values
        rightLowerLegValues = self.sensors["RightLowerLeg"].values

        # Find the longest contiguous period where ALL four feet are off the ground
        allFeetOff = (
            (frontLowerLegValues == -1) &
            (backLowerLegValues == -1) &
            (leftLowerLegValues == -1) &
            (rightLowerLegValues == -1)
        )

        # Use numpy to find contiguous runs of all-feet-off timesteps
        padded = numpy.concatenate([[False], allFeetOff, [False]])
        changes = numpy.diff(padded.astype(int))
        starts = numpy.where(changes == 1)[0]
        ends = numpy.where(changes == -1)[0]
        if len(starts) > 0:
            longestFlight = int(numpy.max(ends - starts))
        else:
            longestFlight = 0

        # Horizontal distance term for Milestone 4 long-jump objective
        torsoState = p.getLinkState(self.robot, 0)
        torsoPosition = torsoState[0]
        horizontalDistance = abs(torsoPosition[0])
        maxHeight = float(numpy.max(self.torsoHeights))

        # A: pure jump objective (maximize longest flight)
        # B: long jump objective (maximize distance * flight)
        if fitnessMode == "B":
            fitness = float(longestFlight) * float(horizontalDistance)
        else:
            fitness = float(longestFlight)

        tmpFileName = "tmp" + str(solutionID) + ".txt"
        fitnessFileName = "fitness" + str(solutionID) + ".txt"
        
        fitnessFile = open(tmpFileName, "w")
        fitnessFile.write(str(fitness))
        fitnessFile.close()

        statsTmpFileName = "tmp_stats" + str(solutionID) + ".txt"
        statsFileName = "stats" + str(solutionID) + ".txt"
        statsFile = open(statsTmpFileName, "w")
        statsFile.write(f"{longestFlight},{horizontalDistance},{maxHeight}")
        statsFile.close()
        
        os.system("mv " + tmpFileName + " " + fitnessFileName)
        os.system("mv " + statsTmpFileName + " " + statsFileName)

    def Save_Sensor_Values(self):
        for sensor in self.sensors.values():
            sensor.Save_Values()
