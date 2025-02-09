import math
import matplotlib.pyplot as plt

# List of stops for Shopping Shuttle Service with latitude, longitude, and names
shopping_shuttle_stops = [
    (35.3031, -80.7329, "Levine Hall"),  # Stop #Levine Hall
    (35.3020, -80.7342, "Hunt Hall"),  # Stop #Hunt Hall
    (35.3061, -80.7370, "Wallis Hall East"),  # Stop #Wallis Hall East
    (35.3077, -80.7288, "Martin Hall"),  # Stop #Martin Hall
    (35.3092, -80.7283, "Patel Brothers"),  # Stop #Patel Brothers
    (35.3101, -80.7275, "Target"),  # Stop #Target
    (35.3112, -80.7260, "Harris Teeter"),  # Stop #Harris Teeter
    (35.3031, -80.7329, "Levine Hall")  # Stop #Levine Hall (loop)
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

# Create a plot for the Shopping Shuttle Service
fig, ax = plt.subplots(figsize=(10, 8))

# Define color for Shopping Shuttle Service
route_color = "purple"

# Extract coordinates and names
lats = [stop[0] for stop in shopping_shuttle_stops]
lons = [stop[1] for stop in shopping_shuttle_stops]
names = [stop[2] for stop in shopping_shuttle_stops]

# Plot the points for the Shopping Shuttle Service route, including the first stop at the end to complete the loop
looped_lats = lats + [lats[0]]  # Add the first latitude at the end
looped_lons = lons + [lons[0]]  # Add the first longitude at the end

# Plot the Shopping Shuttle Service route
ax.plot(looped_lons, looped_lats, marker='o', markersize=6, color=route_color, label="Shopping Shuttle Service")

# Annotate each point with its name
for i, stop in enumerate(shopping_shuttle_stops):
    ax.annotate(f'{names[i]}', (stop[1], stop[0]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

# Calculate and plot the distances between each consecutive stop
total_distance = 0
for i in range(1, len(shopping_shuttle_stops)):
    # Calculate the distance
    distance = calculate_distance((shopping_shuttle_stops[i-1][0], shopping_shuttle_stops[i-1][1]), (shopping_shuttle_stops[i][0], shopping_shuttle_stops[i][1]))
    total_distance += distance
    
    # Annotate the distance between consecutive stops
    mid_lat = (shopping_shuttle_stops[i-1][0] + shopping_shuttle_stops[i][0]) / 2
    mid_lon = (shopping_shuttle_stops[i-1][1] + shopping_shuttle_stops[i][1]) / 2
    ax.annotate(f'{distance:.2f} km', (mid_lon, mid_lat), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color="blue")

# Connect the last stop to the first stop to complete the loop (including the first stop's distance)
distance = calculate_distance((shopping_shuttle_stops[-1][0], shopping_shuttle_stops[-1][1]), (shopping_shuttle_stops[0][0], shopping_shuttle_stops[0][1]))
total_distance += distance

# Annotate the distance between the last and first stop (loop back)
mid_lat = (shopping_shuttle_stops[-1][0] + shopping_shuttle_stops[0][0]) / 2
mid_lon = (shopping_shuttle_stops[-1][1] + shopping_shuttle_stops[0][1]) / 2
ax.annotate(f'{distance:.2f} km', (mid_lon, mid_lat), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color="blue")

# Label the axes and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Shopping Shuttle Service Route with Stops and Distances')

# Set plot limits to focus on the region containing the stops
ax.set_xlim(min(lons) - 0.01, max(lons) + 0.01)
ax.set_ylim(min(lats) - 0.01, max(lats) + 0.01)

# Display the legend
ax.legend()

# Display the plot
plt.show()

# Output total distance for the looped route
print(f"Total distance for Shopping Shuttle Service loop: {total_distance:.2f} km")
