import numpy as np

class Vehicle:
  def __init__(self, vehicle_len = 2.0, x = 0.0, y = 0.0, theta = 0.0, v = 0):
    self.vehicle_length = vehicle_len
    self.x = x
    self.y = y
    self.theta = theta
    self.v = v
  
  def move(self, steerAngle, accel, dt):
    self.x += self.v * dt * np.cos(self.theta)
    self.y += self.v * dt * np.sin(self.theta)
    self.theta += (self.v / self.vehicle_length) * np.tan(steerAngle) * dt
    self.v += accel * dt
  