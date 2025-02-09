import math
import matplotlib.pyplot as plt

#print all of the route names
def calculate_distance(coord1, coord2):
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers

def annotate(stop_list):
    for i, stop in enumerate(stop_list):
        ax.annotate(f'{stop[0]}', (stop[2], stop[1]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

bus_stops = {}
stop_list = {}
route_name = None
route_name_list = []
route_stop_list = []

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
with open("route_stops.txt", "r") as routes:
    for route in routes:
        if route.startswith("Route: "):
            route_name = route[len("Route: "):-1].strip()
            route_name_list.append(route_name)
        elif route.startswith("Stops: "):
            stop_string = route[len("Stops: "):-1].strip()
            route_stop_list = stop_string.split(", ")
            if route_name and route_stop_list: 
                stop_list[route_name] = route_stop_list
        elif route.startswith("----------------------------------------"):
            route_name = None
            route_stop_list = []
print(stop_list)

counter = 0
for route_name in route_name_list:
    print(f'{counter}: {route_name}')
    counter += 1

what_color_index = input("What color would you like the route to be? ")


stops = []
for stop in stop_list[route_name_list[int(what_color_index)]]:
        stops.append(bus_stops[stop])

fig, ax = plt.subplots(figsize=(10, 8))

# Define color for Gold Line
route_color = "black"

# Extract coordinates and names
lats = [stop[1] for stop in stops]
lons = [stop[2] for stop in stops]
names = [stop[0] for stop in stops]

# Plot the points for the Gold Line, including the first stop at the end to complete the loop
looped_lats = lats + [lats[0]]  # Add the first latitude at the end
looped_lons = lons + [lons[0]]  # Add the first longitude at the end

# Plot the Gold Line route
ax.plot(looped_lons, looped_lats, marker='o', markersize=6, color=route_color, label="Gold Line")

# Annotate each point with its name
for i, stop in enumerate(stops):
    ax.annotate(f'{names[i]}', (stop[1], stop[0]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

# Calculate and plot the distances between each consecutive stop
total_distance = 0
for i in range(1, len(stops)):
    # Calculate the distance
    distance = calculate_distance((stops[i-1][1], stops[i-1][2]), (stops[i][1], stops[i][2]))
    total_distance += distance
    annotate(stops)

# Connect the last stop to the first stop to complete the loop (including the first stop's distance)
distance = calculate_distance((stops[-1][1], stops[-1][2]), (stops[0][1], stops[0][2]))
total_distance += distance

annotate(stops)

# Label the axes and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title(f'{route_color} Line Route with Stops and Distances')

# Set plot limits to focus on the region containing the stops
ax.set_xlim(min(lons) - 0.01, max(lons) + 0.01)
ax.set_ylim(min(lats) - 0.01, max(lats) + 0.01)

# Display the legend
ax.legend()

# Display the plot
plt.show()

# Output total distance for the looped route
print(f"Total distance for {route_name_list[int(what_color_index)]} Line loop: {total_distance:.2f} km")
