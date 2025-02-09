import passiogo
import matplotlib.pyplot as plt

# Step 1: Define the Transportation System ID for UNC Charlotte
uncc_system_id = 1053  # UNC Charlotte's ID

# Step 2: Get the TransportationSystem object for UNC Charlotte
system = passiogo.getSystemFromID(uncc_system_id)

# Step 3: Retrieve all stops for UNC Charlotte
stops = system.getStops()

#write the stops to a text file
with open('route_stops.txt', 'w', encoding='utf-8') as file:
    stops = system.getStops()
    for stop in stops:
        file.write(f"Stop ID: {stop.id}, Name: {stop.name}, Latitude: {stop.latitude}, Longitude: {stop.longitude}\n")