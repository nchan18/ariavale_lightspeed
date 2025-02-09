import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx

place_name = 'University of North Carolina at Charlotte'
area = ox.geocode_to_gdf(place_name)

area.columns = [col[:10] for col in area.columns]

area.to_file("uncc_boundary.shp")

# Set the CRS to a suitable projected CRS (e.g., UTM zone 17N)
# area = area.to_crs(epsg=32617)

# Create a buffered boundary that is slightly larger
buffered_area = area.buffer(0.001)  # Buffer distance in meters

# Ensure the buffered area has the same CRS
buffered_area = gpd.GeoDataFrame(geometry=buffered_area, crs=area.crs)

# Get the road network within the buffered boundary
G = ox.graph_from_polygon(buffered_area.unary_union, network_type='all')
Gn = nx.MultiDiGraph()

# Convert the road network to a GeoDataFrame
nodes, edges = ox.graph_to_gdfs(G)

# Remove edges that are sidewalks
edges = edges[edges['highway'] != 'footway']

# Plot the stops from route_stops.txt
stops_lat = []
stops_lon = []
with open("route_stops.txt", "r") as stops:
    for stop in stops:
        lat_index = stop.find("Latitude")
        lon_index = stop.find("Longitude")
        if lat_index != -1 and lon_index != -1:
            lat_start = lat_index + len("Latitude: ")
            lon_start = lon_index + len("Longitude: ")
            stops_lat.append(float(stop[lat_start:stop.find(",", lat_start)].strip()))
            stops_lon.append(float(stop[lon_start:stop.find(",", lon_start)].strip()))

print(stops_lat)
print(stops_lon)
new_nodes = None
new_edges = None

# Add the stops as nodes to the graph
stop_nodes = []
for i in range(len(stops_lat)):
    stop_node = ox.nearest_nodes(G, X=stops_lon[i], Y=stops_lat[i])
    stop_nodes.append(stop_node)
    Gn.add_node(i, x=stops_lon[i], y=stops_lat[i])  # Use integer IDs for stops
    Gn.add_edge(stop_node, i, length=0)  # Add zero-length edge to connect stop to the nearest node

# find the shortest distance between every single stop and connect the stops with the shortest distance
for i in range(len(stop_nodes)):
    for j in range(i+1, len(stop_nodes)):
        shortest_path = nx.shortest_path(G, source=stop_nodes[i], target=stop_nodes[j], weight='length')
        for k in range(len(shortest_path) - 1):
            Gn.add_edge(shortest_path[k], shortest_path[k+1], length=0)
    

#plot gn
fig, ax = plt.subplots()
area.plot(ax=ax, facecolor='none', edgecolor='black', label='Original Boundary')
gpd.GeoSeries(buffered_area.geometry).plot(ax=ax, facecolor='none', edgecolor='blue', linestyle='--', label='Buffered Boundary')
edges.plot(ax=ax, linewidth=1, edgecolor='red', label='Roads')

# fig, ax = plt.subplots()
# area.plot(ax=ax, facecolor='none', edgecolor='black', label='Original Boundary')
# gpd.GeoSeries(buffered_area.geometry).plot(ax=ax, facecolor='none', edgecolor='blue', linestyle='--', label='Buffered Boundary')
# edges.plot(ax=ax, linewidth=1, edgecolor='red', label='Roads')
# # Plot the stops as well
# plt.scatter(stops_lon, stops_lat, color='green', label='Stops')
# plt.legend()
# plt.show()