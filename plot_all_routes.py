import math
import matplotlib.pyplot as plt

# Define all bus stops with their IDs, names, latitudes, and longitudes

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

print(bus_stops)

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
def calculate_distance(coord1, coord2):
    R = 6371  # Earth radius in km
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# Plot setup
fig, ax = plt.subplots(figsize=(15, 10))

for route, route_stops in stops.items():
    # Duplicate first stop at end to complete loop
    closed_route = route_stops + [route_stops[0]]
    
    lats = [stop[1] for stop in closed_route]
    longs = [stop[2] for stop in closed_route]

    # Plot the route
    ax.plot(longs, lats, marker='o', label=route, color=colors.get(route, "blue"))
    
    # Add stop names as text
    for stop in closed_route:
        ax.text(stop[2], stop[1], stop[0], fontsize=9, ha='right', color=colors.get(route, "blue"))

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Bus Routes with Stop Names")
ax.legend()

plt.show()