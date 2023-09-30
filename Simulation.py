import numpy as np
from Vehicle import Vehicle
from MPCController import MPCController
import matplotlib.pyplot as plt

class Simulation:
  def __init__(self, vehicle, path, dt = 0.1, simulation_time = 100):
    self.vehicle = vehicle
    self.path = path
    self.dt = dt
    self.simulation_time = simulation_time
    self.mpc = MPCController(self.vehicle, path, self.dt, prediction_horizon=10)
    self.x_hist = []
    self.y_hist = []

  def run(self):
    for t in np.arange(0, self.simulation_time, self.dt):
      controls = self.mpc.optimize(self.vehicle)
      print(controls)
      if (controls[0] > 0.2):
        controls[0] = 0.2
      if (controls[0] < -0.2):
        controls[0] = -0.2

      if (controls[1] > 5):
        controls[1] = 5
      if (controls[1] < -3):
        controls[1] = -3
      self.vehicle.move(controls[0], controls[1], self.dt)

      if self.vehicle.x >= self.path[-1][0]:
        break
      
      print(f"Time step:{t}")
      print(f"X: {self.vehicle.x}, Y:{self.vehicle.y}, Theta={self.vehicle.theta}, Vel:{self.vehicle.v}\n")
      self.x_hist.append(self.vehicle.x)
      self.y_hist.append(self.vehicle.y)
    
    plt.figure(figsize=(10, 6))
    plt.plot(self.x_hist, self.y_hist, label="Vehicle Path", marker='o')
    plt.plot(*zip(*self.path), color='red', label="Reference Path", linestyle='--')
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Vehicle Path Over Time")
    plt.grid()
    plt.legend()
    plt.show()

