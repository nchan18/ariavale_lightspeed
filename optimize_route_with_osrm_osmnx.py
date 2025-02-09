import osmnx as ox
import networkx as nx
import osrm
import matplotlib.pyplot as plt
import polyline
from geopy.distance import geodesic

# Example stops with (latitude, longitude)
stops = [
    (35.308106119, -80.732820822),  # Stop 1
    (35.308132323, -80.732772658),  # Stop 2
    (35.30935, -80.74416667),  # Stop 3
    (35.31027778, -80.72666667)  # Stop 4
]

def get_graph_from_osm(city='Charlotte, North Carolina'):
    """
    Fetch OpenStreetMap data for a city using OSMnx.
    Returns the road network graph.
    """
    print("Fetching OpenStreetMap graph for:", city)
    graph = ox.graph_from_place(city, network_type='all')
    return graph

def get_nearest_nodes(graph, stops):
    """
    Find the nearest graph nodes for each stop (lat, lon) pair using OSMnx.
    """
    nodes = []
    for lat, lon in stops:
        nearest_node = ox.distance.nearest_nodes(graph, X=lon, Y=lat)
        nodes.append(nearest_node)
    return nodes

def get_route_via_osrm(start_lat, start_lon, end_lat, end_lon):
    """
    Use the OSRM API to get the route between two coordinates (latitude, longitude).
    Returns the polyline geometry.
    """
    client = osrm.Client(host='http://router.project-osrm.org')
    try:
        result = client.route(
            coordinates=[(start_lon, start_lat), (end_lon, end_lat)],
            overview='full',
            annotations=['distance', 'duration']
        )
        route_geometry = result['routes'][0]['geometry']
        return polyline.decode(route_geometry)  # Decoding polyline to lat-lon points
    except Exception as e:
        print("Error with OSRM route:", e)
        return []

def plot_route(graph, route, stops):
    """
    Plot the route on a map.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    # Plot the graph
    ox.plot_graph(graph, ax=ax, node_size=0, bgcolor='w', show=False, close=False)
    
    # Plot the route
    route_latitudes = [lat for lat, lon in route]
    route_longitudes = [lon for lat, lon in route]
    ax.plot(route_longitudes, route_latitudes, color='r', linewidth=3, label='Optimized Route')

    # Plot stops
    stop_latitudes = [lat for lat, lon in stops]
    stop_longitudes = [lon for lat, lon in stops]
    ax.scatter(stop_longitudes, stop_latitudes, color='b', s=100, zorder=5, label='Stops')
    
    plt.legend()
    plt.show()

def main():
    # Fetch OSM graph data for the city
    graph = get_graph_from_osm()

    # Get nearest graph nodes for each stop
    nodes = get_nearest_nodes(graph, stops)
    print(f"Nearest nodes for stops: {nodes}")
    
    # Use OSRM to get the route between each consecutive stop
    all_route_coordinates = []
    for i in range(len(stops) - 1):
        start_lat, start_lon = stops[i]
        end_lat, end_lon = stops[i + 1]
        
        # Get the route via OSRM between the stops
        route = get_route_via_osrm(start_lat, start_lon, end_lat, end_lon)
        all_route_coordinates.extend(route)

    # Plot the route on the map
    plot_route(graph, all_route_coordinates, stops)

if __name__ == '__main__':
    main()
