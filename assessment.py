import csv
from scipy.spatial import distance

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    print("point1:", point1)
    print("point2:", point2)
    return distance.euclidean(point1, point2)

# Load spot data
spot_data = []
with open('clustered_spots_day.csv', 'r') as spots_file:
    reader = csv.DictReader(spots_file)
    for row in reader:
        spot_data.append((row['spot_name'], float(row['latitude']), float(row['longitude']), int(row['day'])))

# Load hotel data
hotel_data = []
with open('hotel.csv', 'r') as hotels_file:
    reader = csv.DictReader(hotels_file)
    for row in reader:
        hotel_data.append((row['hotel_name'], float(row['latitude']), float(row['longitude']), int(row['day_start']), int(row['day_end'])))

# Function to assign spots to hotels based on proximity
def assign_spots_to_hotels(spot_data, hotel_data):
    spot_assignments = {hotel[0]: [] for hotel in hotel_data}
    
    for spot in spot_data:
        for hotel in hotel_data:
            if hotel[3] <= spot[3] <= hotel[4]:
                spot_assignments[hotel[0]].append(spot)
                break
    
    return spot_assignments

# Assign spots to hotels based on proximity
spot_assignments = assign_spots_to_hotels(spot_data, hotel_data)

# Calculate sum of distances from each hotel to its assigned spots
hotel_distances = {}
for hotel, spots in spot_assignments.items():
    hotel_coords = (hotel[1], hotel[2])
    total_distance = sum(calculate_distance((spot[1], spot[2]), hotel_coords) for spot in spots)
    hotel_distances[hotel[0]] = total_distance

# Exporting sum of distances to CSV
with open('hotel_distances.csv', 'w', newline='') as distances_file:
    writer = csv.writer(distances_file)
    writer.writerow(['hotel_name', 'total_distance'])
    for hotel, distance in hotel_distances.items():
        writer.writerow([hotel, distance])
