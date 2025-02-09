import math
import matplotlib.pyplot as plt

# List of stops for Gold Line with latitude, longitude, and names
gold_line_stops = [
    (35.3053, -80.7308, "Wallis Hall"),  # Stop #34
    (35.3074, -80.7322, "Student Health East"),  # Stop #35
    (35.3122, -80.7259, "Fretwell South"),  # Stop #37
    (35.30739, -80.72931, "Cato Hall South"),  # Stop #38
    (35.3065, -80.7287, "Robinson Hall South"),  # Stop #39
    (35.3102, -80.7350, "Levine Hall"),  # Stop #40
    (35.3156, -80.7318, "Hunt Hall"),  # Stop #24
    (35.3152, -80.7344, "Alumni Way West"),  # Stop #56
    (35.3134, -80.7350, "Reese East"),  # Stop #30
    (35.3100, -80.7290, "Robinson Hall North"),  # Stop #31
    (35.3074, -80.7286, "Cato Hall North"),  # Stop #32
    (35.3071, -80.7256, "Fretwell North"),  # Stop #16
    (35.3078, -80.7229, "Klein Hall"),  # Stop #17
    (35.3081, -80.7311, "Student Union West"),  # Stop #18
    (35.3091, -80.7340, "Student Union Deck")  # Stop #33
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

# Create a plot for the Gold Line
fig, ax = plt.subplots(figsize=(10, 8))

# Define color for Gold Line
route_color = "gold"

# Extract coordinates and names
lats = [stop[0] for stop in gold_line_stops]
lons = [stop[1] for stop in gold_line_stops]
names = [stop[2] for stop in gold_line_stops]

# Plot the points for the Gold Line, including the first stop at the end to complete the loop
looped_lats = lats + [lats[0]]  # Add the first latitude at the end
looped_lons = lons + [lons[0]]  # Add the first longitude at the end

# Plot the Gold Line route
ax.plot(looped_lons, looped_lats, marker='o', markersize=6, color=route_color, label="Gold Line")

# Annotate each point with its name
for i, stop in enumerate(gold_line_stops):
    ax.annotate(f'{names[i]}', (stop[1], stop[0]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

# Calculate and plot the distances between each consecutive stop
total_distance = 0
for i in range(1, len(gold_line_stops)):
    # Calculate the distance
    distance = calculate_distance((gold_line_stops[i-1][0], gold_line_stops[i-1][1]), (gold_line_stops[i][0], gold_line_stops[i][1]))
    total_distance += distance
    
    # Annotate the distance between consecutive stops
    mid_lat = (gold_line_stops[i-1][0] + gold_line_stops[i][0]) / 2
    mid_lon = (gold_line_stops[i-1][1] + gold_line_stops[i][1]) / 2
    ax.annotate(f'{distance:.2f} km', (mid_lon, mid_lat), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color="blue")

# Connect the last stop to the first stop to complete the loop (including the first stop's distance)
distance = calculate_distance((gold_line_stops[-1][0], gold_line_stops[-1][1]), (gold_line_stops[0][0], gold_line_stops[0][1]))
total_distance += distance

# Annotate the distance between the last and first stop (loop back)
mid_lat = (gold_line_stops[-1][0] + gold_line_stops[0][0]) / 2
mid_lon = (gold_line_stops[-1][1] + gold_line_stops[0][1]) / 2
ax.annotate(f'{distance:.2f} km', (mid_lon, mid_lat), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color="blue")

# Label the axes and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Gold Line Route with Stops and Distances')

# Set plot limits to focus on the region containing the stops
ax.set_xlim(min(lons) - 0.01, max(lons) + 0.01)
ax.set_ylim(min(lats) - 0.01, max(lats) + 0.01)

# Display the legend
ax.legend()

# Display the plot
plt.show()

# Output total distance for the looped route
print(f"Total distance for Gold Line loop: {total_distance:.2f} km")
