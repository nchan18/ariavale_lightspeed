import math
import matplotlib.pyplot as plt

# Define all bus stops with their IDs, names, latitudes, and longitudes
stops = {
    "Green": [
        (7516, "Light Rail", 35.31177, -80.73317),  # Stop #42
        (7543, "Belk Hall", 35.31027778, -80.73611111),  # Stop #43
        (7530, "Student Union - East", 35.30805556, -80.73277778),  # Stop #8
        (7501, "Auxiliary Services", 35.30798734, -80.730352882),  # Stop #9
        (7519, "Fretwell - South", 35.30694444, -80.72944444),  # Stop #37
        (7520, "Cato Hall - South", 35.305, -80.72833333),  # Stop #38
        (7521, "Robinson Hall - South", 35.30361111, -80.72944444),  # Stop #39
        (7544, "Reese West", 35.304453196, -80.732767051),  # Stop #44
        (7548, "Cone Deck", 35.30433, -80.73458),  # Stop #45
        (15431, "Alumni Way - East", 35.302508661, -80.737559067),  # Stop #49
        (7545, "South Village Deck", 35.301067073, -80.735858307),  # Stop #46
        (7546, "Gage UA Center", 35.302026116, -80.73274879),  # Stop #47
        (7510, "Robinson Hall North", 35.30333333, -80.72944444),  # Stop #31
        (7511, "Cato Hall - North", 35.305, -80.72805556),  # Stop #32
        (7512, "Fretwell - North", 35.30739, -80.72931),  # Stop #16
        (7532, "Student Health - North", 35.31055556, -80.72916667),  # Stop #11
        (8276, "FM/PPS", 35.311624885, -80.730350714),  # Stop #41
        (8568, "North Deck", 35.3135, -80.73189)  # Stop #48
    ],
    "Silver": [
        (7523, "CRI Deck", 35.30935, -80.74416667),  # Stop #1
        (7525, "Duke Centennial Hall", 35.31224722, -80.74166667),  # Stop #3
        (7527, "EPIC - South", 35.31, -80.74194444),  # Stop #5
        (7528, "Athletics Complex - East", 35.307369865, -80.739830199),  # Stop #6
        (7530, "Student Union - East", 35.30805556, -80.73277778),  # Stop #8
        (7501, "Auxiliary Services", 35.30798734, -80.730352882),  # Stop #9
        (7532, "Student Health - North", 35.31055556, -80.72916667),  # Stop #11
        (7533, "Martin Hall", 35.31027778, -80.72666667),  # Stop #12
        (7534, "Lot 6", 35.308847, -80.725169),  # Stop #13
        (7535, "Lot 5A", 35.30722222, -80.72527778),  # Stop #14
        (7536, "East Deck 2", 35.306365, -80.726849),  # Stop #15
        (7512, "Fretwell - North", 35.30739, -80.72931),  # Stop #16
        (7513, "Klein Hall", 35.308101005, -80.730234865),  # Stop #17
        (7514, "Student Union - West", 35.30813611, -80.73277778),  # Stop #18
        (7537, "Athletics Complex - West", 35.3075, -80.73972222),  # Stop #20
        (7538, "EPIC - North", 35.309383154, -80.741234492),  # Stop #21
        (7539, "Grigg Hall", 35.31083333, -80.74138889),  # Stop #22
        (7540, "PORTAL", 35.311106352, -80.743085324)  # Stop #23
    ],
    "Red": [
        (7530, "Student Union East", 35.30805556, -80.73277778),  # Stop #8
        (7519, "Fretwell South", 35.30694444, -80.72944444),  # Stop #37
        (7512, "Fretwell North", 35.30739, -80.72931),  # Stop #16
        (7514, "Student Union West", 35.30813611, -80.73277778),  # Stop #18
        (32704, "Football Stadium/Gate 1", 35.309064, -80.740328)  # Stop #57
    ],
    "Gold": [
        (7533, "Wallis Hall", 35.31027778, -80.72666667),  # Stop #34
        (7517, "Student Health East", 35.311491571, -80.730662848),  # Stop #35
        (7519, "Fretwell South", 35.30694444, -80.72944444),  # Stop #37
        (7520, "Cato Hall South", 35.305, -80.72833333),  # Stop #38
        (7521, "Robinson Hall South", 35.30361111, -80.72944444),  # Stop #39
        (7522, "Levine Hall", 35.302067, -80.732963),  # Stop #40
        (7503, "Hunt Hall", 35.301245, -80.73553),  # Stop #24
        (21288, "Alumni Way West", 35.30285263, -80.73758761),  # Stop #56
        (7509, "Reese East", 35.304298876, -80.732765539),  # Stop #30
        (7510, "Robinson Hall North", 35.30333333, -80.72944444),  # Stop #31
        (7511, "Cato Hall North", 35.305, -80.72805556),  # Stop #32
        (7512, "Fretwell North", 35.30739, -80.72931),  # Stop #16
        (7513, "Klein Hall", 35.308101005, -80.730234865),  # Stop #17
        (7514, "Student Union West", 35.30813611, -80.73277778),  # Stop #18
        (7502, "Student Union Deck", 35.30919, -80.73637)  # Stop #33
    ],
    "Greek": [
        (7514, "Student Union West", 35.30813611, -80.73277778),
        (129987, "Greek Village 1", 35.312138, -80.727255),
        (129988, "Greek Village 8", 35.313786, -80.72523),
        (7513, "Klein Hall", 35.308101005, -80.730234865),
        (129989, "Greek Village 4", 35.312106, -80.726067),
        (7514, "Student Union West", 35.30813611, -80.73277778)
    ],
    "Shopping": [
        (7522, "Levine Hall", 35.302067, -80.732963),
        (7503, "Hunt Hall", 35.301245, -80.73553),
        (7503, "Wallis Hall East", 35.307139, -80.72931),  # Assuming same as Hunt Hall
        (7533, "Martin Hall", 35.31027778, -80.72666667),
        (84435, "Patel Brothers", 35.294934, -80.751104),
        (84436, "Target", 35.293043, -80.745866),
        (84437, "Harris Teeter", 35.296567, -80.738436)
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
    lons = [stop[3] for stop in closed_route]
    names = [stop[1] for stop in closed_route]
    
    # Plot route
    ax.plot(lons, lats, marker='o', markersize=6, linewidth=2, 
            color=colors[route], label=route, alpha=0.7)
    
    # Annotate stops
    for stop in route_stops:
        ax.annotate(stop[1], (stop[3], stop[2]), 
                   textcoords="offset points", xytext=(0,5),
                   ha='center', fontsize=8, alpha=0.8)

    # Calculate total distance
    total_dist = sum(calculate_distance((closed_route[i-1][2], closed_route[i-1][3]),(closed_route[i][2], closed_route[i][3]))for i in range(1, len(closed_route)))
    
    print(f"{route} Route: {total_dist:.2f} km")

# Map decorations
ax.set_title("UNC Charlotte Optimized Shuttle Routes", fontsize=16)
ax.set_xlabel("Longitude", fontsize=12)
ax.set_ylabel("Latitude", fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()