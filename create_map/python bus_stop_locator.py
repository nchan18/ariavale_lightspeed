import requests
import geopy.distance

# List of UNC Charlotte bus stops
stops = [
    {'Stop ID': 8277, 'Name': 'Charter start', 'Latitude': 35.308106119, 'Longitude': -80.732820822},
    {'Stop ID': 8278, 'Name': 'Charter end', 'Latitude': 35.308132323, 'Longitude': -80.732772658},
    {'Stop ID': 7514, 'Name': 'Student Union West', 'Latitude': 35.30813611, 'Longitude': -80.73277778},
    {'Stop ID': 7530, 'Name': 'Student Union East', 'Latitude': 35.30805556, 'Longitude': -80.73277778},
    {'Stop ID': 7523, 'Name': 'CRI Deck', 'Latitude': 35.30935, 'Longitude': -80.74416667},
    {'Stop ID': 7503, 'Name': 'Hunt Hall', 'Latitude': 35.301245, 'Longitude': -80.73553},
    {'Stop ID': 21288, 'Name': 'Alumni Way West', 'Latitude': 35.30285263, 'Longitude': -80.73758761},
    {'Stop ID': 7509, 'Name': 'Reese East', 'Latitude': 35.304298876, 'Longitude': -80.732765539},
    {'Stop ID': 7510, 'Name': 'Robinson Hall North', 'Latitude': 35.30333333, 'Longitude': -80.72944444},
    {'Stop ID': 7511, 'Name': 'Cato Hall North', 'Latitude': 35.305, 'Longitude': -80.72805556},
    {'Stop ID': 7512, 'Name': 'Fretwell North', 'Latitude': 35.30739, 'Longitude': -80.72931},
    {'Stop ID': 7513, 'Name': 'Science Building', 'Latitude': 35.308101005, 'Longitude': -80.730234865},
    {'Stop ID': 7502, 'Name': 'Union Deck', 'Latitude': 35.30919, 'Longitude': -80.73637},
    {'Stop ID': 7516, 'Name': 'Light Rail East', 'Latitude': 35.31177, 'Longitude': -80.73317},
    {'Stop ID': 7517, 'Name': 'Student Health East', 'Latitude': 35.311491571, 'Longitude': -80.730662848},
    {'Stop ID': 7519, 'Name': 'Fretwell South', 'Latitude': 35.30694444, 'Longitude': -80.72944444},
    {'Stop ID': 7520, 'Name': 'Cato Hall South', 'Latitude': 35.305, 'Longitude': -80.72833333},
    {'Stop ID': 7521, 'Name': 'Robinson Hall South', 'Latitude': 35.30361111, 'Longitude': -80.72944444},
    {'Stop ID': 7522, 'Name': 'Levine Hall', 'Latitude': 35.302067, 'Longitude': -80.732963},
    {'Stop ID': 8276, 'Name': 'FM/PPS', 'Latitude': 35.311624885, 'Longitude': -80.730350714},
    {'Stop ID': 8568, 'Name': 'North Deck', 'Latitude': 35.3135, 'Longitude': -80.73189},
    {'Stop ID': 7542, 'Name': 'Light Rail West', 'Latitude': 35.311946629, 'Longitude': -80.733450671},
    {'Stop ID': 7543, 'Name': 'Belk Hall', 'Latitude': 35.31027778, 'Longitude': -80.73611111},
    {'Stop ID': 7501, 'Name': 'Auxiliary Services', 'Latitude': 35.30798734, 'Longitude': -80.730352882},
    {'Stop ID': 7544, 'Name': 'Reese West', 'Latitude': 35.304453196, 'Longitude': -80.732767051},
    {'Stop ID': 7548, 'Name': 'Cone Deck', 'Latitude': 35.30433, 'Longitude': -80.73458},
    {'Stop ID': 15431, 'Name': 'Alumni Way East', 'Latitude': 35.302508661, 'Longitude': -80.737559067},
    {'Stop ID': 7545, 'Name': 'South Village Deck', 'Latitude': 35.301067073, 'Longitude': -80.735858307},
    {'Stop ID': 7546, 'Name': 'Gage Undergraduate Admissions Center', 'Latitude': 35.302026116, 'Longitude': -80.73274879},
    {'Stop ID': 7532, 'Name': 'Student Health North', 'Latitude': 35.31055556, 'Longitude': -80.72916667},
    {'Stop ID': 7525, 'Name': 'Duke Centennial Hall', 'Latitude': 35.31224722, 'Longitude': -80.74166667},
    {'Stop ID': 7527, 'Name': 'EPIC South', 'Latitude': 35.31, 'Longitude': -80.74194444},
    {'Stop ID': 7528, 'Name': 'Athletics Complex East', 'Latitude': 35.307369865, 'Longitude': -80.739830199},
    {'Stop ID': 7533, 'Name': 'Martin Hall', 'Latitude': 35.31027778, 'Longitude': -80.72666667},
    {'Stop ID': 7534, 'Name': 'Lot 6', 'Latitude': 35.308847, 'Longitude': -80.725169},
    {'Stop ID': 7535, 'Name': 'Lot 5A', 'Latitude': 35.30722222, 'Longitude': -80.72527778},
    {'Stop ID': 7536, 'Name': 'East Deck 2', 'Latitude': 35.306365, 'Longitude': -80.726849},
    {'Stop ID': 7537, 'Name': 'Athletics Complex West', 'Latitude': 35.3075, 'Longitude': -80.73972222},
    {'Stop ID': 7538, 'Name': 'EPIC North', 'Latitude': 35.309383154, 'Longitude': -80.741234492},
    {'Stop ID': 7539, 'Name': 'Grigg Hall', 'Latitude': 35.31083333, 'Longitude': -80.74138889},
    {'Stop ID': 15405, 'Name': 'BATT Cave', 'Latitude': 35.31284, 'Longitude': -80.74101},
    {'Stop ID': 7540, 'Name': 'Portal West', 'Latitude': 35.311106352, 'Longitude': -80.743085324},
    {'Stop ID': 129987, 'Name': 'Greek Village 1', 'Latitude': 35.312138, 'Longitude': -80.727255},
    {'Stop ID': 129988, 'Name': 'Greek Village 8', 'Latitude': 35.313786, 'Longitude': -80.72523},
    {'Stop ID': 129989, 'Name': 'Greek Village 4', 'Latitude': 35.312106, 'Longitude': -80.726067},
    {'Stop ID': 84435, 'Name': 'Patel Brothers', 'Latitude': 35.294934, 'Longitude': -80.751104},
    {'Stop ID': 84436, 'Name': 'Target', 'Latitude': 35.293043, 'Longitude': -80.745866},
    {'Stop ID': 84437, 'Name': 'Harris Teeter', 'Latitude': 35.296567, 'Longitude': -80.738436},
    {'Stop ID': 32704, 'Name': 'Football Stadium/Gate 1', 'Latitude': 35.309064, 'Longitude': -80.740328}
]

# Function to find the nearest stop from a given point (latitude, longitude)
def find_nearest_stop(lat, lon, stops):
    min_distance = float('inf')
    nearest_stop = None
    
    for stop in stops:
        stop_coords = (stop['Latitude'], stop['Longitude'])
        user_coords = (lat, lon)
        
        distance = geopy.distance.distance(stop_coords, user_coords).meters
        
        if distance < min_distance:
            min_distance = distance
            nearest_stop = stop
    
    return nearest_stop, min_distance

# Input coordinates for the point you're checking from (e.g., user input, GPS coordinates)
user_lat = 35.308
user_lon = -80.735

nearest_stop, distance = find_nearest_stop(user_lat, user_lon, stops)

# Print the result
if nearest_stop:
    print(f"The nearest stop to the point ({user_lat}, {user_lon}) is '{nearest_stop['Name']}' with a distance of {distance:.2f} meters.")
else:
    print("No nearest stop found.")
