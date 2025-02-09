import math
import matplotlib.pyplot as plt

# List of stops for Greek Village Service with latitude, longitude, and names
greek_village_stops = [
    (35.3081, -80.7311, "Student Union West"),  # Stop #Student Union West
    (35.3069, -80.7306, "Greek Village 1"),  # Stop #Greek Village 1
    (35.3059, -80.7297, "Greek Village 8"),  # Stop #Greek Village 8
    (35.3078, -80.7229, "Klein Hall"),  # Stop #Klein Hall
    (35.3062, -80.7240, "Greek Village 4"),  # Stop #Greek Village 4
    (35.3081, -80.7311, "Student Union West")  # Stop #Student Union West (loop)
]

# Function to calculate distance between two coordinates (in km)
def calculate_distance(coord1, coord2):
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers

# Create a plot for the Greek Village Service
fig, ax = plt.subplots(figsize=(10, 8))

# Define color for Greek Village Service
route_color = "green"

# Extract coordinates and names
lats = [stop[0] for stop in greek_village_stops]
lons = [stop[1] for stop in greek_village_stops]
names = [stop[2] for stop in greek_village_stops]

# Plot the points for the Greek Village Service route, including the first stop at the end to complete the loop
looped_lats = lats + [lats[0]]  # Add the first latitude at the end
looped_lons = lons + [lons[0]]  # Add the first longitude at the end

# Plot the Greek Village Service route
ax.plot(looped_lons, looped_lats, marker='o', markersize=6, color=route_color, label="Greek Village Service")

# Annotate each point with its name
for i, stop in enumerate(greek_village_stops):
    ax.annotate(f'{names[i]}', (stop[1], stop[0]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

# Calculate and plot the distances between each consecutive stop
total_distance = 0
for i in range(1, len(greek_village_stops)):
    # Calculate the distance
    distance = calculate_distance((greek_village_stops[i-1][0], greek_village_stops[i-1][1]), (greek_village_stops[i][0], greek_village_stops[i][1]))
    total_distance += distance
    
    # Annotate the distance between consecutive stops
    mid_lat = (greek_village_stops[i-1][0] + greek_village_stops[i][0]) / 2
    mid_lon = (greek_village_stops[i-1][1] + greek_village_stops[i][1]) / 2
    ax.annotate(f'{distance:.2f} km', (mid_lon, mid_lat), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color="blue")

# Connect the last stop to the first stop to complete the loop (including the first stop's distance)
distance = calculate_distance((greek_village_stops[-1][0], greek_village_stops[-1][1]), (greek_village_stops[0][0], greek_village_stops[0][1]))
total_distance += distance

# Annotate the distance between the last and first stop (loop back)
mid_lat = (greek_village_stops[-1][0] + greek_village_stops[0][0]) / 2
mid_lon = (greek_village_stops[-1][1] + greek_village_stops[0][1]) / 2
ax.annotate(f'{distance:.2f} km', (mid_lon, mid_lat), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color="blue")

# Label the axes and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Greek Village Service Route with Stops and Distances')

# Set plot limits to focus on the region containing the stops
ax.set_xlim(min(lons) - 0.01, max(lons) + 0.01)
ax.set_ylim(min(lats) - 0.01, max(lats) + 0.01)

# Display the legend
ax.legend()

# Display the plot
plt.show()

# Output total distance for the looped route
print(f"Total distance for Greek Village Service loop: {total_distance:.2f} km")
