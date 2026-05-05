import numpy

GRAVITY_X = 0.0
GRAVITY_Y = 0.0
GRAVITY_Z = -9.8

SIMULATION_STEPS = 1000
SLEEP_TIME = 1.0 / 120.0

MAX_MOTOR_FORCE = 180

DEFAULT_MOTOR_AMPLITUDE = numpy.pi / 4.5
DEFAULT_MOTOR_FREQUENCY = 4.0
DEFAULT_MOTOR_OFFSET = 0.0

HALF_FREQUENCY_JOINT_NAME = "Torso_FrontLeg"
HALF_FREQUENCY_SCALE = 0.5

MOTOR_COMMAND_TIMES = numpy.linspace(
    0.0,
    2.0 * numpy.pi,
    SIMULATION_STEPS,
)

DATA_DIRECTORY = "data"

numberOfGenerations = 10
populationSize = 10

numSensorNeurons = 4
numMotorNeurons = 8
motorJointRange = 0.2
