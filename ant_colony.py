import math
import random
import matplotlib.pyplot as plt

# Parse bus stops data from 'stop_list.txt'
bus_stops = {}
with open("stop_list.txt", "r") as stops:
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

# Parse routes and stops data from 'route_stops.txt'
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

# Generate the stop data for each route
stops = {}
for route, stop_names in stop_list.items():
    stops[route] = [bus_stops[stop] for stop in stop_names if stop in bus_stops]

# Calculate the distance between two coordinates using Haversine formula
def calculate_distance(coord1, coord2):
    R = 6371  # Earth radius in km
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Ant Colony Optimization class
class ACO:
    def __init__(self, stops, n_ants=10, n_best=3, n_iterations=100, decay=0.95):
        self.stops = stops
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.distance = {}
        self.pheromone = {}

        # Calculate distances between each pair of stops and initialize pheromone levels
        for stop1, stop2 in zip(stops.keys(), list(stops.keys())[1:]):
            coord1 = (stops[stop1][1], stops[stop1][2])
            coord2 = (stops[stop2][1], stops[stop2][2])
            self.distance[(stop1, stop2)] = calculate_distance(coord1, coord2)
            self.distance[(stop2, stop1)] = self.distance[(stop1, stop2)]
            self.pheromone[(stop1, stop2)] = 1.0
            self.pheromone[(stop2, stop1)] = 1.0

    def run(self):
        best_route = None
        best_distance = float('inf')

        for i in range(self.n_iterations):
            all_routes = self.generate_routes()
            self.update_pheromone(all_routes)
            shortest_route = min(all_routes, key=lambda x: x[1])
            if shortest_route[1] < best_distance:
                best_distance = shortest_route[1]
                best_route = shortest_route

            print(f"Iteration {i+1}/{self.n_iterations}, Best Distance: {best_distance}")

        return best_route

    def generate_routes(self):
        all_routes = []
        for _ in range(self.n_ants):
            route = self.generate_route()
            distance = self.calculate_route_distance(route)
            all_routes.append((route, distance))
        return all_routes

    def generate_route(self):
        route = random.sample(list(self.stops.keys()), len(self.stops))
        return route

    def calculate_route_distance(self, route):
        distance = 0
        for i in range(len(route) - 1):
            stop1 = route[i]
            stop2 = route[i + 1]
            distance += self.distance[(stop1, stop2)]
        return distance

    def update_pheromone(self, all_routes):
        for route, _ in all_routes:
            for i in range(len(route) - 1):
                stop1 = route[i]
                stop2 = route[i + 1]
                self.pheromone[(stop1, stop2)] += 1.0 / self.distance[(stop1, stop2)]
                self.pheromone[(stop2, stop1)] += 1.0 / self.distance[(stop2, stop1)]

        # Decay pheromone levels
        for key in self.pheromone.keys():
            self.pheromone[key] *= self.decay

# Run Ant Colony Optimization to find the best route
aco = ACO(stops, n_ants=10, n_best=3, n_iterations=100, decay=0.95)
best_route, best_distance = aco.run()

# Plot the best route
print(f"Best route: {best_route}")
print(f"Best distance: {best_distance}")

# Extract coordinates for plotting
lats = [stops[stop][1] for stop in best_route]
longs = [stops[stop][2] for stop in best_route]

# Plot the route
fig, ax = plt.subplots(figsize=(15, 10))
ax.plot(longs, lats, marker='o', label="Best Route", color="green")

# Add stop names as text
for stop in best_route:
    ax.text(stops[stop][2], stops[stop][1], stop, fontsize=9, ha='right', color="green")

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Optimal Bus Route with Stop Names")
ax.legend()

plt.show()
