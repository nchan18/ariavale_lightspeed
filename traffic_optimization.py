import time
import passiogo

# Step 1: Define functions first
def adjust_traffic_light(intersection, bus_eta):
    if bus_eta < 30:  # If the bus is 30 seconds away
        print(f"Adjusting traffic light at {intersection} to green for bus.")
        send_traffic_light_command(intersection, "turn_green")
    else:
        print(f"No adjustment needed at {intersection}.")

def send_traffic_light_command(intersection, command):
    # Simulate sending a command to the traffic light controller
    print(f"Sending command to {intersection}: {command}")
    # Replace this with actual API calls or hardware integration

def predict_next_stop(bus, route_to_stops):
    # Get the ordered list of stops for the bus's route
    stops = route_to_stops.get(bus.routeName, [])

    if not stops:
        return None  # No stops found for this route

    # Find the index of the bus's current stop
    # For now, assume the bus is at the first stop (you can improve this logic)
    current_stop_index = 0  # Default to the first stop

    # If the bus has a 'current_stop' attribute, use it to find the index
    if hasattr(bus, 'current_stop'):
        current_stop_index = stops.index(bus.current_stop)

    # Determine the next stop
    if current_stop_index < len(stops) - 1:
        return stops[current_stop_index + 1]  # Next stop in the sequence
    else:
        return None  # No next stop (end of route)

# Step 2: Get the TransportationSystem object for UNC Charlotte
system = passiogo.getSystemFromID(1053)  # UNC Charlotte's system ID

# Step 3: Map routes to their ordered stops
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

# Step 4: Map bus stops to intersections
stop_to_intersection = {
    "Student Union West": "IntersectionX",
    "Fretwell North": "IntersectionY",
    "Light Rail East": "IntersectionZ",
}

# Step 5: Run the optimization loop
while True:
    buses = system.getVehicles()  # Fetch real-time bus data
    for bus in buses:
        # Predict the next stop
        next_stop = predict_next_stop(bus, route_to_stops)

        if next_stop:
            print(f"Bus {bus.id} is approaching {next_stop}.")
            if next_stop in stop_to_intersection:
                intersection = stop_to_intersection[next_stop]
                print(f"Bus {bus.id} will arrive at {intersection} soon.")
                adjust_traffic_light(intersection, 30)  # Example ETA: 30 seconds
        else:
            print(f"Bus {bus.id} does not have a predicted next stop.")

    time.sleep(30)  # Wait 30 seconds before fetching data again