import math
import random
import matplotlib.pyplot as plt

# Define all bus stops with their IDs, names, latitudes, and longitudes
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

print(bus_stops)

stop_list = {}
route_name = None
route_stop_list = []

with open("../create_map/route_stops.txt", "r") as routes:
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

stops = {}
for route, stop_names in stop_list.items():
    stops[route] = [bus_stops[stop] for stop in stop_names if stop in bus_stops]

print(stops)

# Colors for routes
colors = {
    "Route Green": "green",
    "Silver": "silver",
    "Route Red": "red",
    "Route Gold": "gold",
    "Route Greek": "purple",
    "Shopping": "orange"
}

# Calculate distance function
def calculate_distance(coord1, coord2):
    R = 6371  # Earth radius in km
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# Simulated Annealing algorithm
def simulated_annealing(route_stops, initial_temperature=100, cooling_rate=0.995, max_iterations=1000):
    current_route = random.sample(route_stops, len(route_stops))  # Random initial solution
    current_distance = calculate_route_distance(current_route)
    temperature = initial_temperature

    best_route = current_route
    best_distance = current_distance

    for iteration in range(max_iterations):
        # Create a neighboring solution by swapping two stops
        new_route = current_route[:]
        i, j = random.sample(range(len(route_stops)), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        new_distance = calculate_route_distance(new_route)

        # Accept the new solution with a probability
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temperature):
            current_route = new_route
            current_distance = new_distance

            # Update the best solution found so far
            if current_distance < best_distance:
                best_route = current_route
                best_distance = current_distance

        # Reduce the temperature
        temperature *= cooling_rate

    return best_route

# Calculate total route distance
def calculate_route_distance(route):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += calculate_distance(route[i][1:], route[i+1][1:])
    return total_distance

# Optimize all routes using Simulated Annealing and plot them
fig, ax = plt.subplots(figsize=(15, 10))

for route, route_stops in stops.items():
    best_route = simulated_annealing(route_stops)
    
    # Duplicate first stop at the end to complete the loop
    closed_route = best_route + [best_route[0]]
    
    lats = [stop[1] for stop in closed_route]
    longs = [stop[2] for stop in closed_route]

    # Plot the route
    ax.plot(longs, lats, marker='o', label=route, color=colors.get(route, "blue"))
    
    # Add stop names as text
    for stop in closed_route:
        ax.text(stop[2], stop[1], stop[0], fontsize=9, ha='right', color=colors.get(route, "blue"))

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Optimized Bus Routes with Simulated Annealing")
ax.legend()

plt.show()
