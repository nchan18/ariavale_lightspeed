import time
import passiogo
import requests

def get_school_id():
    # Replace with the actual URL of the Passio GO API endpoint
    all_systems = passiogo.getSystems()
    counter = 0
    for system in all_systems:
        print(f"{counter}:{system.name}")
        counter += 1
    school_id = int(input("Enter the number of the school you want to get the ID for:"))
    return all_systems[school_id].id

# Example usage
school_name = "University of North Carolina at Charlotte"
school_id = get_school_id()
if school_id:
    print(f"The ID for {school_name} is {school_id}")
    # Step 2: Get the TransportationSystem object for UNC Charlotte
    system = passiogo.getSystemFromID(school_id)

    # Step 3: Retrieve all stops for UNC Charlotte
    stops = system.getStops()

    # Step 4: Print the stops
    print(f"Stops for UNC Charlotte (System ID: {school_id}):")
    for stop in stops:
        print(f"Stop ID: {stop.id}, Name: {stop.name}, Latitude: {stop.latitude}, Longitude: {stop.longitude}")

    # Step 1: Get the TransportationSystem object for UNC Charlotte
    system = passiogo.getSystemFromID(1053)  # UNC Charlotte's system ID

    # Step 2: Fetch all routes for the transportation system
    routes = system.getRoutes()

    # Step 3: Create a dictionary to store route-stop mappings
    route_stop_mapping = {}

    # Step 4: Fetch stops for each route and store the mapping
    for route in routes:
        route_name = route.name  # Get the route name
        stops = route.getStops()  # Fetch stops for this route
        stop_names = [stop.name for stop in stops]  # Extract stop names
        route_stop_mapping[route_name] = stop_names  # Add to the dictionary

    # Step 5: Print the route-stop mapping
    for route_name, stop_names in route_stop_mapping.items():
        print(f"Route: {route_name}")
        print(f"Stops: {', '.join(stop_names)}")
        print("-" * 40)  # Separator for readability
else:
    print(f"School named {school_name} not found")

