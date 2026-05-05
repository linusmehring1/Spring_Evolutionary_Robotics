import sys

from parallelHillClimber import PARALLEL_HILL_CLIMBER

fitnessMode = sys.argv[1] if len(sys.argv) > 1 else "A"
if fitnessMode not in ["A", "B"]:
	raise ValueError("Fitness mode must be 'A' or 'B'")

phc = PARALLEL_HILL_CLIMBER(fitnessMode)
phc.Evolve()
phc.Show_Best()
