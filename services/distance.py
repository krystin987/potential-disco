# distance.py

import csv

from main import distance_data


# Load distance data from a CSV file
def load_distance_data(file_path):
    distance_data_list = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                distance_row = [float(x) if x else 0.0 for x in row]
                distance_data_list.append(distance_row)
            except ValueError as e:
                print(f"Error parsing row: {row}, error: {e}")
    return distance_data_list

# Function to get distance between two locations based on their indices in the distance data
def get_distance(location_1_index, location_2_index):
    if location_1_index < 0 or location_1_index >= len(distance_data):
        print(f"Error: location_1_index ({location_1_index}) is out of range.")
        return float('inf')  # Return a large value to indicate an invalid distance
    if location_2_index < 0 or location_2_index >= len(distance_data):
        print(f"Error: location_2_index ({location_2_index}) is out of range.")
        return float('inf')  # Return a large value to indicate an invalid distance
    return distance_data[location_1_index][location_2_index]

