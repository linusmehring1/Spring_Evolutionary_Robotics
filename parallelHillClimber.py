import copy
import os

from solution import SOLUTION
import constants as c


class PARALLEL_HILL_CLIMBER:
    def __init__(self, fitnessMode="A"):
        os.system("rm brain*.nndf 2>/dev/null")
        os.system("rm fitness*.txt 2>/dev/null")
        os.system("rm stats*.txt 2>/dev/null")
        self.fitnessMode = fitnessMode
        
        self.nextAvailableID = 0
        self.parents = {}
        
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for key in self.children:
            self.children[key].Mutate()

    def Evaluate(self, solutions):
        for key in solutions:
            solutions[key].Start_Simulation("DIRECT", self.fitnessMode)
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()

    def Select(self):
        for key in self.parents:
            # MAXIMIZE fitness: longer contiguous flight phase = better jump
            if self.parents[key].fitness < self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        print()
        for key in self.parents:
            print(self.parents[key].fitness, self.children[key].fitness)
        print()

    def Show_Best(self):
        bestKey = None
        bestFitness = -1000.0  # Start low, looking for highest (longest flight) fitness
        for key in self.parents:
            if self.parents[key].fitness > bestFitness:
                bestFitness = self.parents[key].fitness
                bestKey = key
        print(f"\n=== FITNESS MODE {self.fitnessMode} RESULTS ===")
        if self.fitnessMode == "A":
            print(f"Best fitness (longest flight): {bestFitness:.3f} timesteps")
        else:
            print(f"Best fitness (distance * flight): {bestFitness:.3f}")
        print(f"Longest flight: {self.parents[bestKey].longestFlight} timesteps")
        print(f"Horizontal distance: {self.parents[bestKey].horizontalDistance:.3f}")
        print(f"Max torso height: {self.parents[bestKey].maxHeight:.3f}\n")
        self.parents[bestKey].Start_Simulation("GUI", self.fitnessMode)
