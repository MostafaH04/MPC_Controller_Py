import numpy as np
from scipy.optimize import minimize
from Vehicle import Vehicle

class MPCController:
  def __init__(self, vehicle, path, dt, prediction_horizon):
    self.car = vehicle
    self.path = path
    self.dt = dt
    self.prediction_horizon = prediction_horizon

  def cost_function(self, controls):
    total_cost = 0.0

    minVal = 999999999999
    minPos = 0
    for i in range(len(self.path)):
      cost = (self.car.x - self.path[i][0]) ** 2 + (self.car.y - self.path[i][1]) ** 2
      if cost < minVal:
        minVal = cost
        minPos = i
    path = self.path[minPos:]

    # print(path)


    length = self.car.vehicle_length
    x = self.car.x
    y = self.car.y
    theta = self.car.theta
    v = self.car.v
    future_car = Vehicle(length, x, y, theta, v)


    for i in range(0, min(self.prediction_horizon,len(path))):
      future_controls = [controls[i*2], controls[i*2+1]]
      if (future_controls[0] > 0.2):
        future_controls[0] = 0.2
      if (future_controls[0] < -0.2):
        future_controls[0] = -0.2

      if (future_controls[1] > 5):
        future_controls[1] = 5
      if (future_controls[1] < -3):
        future_controls[1] = -3

      future_car.move(future_controls[0],future_controls[1], self.dt)

      # print(future_controls)
      # print(future_car.x, future_car.y)
      # input()
      pos_err = (future_car.x - path[i][0]) ** 2
      pos_err += (future_car.y - path[i][1]) ** 2
      # print(future_controls)
      # print()
      # input()
      control_eff = future_controls[0] ** 2 + future_controls[1] ** 2

      total_cost += pos_err + control_eff
    # print(total_cost)
    return total_cost
  
  def optimize(self, vehicle):
    self.car = vehicle
    init_controls = np.zeros((self.prediction_horizon,2))

    control_bounds = [(-0.5,0.5)] * self.prediction_horizon
    # print(control_bounds)

    result = minimize(self.cost_function, init_controls)
    return result.x