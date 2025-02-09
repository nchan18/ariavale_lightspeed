import math
import matplotlib.pyplot as plt

# Define all bus stops for each route
stops = {
    "Shopping": [
        (35.301245, -80.73553, "Levine Hall"),
        (35.30739, -80.72931, "Hunt Hall"),
        (35.307139, -80.72931, "Wallis Hall East"),
        (35.31055556, -80.72666667, "Martin Hall"),
        (35.294934, -80.751104, "Patel Brothers"),
        (35.293043, -80.745866, "Target"),
        (35.296567, -80.738436, "Harris Teeter")
    ],
    "Greek": [
        (35.308132323, -80.732772658, "Student Union West"),
        (35.312138, -80.727255, "Greek Village 1"),
        (35.313786, -80.72523, "Greek Village 8"),
        (35.312106, -80.726067, "Greek Village 4"),
        (35.308132323, -80.732772658, "Student Union West")
    ],
    "Gold": [
        (35.31055556, -80.72666667, "Wallis Hall"),
        (35.311946629, -80.733450671, "Student Health East"),
        (35.31027778, -80.73611111, "Fretwell South"),
        (35.309064, -80.740328, "Cato Hall South"),
        (35.308106119, -80.732820822, "Levine Hall"),
        (35.30739, -80.72931, "Hunt Hall"),
        (35.307139, -80.72931, "Wallis Hall East"),
        (35.31055556, -80.72666667, "Martin Hall"),
        (35.30789, -80.732, "South Village Deck"),
        (35.3103, -80.7401, "Gage UA Center"),
        (35.3111, -80.7302, "Alumni Way West")
    ],
    "Red": [
        (35.308106119, -80.732820822, "Student Union East"),
        (35.30739, -80.72931, "Fretwell South"),
        (35.3075, -80.73972222, "Football Stadium/Gate 1"),
        (35.307, -80.7295, "Fretwell North")
    ],
    "Silver": [
        (35.30739, -80.743085324, "CRI Deck"),
        (35.30935, -80.74416667, "Duke Centennial Hall"),
        (35.31284, -80.74101, "EPIC South"),
        (35.31027778, -80.74138889, "Athletics Complex East"),
        (35.308106119, -80.732820822, "Student Union West"),
        (35.31295, -80.7461, "Student Health – North"),
        (35.311946, -80.733451, "Martin Hall")
    ],
    "Green": [
        (35.308132323, -80.732772658, "Student Union East"),
        (35.30333333, -80.72944444, "Robinson Hall North"),
        (35.305, -80.72805556, "Cato Hall North"),
        (35.30739, -80.72931, "Fretwell North"),
        (35.305, -80.72833333, "Fretwell South"),
        (35.30361111, -80.72944444, "Robinson Hall South"),
        (35.306, -80.739, "Light Rail"),
        (35.311, -80.740, "Belk Hall"),
        (35.307, -80.740, "Auxiliary Services"),
        (35.309, -80.745, "Reese West"),
        (35.3115, -80.748, "Alumni Way East"),
        (35.313, -80.741, "South Village Deck"),
        (35.312, -80.743, "Gage UA Center"),
        (35.31, -80.739, "FM/PPS"),
        (35.308, -80.742, "North Deck")
    ]
}

# Colors for routes
colors = {
    "Shopping": "green",
    "Greek": "brown",
    "Gold": "gold",
    "Red": "red",
    "Silver": "blue",
    "Green": "purple"
}

# Function to calculate distance
def calculate_distance(coord1, coord2):
    R = 6371  # Radius of the Earth in km
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in km

# Plot setup
fig, ax = plt.subplots()

# Plotting each route
for route, route_stops in stops.items():
    # Store the first stop to close the loop later
    first_stop = route_stops[0]

    # Extract latitude, longitude, and names
    lats = [stop[0] for stop in route_stops]
    lons = [stop[1] for stop in route_stops]
    names = [stop[2] for stop in route_stops]

    # Plot the route through all stops first
    ax.plot(lons, lats, marker='o', markersize=6, color=colors[route], label=route)

    # Annotate the stops
    for i, stop in enumerate(route_stops):
        ax.annotate(names[i], (stop[1], stop[0]), textcoords="offset points", xytext=(0, 10), ha='center')

    # After visiting all stops, close the loop by appending the first stop
    route_stops.append(first_stop)
    # Calculate and print the total distance
    total_distance = sum(calculate_distance(route_stops[i-1][:2], route_stops[i][:2]) for i in range(1, len(route_stops)))
    print(f"Total distance for {route}: {total_distance:.2f} km")

# Setting labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('UNC Charlotte Shuttle Routes')

# Display legend and plot
ax.legend()
plt.show()
