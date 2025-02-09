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

# Step 2: Fetch real-time bus data with predicted arrival times
system = passiogo.getSystemFromID(1053)  # UNC Charlotte's system ID

# Step 3: Map bus stops to intersections
stop_to_intersection = {
    "Student Union West": "IntersectionX",
    "Fretwell North": "IntersectionY",
    "Light Rail East": "IntersectionZ",
}

# Step 4: Run the optimization loop
while True:
    buses = system.getVehicles()  # Fetch real-time bus data
    for bus in buses:
        # Inspect the bus object to find the correct attribute
        print(bus.__dict__)  # Debugging: Print all attributes of the bus object

        # Example: Replace 'next_stop' with the correct attribute
        if hasattr(bus, 'next_stop'):  # Check if the attribute exists
            next_stop = bus.next_stop
        else:
            print(f"Bus {bus.id} does not have a 'next_stop' attribute.")
            continue  # Skip this bus and move to the next one

        eta = bus.eta  # Get the predicted arrival time at the next stop

        if next_stop in stop_to_intersection:
            intersection = stop_to_intersection[next_stop]
            print(f"Bus {bus.id} will arrive at {intersection} in {eta} seconds.")
            adjust_traffic_light(intersection, eta)

    time.sleep(30)  # Wait 30 seconds before fetching data again