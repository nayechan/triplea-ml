import csv
import numpy as np

# Generate hotel data
num_hotels = 33
hotel_data = [(f'Hotel {i+1}', np.random.uniform(30, 45), np.random.uniform(-125, -65), i+1, i+1) for i in range(num_hotels)]

# Write hotel data to hotel.csv
with open('hotel.csv', 'w', newline='') as hotels_file:
    writer = csv.writer(hotels_file)
    writer.writerow(['hotel_name', 'latitude', 'longitude', 'day_start', 'day_end'])
    writer.writerows(hotel_data)

# Generate spot data
num_spots = 99
spot_data = [(f'Spot {i+1}', np.random.uniform(30, 45), np.random.uniform(-125, -65)) for i in range(num_spots)]

# Write spot data to data.csv
with open('data.csv', 'w', newline='') as spots_file:
    writer = csv.writer(spots_file)
    writer.writerow(['spot_name', 'latitude', 'longitude'])
    writer.writerows(spot_data)
