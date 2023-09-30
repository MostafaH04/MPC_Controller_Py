from Simulation import Simulation
from Vehicle import Vehicle
import numpy as np

# Car instance
car = Vehicle()

# path
path = [(0,1), (1, 1), (2, 1), (3, 1), (4, 1), (5,1)]
for i in range(6,100):
  path.append((i, 1))
# Simulation Instance
sim = Simulation(car, path)

sim.run()


