import math
import matplotlib.pyplot as plt

# Define all bus stops with their IDs, names, latitudes, and longitudes
stops = {
    "Gold": [
        (7514, "Student Union West", 35.30813611, -80.73277778),
        (7503, "Hunt Hall", 35.301245, -80.73553),
        (21288, "Alumni Way West", 35.30285263, -80.73758761),
        (7509, "Reese East", 35.304298876, -80.732765539),
        (7510, "Robinson Hall North", 35.30333333, -80.72944444),
        (7511, "Cato Hall North", 35.305, -80.72805556),
        (7512, "Fretwell North", 35.30739, -80.72931),
        (7513, "Science Building", 35.308101005, -80.730234865),
        (7502, "Union Deck", 35.30919, -80.73637),
        (7516, "Light Rail East", 35.31177, -80.73317),
        (7517, "Student Health East", 35.311491571, -80.730662848),
        (7519, "Fretwell South", 35.30694444, -80.72944444),
        (7520, "Cato Hall South", 35.305, -80.72833333),
        (7521, "Robinson Hall South", 35.30361111, -80.72944444),
        (7522, "Levine Hall", 35.302067, -80.732963)
    ],
    "Silver": [
        (7514, "Student Union West", 35.30813611, -80.73277778),
        (7530, "Student Union East", 35.30805556, -80.73277778),
        (7523, "CRI Deck", 35.30935, -80.74416667),
        (7525, "Duke Centennial Hall", 35.31224722, -80.74166667),
        (7527, "EPIC - South", 35.31, -80.74194444),
        (7528, "Athletics Complex - East", 35.307369865, -80.739830199),
        (7532, "Student Health North", 35.31055556, -80.72916667),
        (7533, "Martin Hall", 35.31027778, -80.72666667),
        (7534, "Lot 6", 35.308847, -80.725169),
        (7535, "Lot 5A", 35.30722222, -80.72527778),
        (7536, "East Deck 2", 35.306365, -80.726849),
        (7512, "Fretwell North", 35.30739, -80.72931),
        (7513, "Science Building", 35.308101005, -80.730234865),
        (7527, "EPIC North", 35.309383154, -80.741234492),
        (7539, "Grigg Hall", 35.31083333, -80.74138889),
        (7540, "PORTAL", 35.311106352, -80.743085324)
    ],
    "Shopping": [
        (7503, "Hunt Hall", 35.301245, -80.73553),
        (7516, "Light Rail East", 35.31177, -80.73317),
        (7522, "Levine Hall", 35.302067, -80.732963),
        (7533, "Martin Hall", 35.31027778, -80.72666667),
        (84435, "Patel Brothers", 35.294934, -80.751104),
        (84436, "Target", 35.293043, -80.745866),
        (84437, "Harris Teeter", 35.296567, -80.738436)
    ],
    "Charter": [
        (8277, "Charter start", 35.3062, -80.7361),
        (8278, "Charter end", 35.3087, -80.7405)
    ],
    "NPT Niner Paratransit": [
        (7514, "Student Union West", 35.30813611, -80.73277778),
        (7530, "Student Union East", 35.30805556, -80.73277778),
        (7523, "CRI Deck", 35.30935, -80.74416667)
    ],
    "Green": [
        (7530, "Student Union East", 35.30805556, -80.73277778),
        (7510, "Robinson Hall North", 35.30333333, -80.72944444),
        (7511, "Cato Hall North", 35.305, -80.72805556),
        (7512, "Fretwell North", 35.30739, -80.72931),
        (7519, "Fretwell South", 35.30694444, -80.72944444),
        (7520, "Cato Hall South", 35.305, -80.72833333),
        (7521, "Robinson Hall South", 35.30361111, -80.72944444),
        (8276, "FM/PPS", 35.311624885, -80.730350714),
        (8568, "North Deck", 35.3135, -80.73189),
        (7542, "Light Rail West", 35.3101, -80.7389),
        (7543, "Belk Hall", 35.31027778, -80.73611111),
        (7501, "Auxiliary Services", 35.30798734, -80.730352882),
        (7544, "Reese West", 35.304453196, -80.732767051),
        (7548, "Cone Deck", 35.30433, -80.73458),
        (15431, "Alumni Way East", 35.302508661, -80.737559067),
        (7545, "South Village Deck", 35.301067073, -80.735858307),
        (7546, "Gage Undergraduate Admissions Center", 35.302026116, -80.73274879),
        (7532, "Student Health North", 35.31055556, -80.72916667)
    ],
    "Greek": [
        (7514, "Student Union West", 35.30813611, -80.73277778),
        (129987, "Greek Village 1", 35.312138, -80.727255),
        (129988, "Greek Village 8", 35.313786, -80.72523),
        (7513, "Science Building", 35.308101005, -80.730234865),
        (129989, "Greek Village 4", 35.312106, -80.726067)
    ],
    "Red": [
        (7530, "Student Union East", 35.30805556, -80.73277778),
        (7519, "Fretwell South", 35.30694444, -80.72944444),
        (7512, "Fretwell North", 35.30739, -80.72931),
        (7514, "Student Union West", 35.30813611, -80.73277778),
        (32704, "Football Stadium/Gate 1", 35.309064, -80.740328)
    ]
}

# Colors for routes
colors = {
    "Green": "green",
    "Silver": "silver",
    "Red": "red",
    "Gold": "gold",
    "Greek": "purple",
    "Shopping": "orange"
}

def calculate_distance(coord1, coord2):
    R = 6371  # Earth radius in km
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# Plot setup
fig, ax = plt.subplots(figsize=(15, 10))

for route, route_stops in stops.items():
    # Duplicate first stop at end to complete loop
    closed_route = route_stops + [route_stops[0]]
    
    lats = [stop[2] for stop in closed_route]
    longs = [stop[3] for stop in closed_route]

    # Plot the route
    ax.plot(longs, lats, marker='o', label=route, color=colors.get(route, "blue"))
    
    # Add stop names as text
    for stop in closed_route:
        ax.text(stop[3], stop[2], stop[1], fontsize=9, ha='right', color=colors.get(route, "blue"))

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Bus Routes with Stop Names")
ax.legend()

plt.show()
