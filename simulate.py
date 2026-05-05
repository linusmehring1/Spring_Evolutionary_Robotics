import sys
import constants as c
from simulation import SIMULATION


if __name__ == "__main__":
    directOrGUI = sys.argv[1]
    solutionID = sys.argv[2]
    fitnessMode = sys.argv[3] if len(sys.argv) > 3 else "A"
    simulation = SIMULATION(directOrGUI, solutionID, fitnessMode)
    simulation.Run()
    simulation.Get_Fitness(solutionID)

