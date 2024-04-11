import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

# Load spot data
spot_data = []
with open('data.csv', 'r') as spots_file:
    reader = csv.DictReader(spots_file)
    for row in reader:
        spot_data.append((row['spot_name'], float(row['latitude']), float(row['longitude'])))

# Load hotel data
hotel_data = []
with open('hotel.csv', 'r') as hotels_file:
    reader = csv.DictReader(hotels_file)
    for row in reader:
        hotel_data.append((row['hotel_name'], float(row['latitude']), float(row['longitude']), int(row['day_start']), int(row['day_end'])))

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return distance.euclidean(point1, point2)

# Function to assign spots to hotels based on proximity and capacity
def assign_spots_to_hotels(spot_data, hotel_data):
    num_spots_per_day = len(spot_data) // len(hotel_data)
    spot_assignments = {i: [] for i in range(1, len(hotel_data) + 1)}
    spots_remaining = {i: num_spots_per_day for i in range(1, len(hotel_data) + 1)}
    
    for spot in spot_data:
        min_distance = float('inf')
        closest_hotel = None
        
        for hotel in hotel_data:
            dist = calculate_distance((spot[1], spot[2]), (hotel[1], hotel[2]))
            if dist < min_distance and spots_remaining[hotel[3]] > 0:
                min_distance = dist
                closest_hotel = hotel
        
        if closest_hotel is not None:
            spot_assignments[closest_hotel[3]].append(spot)
            spots_remaining[closest_hotel[3]] -= 1
    
    return spot_assignments

# Assign spots to hotels based on proximity and capacity
spot_assignments = assign_spots_to_hotels(spot_data, hotel_data)

# Plot spots and hotels with assigned day centers
plt.figure(figsize=(10, 6))
for day_index, spots_in_day in spot_assignments.items():
    if spots_in_day:  # Check if there are spots assigned to this day
        spots = np.array([(spot[1], spot[2]) for spot in spots_in_day])
        plt.scatter(spots[:,0], spots[:,1], label=f'Day {day_index}')

for hotel in hotel_data:
    plt.scatter(hotel[1], hotel[2], color='red', label='Hotels')
    plt.annotate(hotel[0], (hotel[1], hotel[2]), textcoords="offset points", xytext=(10,0), ha='center')

plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('Optimized Spots and Assigned Hotels')
plt.legend()
plt.show()

# Exporting clustered spots and hotel distances to CSV
with open(f'clustered_spots_day.csv', 'w', newline='') as spots_file:
    writer = csv.writer(spots_file)
    writer.writerow(['spot_name', 'latitude', 'longitude', 'day', 'hotel_name', 'distance_to_hotel'])
    for day_index, spots_in_day in spot_assignments.items():
        for spot in spots_in_day:
            for hotel in hotel_data:
                if hotel[3] <= day_index <= hotel[4]:
                    distance_to_hotel = calculate_distance((spot[1], spot[2]), (hotel[1], hotel[2]))
                    writer.writerow([spot[0], spot[1], spot[2], day_index, hotel[0], distance_to_hotel])


