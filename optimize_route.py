import requests
import json
import polyline
import folium
from folium.plugins import MarkerCluster

# Function to get the route via OSRM API
def get_route_via_osrm(stops):
    osrm_url = "http://router.project-osrm.org/route/v1/driving/"
    
    # Creating a list of coordinates in the format required by OSRM
    coordinates = ";".join([f"{lon},{lat}" for lat, lon in stops])

    # Build the URL for OSRM API request, requesting route geometry (polyline) and overview=false to avoid extra details
    url = osrm_url + coordinates + "?overview=full&geometries=polyline"

    # Make the request to the OSRM API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Log the entire response to understand its structure
        print("OSRM Response:", json.dumps(data, indent=4))
        
        # Ensure the 'routes' field exists and contains at least one route
        if 'routes' in data and len(data['routes']) > 0:
            route = data['routes'][0]
            
            # Check if 'geometry' exists in the route
            if 'geometry' in route:
                return route['geometry']
            else:
                print("Error: 'geometry' field not found in route.")
                return None
        else:
            print("Error: No routes found.")
            return None
    else:
        print(f"Error: Failed to retrieve route from OSRM. Status code: {response.status_code}")
        return None

# Function to plot the route on a map using folium
def plot_route_on_map(route_geometry, stops):
    # Decode the polyline geometry
    route_points = polyline.decode(route_geometry)
    
    # Create a map centered at the first stop
    map_center = stops[0]  # Use the first stop as the center
    map_obj = folium.Map(location=map_center, zoom_start=15)
    
    # Add markers for each stop
    marker_cluster = MarkerCluster().add_to(map_obj)
    for lat, lon in stops:
        folium.Marker([lat, lon], popup=f"Stop: ({lat}, {lon})").add_to(marker_cluster)
    
    # Plot the route on the map
    route_line = folium.PolyLine(route_points, color="blue", weight=4, opacity=0.6)
    route_line.add_to(map_obj)
    
    # Save the map to an HTML file
    map_obj.save("optimized_route_map_with_stops.html")
    print("Map saved as optimized_route_map_with_stops.html")

# Main function
def main():
    # List of stops with latitude and longitude (UNC Charlotte example)
    stops = [
        (35.308106119, -80.732820822),  # Charter start
        (35.308132323, -80.732772658),  # Charter end
        (35.30813611, -80.73277778),    # Student Union West
        (35.30805556, -80.73277778),    # Student Union East
        (35.30935, -80.74416667),       # CRI Deck
        (35.301245, -80.73553),         # Hunt Hall
        (35.30285263, -80.73758761),    # Alumni Way West
        (35.304298876, -80.732765539),  # Reese East
        (35.30333333, -80.72944444),    # Robinson Hall North
        (35.305, -80.72805556),         # Cato Hall North
        (35.30739, -80.72931),          # Fretwell North
        (35.308101005, -80.730234865),  # Science Building
        (35.30919, -80.73637),          # Union Deck
        (35.31177, -80.73317),          # Light Rail East
        (35.311491571, -80.730662848),  # Student Health East
        (35.30694444, -80.72944444),    # Fretwell South
        (35.305, -80.72833333),         # Cato Hall South
        (35.30361111, -80.72944444),    # Robinson Hall South
        (35.302067, -80.732963),        # Levine Hall
        (35.311624885, -80.730350714),  # FM/PPS
        (35.3135, -80.73189),           # North Deck
        (35.311946629, -80.733450671),  # Light Rail West
        (35.31027778, -80.73611111),    # Belk Hall
        (35.30798734, -80.730352882),   # Auxiliary Services
        (35.304453196, -80.732767051),  # Reese West
        (35.30433, -80.73458),          # Cone Deck
        (35.302508661, -80.737559067),  # Alumni Way East
        (35.301067073, -80.735858307),  # South Village Deck
        (35.302026116, -80.73274879),   # Gage Undergraduate Admissions Center
        (35.31055556, -80.72916667),    # Student Health North
        (35.31224722, -80.74166667),    # Duke Centennial Hall
        (35.31, -80.74194444),          # EPIC South
        (35.307369865, -80.739830199),  # Athletics Complex East
        (35.31027778, -80.72666667),    # Martin Hall
        (35.308847, -80.725169),        # Lot 6
        (35.30722222, -80.72527778),    # Lot 5A
        (35.306365, -80.726849),        # East Deck 2
        (35.3075, -80.73972222),        # Athletics Complex West
        (35.309383154, -80.741234492),  # EPIC North
        (35.31083333, -80.74138889),    # Grigg Hall
        (35.31284, -80.74101),          # BATT Cave
        (35.311106352, -80.743085324),  # Portal West
        (35.312138, -80.727255),        # Greek Village 1
        (35.313786, -80.72523),         # Greek Village 8
        (35.312106, -80.726067),        # Greek Village 4
        (35.294934, -80.751104),        # Patel Brothers
        (35.293043, -80.745866),        # Target
        (35.296567, -80.738436),        # Harris Teeter
        (35.309064, -80.740328)         # Football Stadium/Gate 1
    ]
    
    print("Fetching the optimal route...")
    route_geometry = get_route_via_osrm(stops)
    
    # If the route was successfully retrieved, plot it on the map
    if route_geometry:
        plot_route_on_map(route_geometry, stops)
    else:
        print("Failed to retrieve or plot the route.")

# Run the script
if __name__ == "__main__":
    main()
