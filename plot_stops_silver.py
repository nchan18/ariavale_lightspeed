import math
import matplotlib.pyplot as plt

# List of stops for Silver Line with latitude, longitude, and names
silver_line_stops = [
    (35.307083, -80.730644, "CRI Deck"),  # Stop #1
    (35.305833, -80.734444, "Duke Centennial Hall"),  # Stop #3
    (35.308056, -80.733611, "EPIC – South"),  # Stop #5
    (35.310278, -80.737222, "Athletics Complex – East"),  # Stop #6
    (35.31027778, -80.73277778, "Student Union – East"),  # Stop #8
    (35.30798734, -80.73035288, "Auxiliary Services"),  # Stop #9
    (35.31027778, -80.72666667, "Student Health – North"),  # Stop #11
    (35.30722222, -80.72527778, "Martin Hall"),  # Stop #12
    (35.312842, -80.728050, "Lot 6"),  # Stop #13
    (35.312249, -80.725944, "Lot 5A"),  # Stop #14
    (35.312849, -80.723064, "East Deck 2"),  # Stop #15
    (35.30739, -80.72931, "Fretwell – North"),  # Stop #16
    (35.305833, -80.728611, "Klein Hall"),  # Stop #17
    (35.308056, -80.731944, "Student Union – West"),  # Stop #18
    (35.314444, -80.727778, "Athletics Complex – West"),  # Stop #20
    (35.310833, -80.726111, "EPIC – North"),  # Stop #21
    (35.310277, -80.723611, "Grigg Hall"),  # Stop #22
    (35.316667, -80.722222, "Motorsports"),  # Stop #55
    (35.312222, -80.718611, "PORTAL")  # Stop #23
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

# Create a plot for the Silver Line
fig, ax = plt.subplots(figsize=(10, 8))

# Define color for Silver Line
route_color = "silver"

# Extract coordinates and names
lats = [stop[0] for stop in silver_line_stops]
lons = [stop[1] for stop in silver_line_stops]
names = [stop[2] for stop in silver_line_stops]

# Plot the points for the Silver Line, including the first stop at the end to complete the loop
looped_lats = lats + [lats[0]]  # Add the first latitude at the end
looped_lons = lons + [lons[0]]  # Add the first longitude at the end

# Plot the Silver Line route
ax.plot(looped_lons, looped_lats, marker='o', markersize=6, color=route_color, label="Silver Line")

# Annotate each point with its name
for i, stop in enumerate(silver_line_stops):
    ax.annotate(f'{names[i]}', (stop[1], stop[0]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

# Calculate and plot the distances between each consecutive stop
total_distance = 0
for i in range(1, len(silver_line_stops)):
    # Calculate the distance
    distance = calculate_distance((silver_line_stops[i-1][0], silver_line_stops[i-1][1]), (silver_line_stops[i][0], silver_line_stops[i][1]))
    total_distance += distance
    
    # Annotate the distance between consecutive stops
    mid_lat = (silver_line_stops[i-1][0] + silver_line_stops[i][0]) / 2
    mid_lon = (silver_line_stops[i-1][1] + silver_line_stops[i][1]) / 2
    ax.annotate(f'{distance:.2f} km', (mid_lon, mid_lat), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color="blue")

# Connect the last stop to the first stop to complete the loop (including the first stop's distance)
distance = calculate_distance((silver_line_stops[-1][0], silver_line_stops[-1][1]), (silver_line_stops[0][0], silver_line_stops[0][1]))
total_distance += distance

# Annotate the distance between the last and first stop (loop back)
mid_lat = (silver_line_stops[-1][0] + silver_line_stops[0][0]) / 2
mid_lon = (silver_line_stops[-1][1] + silver_line_stops[0][1]) / 2
ax.annotate(f'{distance:.2f} km', (mid_lon, mid_lat), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color="blue")

# Label the axes and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Silver Line Route with Stops and Distances')

# Set plot limits to focus on the region containing the stops
ax.set_xlim(min(lons) - 0.01, max(lons) + 0.01)
ax.set_ylim(min(lats) - 0.01, max(lats) + 0.01)

# Display the legend
ax.legend()

# Display the plot
plt.show()

# Output total distance for the looped route
print(f"Total distance for Silver Line loop: {total_distance:.2f} km")
