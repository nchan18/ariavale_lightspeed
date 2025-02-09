import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, LineString

# Sample bus stop coordinates (replace with actual data)
bus_stops = [
    (35.308106119, -80.732820822),  # Example stop 1
    (35.308132323, -80.732772658),  # Example stop 2
    (35.30813611, -80.73277778),    # Example stop 3
    (35.30805556, -80.73277778),    # Example stop 4
    (35.30935, -80.74416667),       # Example stop 5
]

# Create a GeoDataFrame for bus stops
bus_stop_points = [Point(lon, lat) for lat, lon in bus_stops]
gdf_stops = gpd.GeoDataFrame(geometry=bus_stop_points)

# Create a GeoDataFrame for the route (a line connecting all bus stops)
route = LineString(bus_stop_points)
gdf_route = gpd.GeoDataFrame(geometry=[route])

# Create the plot
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the route as a line
gdf_route.plot(ax=ax, color='blue', linewidth=2)

# Plot the bus stops as points
gdf_stops.plot(ax=ax, color='red', marker='o', markersize=50)

# Label the bus stops
for idx, stop in enumerate(bus_stops):
    ax.text(stop[1], stop[0], f"Stop {idx+1}", fontsize=12, ha='right')

# Customize the plot
ax.set_title('Bus Route and Stops')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.grid(True)

# Show the plot
plt.show()
