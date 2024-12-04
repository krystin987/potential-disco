# distance.py

import csv

# Load distance data from a CSV file
def load_distance_data(file_path):
    distance_data = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                distance_row = [float(x) if x else 0.0 for x in row]
                distance_data.append(distance_row)
            except ValueError as e:
                print(f"Error parsing row: {row}, error: {e}")
    return distance_data

# Function to get distance between two locations based on their indices in the distance data
def get_distance(location_1_index, location_2_index, distance_data):
    return distance_data[location_1_index][location_2_index]
