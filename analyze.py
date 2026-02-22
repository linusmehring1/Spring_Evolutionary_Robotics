import numpy
import matplotlib.pyplot

PLOT_MODE = "motor_vectors"  # "motor_vectors" or "sensors"

if PLOT_MODE == "sensors":
    backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
    frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")
    print(backLegSensorValues)
    print(frontLegSensorValues)
    matplotlib.pyplot.plot(backLegSensorValues, label="BackLeg", linewidth=3)
    matplotlib.pyplot.plot(frontLegSensorValues, label="FrontLeg")
elif PLOT_MODE == "motor_vectors":
    backLegMotorValues = numpy.load("data/backLegMotorValues.npy")
    frontLegMotorValues = numpy.load("data/frontLegMotorValues.npy")
    print(backLegMotorValues)
    print(frontLegMotorValues)
    matplotlib.pyplot.plot(backLegMotorValues, label="BackLeg Motor", linewidth=3)
    matplotlib.pyplot.plot(frontLegMotorValues, label="FrontLeg Motor")
else:
    raise ValueError(f"Unknown PLOT_MODE: {PLOT_MODE}")

matplotlib.pyplot.legend()
matplotlib.pyplot.show()
