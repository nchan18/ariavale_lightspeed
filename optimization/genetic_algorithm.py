import random
import math
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

# Colors for routes
colors = {
    "Route Green": "green",
    "Silver": "silver",
    "Route Red": "red",
    "Route Gold": "gold",
    "Route Greek": "purple",
    "Shopping": "orange"
}

def calculate_distance(coord1, coord2):
    """Calculate the Haversine distance between two coordinates."""
    R = 6371  # Earth radius in km
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def calculate_route_distance(route):
    """Calculate the total distance of a given route."""
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += calculate_distance((route[i][1], route[i][2]), (route[i+1][1], route[i+1][2]))
    return total_distance

def create_initial_population(route_stops, population_size=100):
    """Create the initial population of routes by randomly shuffling the stops."""
    population = []
    for _ in range(population_size):
        random_route = random.sample(route_stops, len(route_stops))
        population.append(random_route)
    return population

def select_parents(population, fitness_scores):
    """Select two parents based on fitness scores (lower distance is better)."""
    total_fitness = sum(fitness_scores)
    selection_prob = [1 - (score / total_fitness) for score in fitness_scores]
    selected_parents = random.choices(population, weights=selection_prob, k=2)
    return selected_parents

def crossover(parent1, parent2):
    """Perform a crossover between two parents to produce a child route."""
    split_point = random.randint(1, len(parent1) - 2)
    child = parent1[:split_point] + [stop for stop in parent2 if stop not in parent1[:split_point]]
    return child

def mutate(route, mutation_rate=0.05):
    """Perform a mutation by swapping two random stops in the route."""
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

def genetic_algorithm(route_stops, generations=100, population_size=100, mutation_rate=0.05):
    """Run the Genetic Algorithm to find an optimized bus route."""
    population = create_initial_population(route_stops, population_size)
    best_route = None
    best_distance = float('inf')

    for generation in range(generations):
        fitness_scores = [calculate_route_distance(route) for route in population]
        new_population = []

        for _ in range(population_size // 2):
            parents = select_parents(population, fitness_scores)
            child1 = crossover(parents[0], parents[1])
            child2 = crossover(parents[1], parents[0])

            new_population.append(mutate(child1, mutation_rate))
            new_population.append(mutate(child2, mutation_rate))

        population = new_population

        # Track the best solution
        best_generation_route = min(zip(population, fitness_scores), key=lambda x: x[1])
        if best_generation_route[1] < best_distance:
            best_route, best_distance = best_generation_route

    return best_route

# Plot setup
fig, ax = plt.subplots(figsize=(15, 10))

# Apply Genetic Algorithm to optimize the route for each bus route
for route, route_stops in stops.items():
    # Get the optimized route using the Genetic Algorithm
    optimized_route = genetic_algorithm(route_stops)
    
    # Duplicate first stop at end to complete loop
    closed_route = optimized_route + [optimized_route[0]]

    lats = [stop[1] for stop in closed_route]
    longs = [stop[2] for stop in closed_route]

    # Plot the route
    ax.plot(longs, lats, marker='o', label=route, color=colors.get(route, "blue"))
    
    # Add stop names as text
    for stop in closed_route:
        ax.text(stop[2], stop[1], stop[0], fontsize=9, ha='right', color=colors.get(route, "blue"))

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Optimized Bus Routes with Stop Names (Genetic Algorithm)")
ax.legend()

plt.show()
