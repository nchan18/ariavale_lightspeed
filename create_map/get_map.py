import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx


place_name = 'University of North Carolina at Charlotte'
area = ox.geocode_to_gdf(place_name)

area.columns = [col[:10] for col in area.columns]

area.to_file("uncc_boundary.shp")

buffered_area = area.buffer(0.01)  # Adjust the buffer distance as needed

G = ox.graph_from_polygon(buffered_area.unary_union, network_type='all')
Gn = nx.MultiDiGraph()

nodes, edges = ox.graph_to_gdfs(G)

edges = edges[edges['highway'] != 'footway']

# Plot the stops form route_stops.txt
stops_lat = []
stops_lon = []
with open("stop_list.txt", "r") as stops:
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

#add the stops as nodes to the graph
for i in range(len(stops_lat)):
    Gn.add_node(i, x=stops_lon[i], y=stops_lat[i])

#find the stop nodes closest to the road network
for i in range(len(stops_lat)):
    stop_node = ox.nearest_nodes(G, X= stops_lat[i], Y= stops_lon[i])
    Gn.add_edge(stop_node, i)

fig, ax = plt.subplots()
area.plot(ax=ax, facecolor='none', edgecolor='black', label='Original Boundary')
gpd.GeoSeries(buffered_area).plot(ax=ax, facecolor='none', edgecolor='blue', linestyle='--', label='Buffered Boundary')
edges.plot(ax=ax, linewidth=1, edgecolor='black', label='Roads')
# plot the stops as well
plt.scatter(stops_lon, stops_lat, color='red', label='Stops', s=100)
plt.legend()
plt.show()
