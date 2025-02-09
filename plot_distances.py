import math
import matplotlib.pyplot as plt

# Haversine function to calculate distance between two points
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371  # Radius of Earth in kilometers
    distance = R * c  # Distance in kilometers
    return distance

# List of stops with latitude and longitude
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

# Calculate and store distances
distances = []
for i in range(len(stops) - 1):
    lat1, lon1 = stops[i]
    lat2, lon2 = stops[i + 1]
    distance = haversine(lat1, lon1, lat2, lon2)
    distances.append(distance)

# Plotting the route with distances on Matplotlib
fig, ax = plt.subplots()

# Extract latitudes and longitudes for plotting
lats = [stop[0] for stop in stops]
lons = [stop[1] for stop in stops]

# Plot the points
ax.plot(lons, lats, 'bo-', markersize=6)

# Annotate each point with its index (stop number)
for i, stop in enumerate(stops):
    ax.annotate(f'{i + 1}', (stop[1], stop[0]), textcoords="offset points", xytext=(0, 10), ha='center')

# Plot the distances between consecutive points
for i in range(len(distances)):
    ax.annotate(f'{distances[i]:.2f} km', 
                ((lons[i] + lons[i + 1]) / 2, (lats[i] + lats[i + 1]) / 2),
                textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color='green')

# Label the axes
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Stops and Distances between Each Stop')

plt.show()
