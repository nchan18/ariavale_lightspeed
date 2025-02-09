import math
import matplotlib.pyplot as plt

# List of stops for Green Line with latitude, longitude, and names
green_line_stops = [
    (35.311946629, -80.733450671, "Light Rail"),  # Stop #42
    (35.31027778, -80.73611111, "Belk Hall"),  # Stop #43
    (35.308132323, -80.732772658, "Student Union – East"),  # Stop #8
    (35.30798734, -80.730352882, "Auxiliary Services"),  # Stop #9
    (35.30739, -80.72931, "Fretwell – South"),  # Stop #37
    (35.305, -80.72833333, "Cato Hall – South"),  # Stop #38
    (35.30361111, -80.72944444, "Robinson Hall – South"),  # Stop #39
    (35.311491571, -80.730662848, "Reese West"),  # Stop #44
    (35.31224722, -80.74166667, "Cone Deck"),  # Stop #45
    (35.31083333, -80.74138889, "Alumni Way – East"),  # Stop #49
    (35.30722222, -80.72527778, "South Village Deck"),  # Stop #46
    (35.31284, -80.74101, "Gage UA Center"),  # Stop #47
    (35.30333333, -80.72944444, "Robinson Hall North"),  # Stop #31
    (35.305, -80.72805556, "Cato Hall – North"),  # Stop #32
    (35.30739, -80.72931, "Fretwell – North"),  # Stop #16
    (35.31027778, -80.72666667, "Student Health – North"),  # Stop #11
    (35.311491571, -80.730662848, "FM/PPS"),  # Stop #41
    (35.31224722, -80.74166667, "North Deck")  # Stop #48
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

# Create a plot for the Green Line
fig, ax = plt.subplots(figsize=(10, 8))

# Define color for Green Line
route_color = "green"

# Extract coordinates and names
lats = [stop[0] for stop in green_line_stops]
lons = [stop[1] for stop in green_line_stops]
names = [stop[2] for stop in green_line_stops]

# Plot the points for the Green Line, including the first stop at the end to complete the loop
looped_lats = lats + [lats[0]]  # Add the first latitude at the end
looped_lons = lons + [lons[0]]  # Add the first longitude at the end

# Plot the Green Line route
ax.plot(looped_lons, looped_lats, marker='o', markersize=6, color=route_color, label="Green Line")

# Annotate each point with its name
for i, stop in enumerate(green_line_stops):
    ax.annotate(f'{names[i]}', (stop[1], stop[0]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

# Calculate and plot the distances between each consecutive stop
total_distance = 0
for i in range(1, len(green_line_stops)):
    # Calculate the distance
    distance = calculate_distance((green_line_stops[i-1][0], green_line_stops[i-1][1]), (green_line_stops[i][0], green_line_stops[i][1]))
    total_distance += distance
    
    # Annotate the distance between consecutive stops
    mid_lat = (green_line_stops[i-1][0] + green_line_stops[i][0]) / 2
    mid_lon = (green_line_stops[i-1][1] + green_line_stops[i][1]) / 2
    ax.annotate(f'{distance:.2f} km', (mid_lon, mid_lat), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color="blue")

# Connect the last stop to the first stop to complete the loop (including the first stop's distance)
distance = calculate_distance((green_line_stops[-1][0], green_line_stops[-1][1]), (green_line_stops[0][0], green_line_stops[0][1]))
total_distance += distance

# Annotate the distance between the last and first stop (loop back)
mid_lat = (green_line_stops[-1][0] + green_line_stops[0][0]) / 2
mid_lon = (green_line_stops[-1][1] + green_line_stops[0][1]) / 2
ax.annotate(f'{distance:.2f} km', (mid_lon, mid_lat), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color="blue")

# Label the axes and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Green Line Route with Stops and Distances')

# Set plot limits to focus on the region containing the stops
ax.set_xlim(min(lons) - 0.01, max(lons) + 0.01)
ax.set_ylim(min(lats) - 0.01, max(lats) + 0.01)

# Display the legend
ax.legend()

# Display the plot
plt.show()

# Output total distance for the looped route
print(f"Total distance for Green Line loop: {total_distance:.2f} km")
