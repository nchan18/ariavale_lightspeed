import math
import matplotlib.pyplot as plt
import gym
import numpy as np
from stable_baselines3 import PPO

# Load bus stop data
bus_stops = {}
with open("../create_map/stop_list.txt", "r") as stops:
    for stop in stops:
        lat_index = stop.find("Latitude")
        lon_index = stop.find("Longitude")
        if lat_index != -1 and lon_index != -1:
            lat_start = lat_index + len("Latitude: ")
            lon_start = lon_index + len("Longitude: ")
            name_start = stop.find("Name: ") + len("Name: ")
            bus_stops[stop[name_start:lat_index-2].strip()] = (
                stop[name_start:lat_index-2].strip(),
                float(stop[lat_start:stop.find(",", lat_start)].strip()),
                float(stop[lon_start:stop.find(",", lon_start)].strip())
            )

# Check if bus_stops dictionary is correctly populated
print(bus_stops)

# Load route stop data
stop_list = {}
route_name = None
route_stop_list = []

with open("route_stops.txt", "r") as routes:
    for route in routes:
        if route.startswith("Route: "):
            route_name = route[len("Route: "):-1].strip()
        elif route.startswith("Stops: "):
            stop_string = route[len("Stops: "):-1].strip()
            route_stop_list = stop_string.split(", ")
            stop_list[route_name] = route_stop_list
        elif route.startswith("----------------------------------------"):
            route_name = None
            route_stop_list = []

# Check if stop_list is populated correctly
print(stop_list)

# Create the environment class
class BusRouteEnv(gym.Env):
    def __init__(self, bus_stops, stop_list):
        super(BusRouteEnv, self).__init__()

        # Set up the bus stop data
        self.bus_stops = bus_stops
        self.stop_list = stop_list
        self.routes = list(stop_list.keys())
        
        # Initialize variables for state and action space
        self.action_space = gym.spaces.Discrete(len(self.routes))  # One action per route
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(2,))  # Placeholder for state

    def reset(self):
        # Initialize the environment at the start of each episode
        self.current_route = 0
        return np.array([0, 0])

    def step(self, action):
        # Perform one step in the environment based on the selected action (route)
        reward = 0
        route_name = self.routes[action]
        
        # Calculate reward for the selected route (this is a placeholder, implement the real logic)
        reward = -len(self.stop_list[route_name])  # Assume fewer stops = better reward for simplicity
        
        done = False  # Keep the episode running indefinitely for now
        info = {}  # You can add any additional info if needed
        
        return np.array([0, 0]), reward, done, info

    def render(self):
        # Render the bus route for visualization (optional)
        plt.figure(figsize=(10, 6))
        for route, stops in self.stop_list.items():
            latitudes = []
            longitudes = []
            for stop in stops:
                latitudes.append(self.bus_stops[stop][1])
                longitudes.append(self.bus_stops[stop][2])
            
            plt.plot(longitudes, latitudes, marker='o', label=route)

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Bus Routes')
        plt.legend()
        plt.show()

# Instantiate the environment
env = BusRouteEnv(bus_stops, stop_list)

# Set up the PPO model
model = PPO("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=10000)

# Save the trained model
model.save("ppo_bus_route_optimizer")

# Test the trained model
obs = env.reset()
for _ in range(10):  # Run for 10 steps
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()  # Optionally render the route on each step

    if done:
        break
