import time
import pybullet as p
import pybullet_data

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")

# load world
p.loadSDF("world.sdf")

# load robot
robotId = p.loadURDF("body.urdf")

for i in range(1000):
    p.stepSimulation()
    time.sleep(1/60)

p.disconnect()
