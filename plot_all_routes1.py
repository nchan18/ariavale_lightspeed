import math
import folium

# Read bus stops from file and store them in a dictionary
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

# Read routes and their stops from file
stop_list = {}
with open("route_stops.txt", "r") as routes:
    for route in routes:
        if route.startswith("Route: "):
            route_name = route[len("Route: "):-1].strip()
        elif route.startswith("Stops: "):
            stop_string = route[len("Stops: "):-1].strip()
            stop_list[route_name] = stop_string.split(", ")

# Get stops associated with each route
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

valid_colors = {'green', 'silver', 'red', 'gold', 'purple', 'orange', 'blue'}

def calculate_distance(coord1, coord2):
    """Calculate distance between two lat/lon points using Haversine formula."""
    R = 6371  # Earth radius in km
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def find_nearest_neighbor_route(route_stops):
    """Rearrange stops to follow the nearest neighbor heuristic."""
    if not route_stops:
        return []

    unvisited = set(route_stops)
    ordered_route = [route_stops[0]]  # Start from the first stop
    unvisited.remove(route_stops[0])

    while unvisited:
        last_stop = ordered_route[-1]
        next_stop = min(unvisited, key=lambda stop: calculate_distance((last_stop[1], last_stop[2]), (stop[1], stop[2])))
        ordered_route.append(next_stop)
        unvisited.remove(next_stop)

    return ordered_route

# Initialize the map (using a central location for better zoom)
base_map = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

# Plot the routes on the map
for route, route_stops in stops.items():
    optimized_route = find_nearest_neighbor_route(route_stops)
    closed_route = optimized_route + [optimized_route[0]]  # Complete the loop

    # Plot each route
    for i in range(len(closed_route)-1):
        start_stop = closed_route[i]
        end_stop = closed_route[i+1]
        folium.PolyLine(
            locations=[(start_stop[1], start_stop[2]), (end_stop[1], end_stop[2])],
            color=colors.get(route, "blue"),
            weight=5,
            opacity=0.7
        ).add_to(base_map)

    # Add markers for each stop, ensuring color is valid
    for stop in closed_route:
        marker_color = colors.get(route, "blue")
        if marker_color not in valid_colors:
            marker_color = 'blue'  # Set to blue if the color is invalid
        folium.Marker(
            location=[stop[1], stop[2]],
            popup=stop[0],
            icon=folium.Icon(color=marker_color)
        ).add_to(base_map)

# Save the map as an HTML file with the new name
map_file = "optimized_bus_routes_map.html"
base_map.save(map_file)
print(f"Map has been saved to: {map_file}")
