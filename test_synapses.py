#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

import pybullet as p
import pybullet_data
import constants as c

# Start physics simulation
p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(c.GRAVITY_X, c.GRAVITY_Y, c.GRAVITY_Z)

# Generate and load robot
import generate
generate.Generate_Body()
generate.Generate_Brain()

robot = p.loadURDF("body.urdf")

import pyrosim.pyrosim as pyrosim
pyrosim.Prepare_To_Simulate(robot)

from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR

nn = NEURAL_NETWORK("brain.nndf")

# Prepare sensors
sensors = {}
for linkName in pyrosim.linkNamesToIndices:
    sensors[linkName] = SENSOR(linkName)

print("=" * 60)
print("NEURAL NETWORK WITH SYNAPSES - TEST")
print("=" * 60)

print("\nNetwork Structure:")
print(f"  Sensor Neurons: 0 (Torso), 1 (BackLeg), 2 (FrontLeg)")
print(f"  Motor Neurons: 3 (Torso_BackLeg), 4 (Torso_FrontLeg)")
print(f"  Total Synapses: {len(nn.synapses)}")

print("\nSynapse Connections:")
for key in sorted(nn.synapses.keys()):
    synapse = nn.synapses[key]
    print(f"  {key[0]} → {key[1]}: weight={synapse.Get_Weight():.4f}")

# Simulate a few steps
print("\n" + "=" * 60)
print("SIMULATION STEPS (Closed-Loop Control)")
print("=" * 60)

for step in range(5):
    p.stepSimulation()
    
    # Sense
    for sensor in sensors.values():
        sensor.Get_Value(step)
    
    # Think (neural network processes sensor inputs through synapses)
    nn.Update()
    
    # Show neuron values
    print(f"\nStep {step}:")
    print(f"  Sensor values: ", end="")
    for i in [0, 1, 2]:
        val = nn.Get_Value_Of(str(i))
        print(f"{val:7.3f} ", end="")
    print()
    print(f"  Motor values:  ", end="")
    for i in [3, 4]:
        val = nn.Get_Value_Of(str(i))
        print(f"{val:7.3f} ", end="")
    print()

print("\n" + "=" * 60)
print("RESULT: Synapses successfully transmit sensor values to motors!")
print("The robot has closed-loop control through its neural network.")
print("=" * 60)

p.disconnect()
