import time
import math
import random
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
import threading


class DroneState(Enum):
    IDLE = "IDLE"
    FLYING = "FLYING"
    RETURNING = "RETURNING"


class Drone:
    def __init__(self, name, max_battery=100):
        self.name = name
        self.battery = max_battery
        self.state = DroneState.IDLE
        self.position = np.array([0.0, 0.0, 0.0])  # x, y, z
        self.waypoints = []
        self.obstacles = []
        self.telemetry = {}

    def fly_to(self, waypoint):
        if self.battery <= 0:
            print(f"{self.name}: Battery empty!")
            self.state = DroneState.IDLE
            return
        if self.state == DroneState.FLYING:
            print(f"{self.name}: Already flying!")
            return

        self.state = DroneState.FLYING
        self.waypoints.append(waypoint)
        self.calculate_flight_path(waypoint)

    def calculate_flight_path(self, waypoint):
        print(f"{self.name}: Flying to {waypoint}.")
        while not np.array_equal(self.position, waypoint):
            self.update_position(waypoint)
            print(f"{self.name}: Position {self.position}, Battery {self.battery}%")
            if self.battery <= 0:
                print(f"{self.name}: Battery empty!")
                self.state = DroneState.IDLE
                break
            time.sleep(1)

        if self.battery > 0:
            print(f"{self.name}: Arrived at {waypoint}.")    
            self.state = DroneState.IDLE

    def update_position(self, waypoint):
        direction = waypoint - self.position
        distance = np.linalg.norm(direction)
        if distance == 0:
            return

        step = min(distance, self.battery * 0.1)
        self.position += (direction / distance) * step
        self.battery -= step * 0.1

    def return_home(self):
        if self.state == DroneState.FLYING:
            print(f"{self.name}: Returning home.")
            self.fly_to(np.array([0.0, 0.0, 0.0]))
        else:
            print(f"{self.name} is not flying.")

    def add_obstacle(self, obstacle):
        print(f"{self.name}: Obstacle detected at {obstacle}.")
        self.obstacles.append(obstacle)
        self.avoid_obstacle(obstacle)

    def avoid_obstacle(self, obstacle):
        print(f"{self.name}: Calculating avoidance path around {obstacle}.")
        new_waypoint = self.position + np.array([1.0, 1.0, 0.0])  # Dummy avoidance strategy
        self.fly_to(new_waypoint)

    def get_telemetry(self):
        self.telemetry['position'] = self.position
        self.telemetry['battery'] = self.battery
        self.telemetry['state'] = self.state
        print(f"{self.name}: Telemetry: {self.telemetry}")
        

class DroneFleet:
    def __init__(self):
        self.drones = []
        
    def add_drone(self, drone):
        self.drones.append(drone)
        print(f"Added drone: {drone.name}")

    def command_drones(self, waypoint):
        for drone in self.drones:
            drone.fly_to(waypoint)

    def get_fleet_telemetry(self):
        for drone in self.drones:
            drone.get_telemetry()

            
# Simulation of drone operations
if __name__ == "__main__":
    fleet = DroneFleet()
    drone1 = Drone("Drone1")
    drone2 = Drone("Drone2")
    
    fleet.add_drone(drone1)
    fleet.add_drone(drone2)

    time.sleep(2)

    fleet.command_drones(np.array([10.0, 10.0, 0.0]))
    
    # Simulate adding obstacles during flight
    for i in range(3):
        time.sleep(5)
        obstacle = np.array([random.uniform(5, 15), random.uniform(5, 15), 0.0])
        drone1.add_obstacle(obstacle)

    time.sleep(5)
    fleet.get_fleet_telemetry()

    drone1.return_home()
    drone2.return_home()
    
    time.sleep(5)
    fleet.get_fleet_telemetry()


# Visualization of drone path
def plot_path(drone):
    plt.plot(drone.position[0], drone.position[1], 'ro', label=drone.name)
    plt.xlim(-5, 15)
    plt.ylim(-5, 15)
    plt.title('Drone Path')
    plt.xlabel('X position')
    plt.ylabel('Y position')
    plt.legend()
    plt.grid()
    plt.show()


# Create a separate thread for plotting
def plot_thread(drone):
    while drone.state != DroneState.IDLE:
        time.sleep(1)
    plot_path(drone)


if __name__ == "__main__":
    plot_thread(drone1)
    plot_thread(drone2)