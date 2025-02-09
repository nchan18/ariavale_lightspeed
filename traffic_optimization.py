import time
import logging
import passiogo
from geopy.distance import geodesic

# Step 1: Set up logging
logging.basicConfig(filename='traffic_optimization.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Step 2: Define functions
def adjust_traffic_light(intersection, bus_eta):
    if bus_eta < 30:  # If the bus is 30 seconds away
        logging.info(f"Adjusting traffic light at {intersection} to green for bus.")
        send_traffic_light_command(intersection, "turn_green")
    else:
        logging.info(f"No adjustment needed at {intersection}.")

def send_traffic_light_command(intersection, command):
    # Simulate sending a command to the traffic light controller
    logging.info(f"Sending command to {intersection}: {command}")
    # Replace this with actual API calls or hardware integration
    if command == "turn_green":
        print(f"Turning green at {intersection}.")
    elif command == "turn_red":
        print(f"Turning red at {intersection}.")

def predict_next_stop(bus, route_to_stops, stops_data):
    # Get the ordered list of stops for the bus's route
    stops = route_to_stops.get(bus.routeName, [])

    if not stops:
        print(f"Bus {bus.id} has no stops mapped for route {bus.routeName}.")
        return None  # No stops found for this route

    # Get the bus's current location
    if hasattr(bus, 'latitude') and hasattr(bus, 'longitude'):
        bus_location = (bus.latitude, bus.longitude)
    elif hasattr(bus, 'lat') and hasattr(bus, 'lon'):  # Check for alternative attribute names
        bus_location = (bus.lat, bus.lon)
    else:
        print(f"Bus {bus.id} does not have location data.")
        return None

    # Find the closest stop
    closest_stop = None
    min_distance = float('inf')

    for stop_name in stops:
        stop_location = (stops_data[stop_name]['latitude'], stops_data[stop_name]['longitude'])
        distance = geodesic(bus_location, stop_location).meters  # Distance in meters

        if distance < min_distance:
            min_distance = distance
            closest_stop = stop_name

    # Find the index of the closest stop
    closest_stop_index = stops.index(closest_stop)

    # Determine the next stop
    if closest_stop_index < len(stops) - 1:
        return stops[closest_stop_index + 1]  # Next stop in the sequence
    else:
        print(f"Bus {bus.id} is at the last stop ({closest_stop}) in its route.")
        return None  # No next stop (end of route)

# Step 3: Get the TransportationSystem object for UNC Charlotte
system = passiogo.getSystemFromID(1053)  # UNC Charlotte's system ID

# Step 4: Map routes to their ordered stops
route_to_stops = {
    "Route Gold": [
        "Student Union West", "Hunt Hall", "Alumni Way West", "Reese East", 
        "Robinson Hall North", "Cato Hall North", "Fretwell North", 
        "Science Building", "Union Deck", "Light Rail East", 
        "Student Health East", "Fretwell South", "Cato Hall South", 
        "Robinson Hall South", "Levine Hall"
    ],
    "Silver": [
        "Student Union West", "Student Union East", "CRI Deck", 
        "Fretwell North", "Science Building", "Auxiliary Services", 
        "Student Health North", "Duke Centennial Hall", "EPIC South", 
        "Athletics Complex East", "Martin Hall", "Lot 6", "Lot 5A", 
        "East Deck 2", "Athletics Complex West", "EPIC North", 
        "Grigg Hall", "BATT Cave", "Portal West"
    ],
    "Shopping": [
        "Hunt Hall", "Light Rail East", "Levine Hall", "Martin Hall", 
        "Patel Brothers", "Target", "Harris Teeter"
    ],
    "Charter": ["Charter start", "Charter end"],
    "NPT Niner Paratransit": [
        "Student Union West", "Student Union East", "CRI Deck"
    ],
    "Route Green": [
        "Student Union East", "Robinson Hall North", "Cato Hall North", 
        "Fretwell North", "Fretwell South", "Cato Hall South", 
        "Robinson Hall South", "FM/PPS", "North Deck", "Light Rail West", 
        "Belk Hall", "Auxiliary Services", "Reese West", "Cone Deck", 
        "Alumni Way East", "South Village Deck", "Gage Undergraduate Admissions Center", 
        "Student Health North"
    ],
    "Route Greek": [
        "Student Union West", "Science Building", "Greek Village 1", 
        "Greek Village 8", "Greek Village 4"
    ],
    "Route Red": [
        "Student Union West", "Student Union East", "Fretwell North", 
        "Fretwell South", "Football Stadium/Gate 1"
    ]
}

# Step 5: Map bus stops to their coordinates
stops_data = {
    "Student Union West": {"latitude": 35.30813611, "longitude": -80.73277778},
    "Hunt Hall": {"latitude": 35.301245, "longitude": -80.73553},
    "Alumni Way West": {"latitude": 35.30285263, "longitude": -80.73758761},
    "Reese East": {"latitude": 35.304298876, "longitude": -80.732765539},
    "Robinson Hall North": {"latitude": 35.30333333, "longitude": -80.72944444},
    "Cato Hall North": {"latitude": 35.305, "longitude": -80.72805556},
    "Fretwell North": {"latitude": 35.30739, "longitude": -80.72931},
    "Science Building": {"latitude": 35.308101005, "longitude": -80.730234865},
    "Union Deck": {"latitude": 35.30919, "longitude": -80.73637},
    "Light Rail East": {"latitude": 35.31177, "longitude": -80.73317},
    "Student Health East": {"latitude": 35.311491571, "longitude": -80.730662848},
    "Fretwell South": {"latitude": 35.30694444, "longitude": -80.72944444},
    "Cato Hall South": {"latitude": 35.305, "longitude": -80.72833333},
    "Robinson Hall South": {"latitude": 35.30361111, "longitude": -80.72944444},
    "Levine Hall": {"latitude": 35.302067, "longitude": -80.732963},
    # Add more stops here
}

# Step 6: Map bus stops to intersections
stop_to_intersection = {
    "Student Union West": "IntersectionX",
    "Fretwell North": "IntersectionY",
    "Light Rail East": "IntersectionZ",
    "Hunt Hall": "IntersectionA",
    "Levine Hall": "IntersectionB",
    # Add more stops and intersections as needed
}

# Step 7: Run the optimization loop
while True:
    buses = system.getVehicles()  # Fetch real-time bus data

    for bus in buses:
        # Skip buses without location data
        if not hasattr(bus, 'latitude') or not hasattr(bus, 'longitude'):
            print(f"Bus {bus.id} does not have location data. Skipping...")
            continue

        # Predict the next stop
        next_stop = predict_next_stop(bus, route_to_stops, stops_data)

        if next_stop:
            logging.info(f"Bus {bus.id} is approaching {next_stop}.")
            if next_stop in stop_to_intersection:
                intersection = stop_to_intersection[next_stop]
                logging.info(f"Bus {bus.id} will arrive at {intersection} soon.")
                adjust_traffic_light(intersection, 30)  # Example ETA: 30 seconds
        else:
            logging.warning(f"Bus {bus.id} does not have a predicted next stop. Route: {bus.routeName}")

    time.sleep(30)  # Wait 30 seconds before fetching data again