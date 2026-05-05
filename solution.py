import numpy
import random
import os
import time
import pyrosim.pyrosim as pyrosim
import constants as c


class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        self.longestFlight = 0
        self.horizontalDistance = 0.0
        self.maxHeight = 0.0

    def Set_ID(self, myID):
        self.myID = myID

    def Start_Simulation(self, directOrGUI, fitnessMode):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        os.system(
            "python3 simulate.py "
            + directOrGUI
            + " "
            + str(self.myID)
            + " "
            + fitnessMode
            + " 2>&1 &"
        )

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        statsFileName = "stats" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        while not os.path.exists(statsFileName):
            time.sleep(0.01)
        
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()

        statsFile = open(statsFileName, "r")
        statsContents = statsFile.read().strip().split(",")
        statsFile.close()
        if len(statsContents) == 3:
            self.longestFlight = int(float(statsContents[0]))
            self.horizontalDistance = float(statsContents[1])
            self.maxHeight = float(statsContents[2])
        
        os.system("rm " + fitnessFileName)
        os.system("rm " + statsFileName)

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        pyrosim.Send_Cube(
            name="Box",
            pos=[0, 5, 0.5],
            size=[1, 1, 1]
        )

        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")

        # Torso at center
        pyrosim.Send_Cube(
            name="Torso",
            pos=[0, 0, 1],
            size=[1, 1, 1]
        )

        # Front leg (pointing in +y direction)
        pyrosim.Send_Joint(
            name="Torso_FrontLeg",
            parent="Torso",
            child="FrontLeg",
            type="revolute",
            position=[0, 0.5, 1],
            jointAxis="1 0 0"
        )
        pyrosim.Send_Cube(
            name="FrontLeg",
            pos=[0, 0.5, 0],
            size=[0.2, 1, 0.2]
        )

        # Back leg (pointing in -y direction)
        pyrosim.Send_Joint(
            name="Torso_BackLeg",
            parent="Torso",
            child="BackLeg",
            type="revolute",
            position=[0, -0.5, 1],
            jointAxis="1 0 0"
        )
        pyrosim.Send_Cube(
            name="BackLeg",
            pos=[0, -0.5, 0],
            size=[0.2, 1, 0.2]
        )

        # Left leg (pointing in +x direction)
        pyrosim.Send_Joint(
            name="Torso_LeftLeg",
            parent="Torso",
            child="LeftLeg",
            type="revolute",
            position=[0.5, 0, 1],
            jointAxis="0 1 0"
        )
        pyrosim.Send_Cube(
            name="LeftLeg",
            pos=[0.5, 0, 0],
            size=[1, 0.2, 0.2]
        )

        # Right leg (pointing in -x direction)
        pyrosim.Send_Joint(
            name="Torso_RightLeg",
            parent="Torso",
            child="RightLeg",
            type="revolute",
            position=[-0.5, 0, 1],
            jointAxis="0 1 0"
        )
        pyrosim.Send_Cube(
            name="RightLeg",
            pos=[-0.5, 0, 0],
            size=[1, 0.2, 0.2]
        )

        # Front lower leg
        pyrosim.Send_Joint(
            name="FrontLeg_FrontLowerLeg",
            parent="FrontLeg",
            child="FrontLowerLeg",
            type="revolute",
            position=[0, 1, 0],
            jointAxis="1 0 0"
        )
        pyrosim.Send_Cube(
            name="FrontLowerLeg",
            pos=[0, 0, -0.5],
            size=[0.2, 0.2, 1]
        )

        # Back lower leg
        pyrosim.Send_Joint(
            name="BackLeg_BackLowerLeg",
            parent="BackLeg",
            child="BackLowerLeg",
            type="revolute",
            position=[0, -1, 0],
            jointAxis="1 0 0"
        )
        pyrosim.Send_Cube(
            name="BackLowerLeg",
            pos=[0, 0, -0.5],
            size=[0.2, 0.2, 1]
        )

        # Left lower leg
        pyrosim.Send_Joint(
            name="LeftLeg_LeftLowerLeg",
            parent="LeftLeg",
            child="LeftLowerLeg",
            type="revolute",
            position=[1, 0, 0],
            jointAxis="0 1 0"
        )
        pyrosim.Send_Cube(
            name="LeftLowerLeg",
            pos=[0, 0, -0.5],
            size=[0.2, 0.2, 1]
        )

        # Right lower leg
        pyrosim.Send_Joint(
            name="RightLeg_RightLowerLeg",
            parent="RightLeg",
            child="RightLowerLeg",
            type="revolute",
            position=[-1, 0, 0],
            jointAxis="0 1 0"
        )
        pyrosim.Send_Cube(
            name="RightLowerLeg",
            pos=[0, 0, -0.5],
            size=[0.2, 0.2, 1]
        )

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # Sensor neurons only for feet (lower legs)
        pyrosim.Send_Sensor_Neuron(name=0, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="RightLowerLeg")

        # Motor neurons for all 8 joints
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=8, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=9, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_RightLowerLeg")

        # Synapses connecting sensor neurons to motor neurons
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow,
                    targetNeuronName=currentColumn + c.numSensorNeurons,
                    weight=self.weights[currentRow, currentColumn]
                )

        pyrosim.End()
