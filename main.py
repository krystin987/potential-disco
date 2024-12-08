# Student ID: 010826054

from datetime import datetime

import utils
from models.hash_table import HashTable
from models.truck import Truck
from user_interface.viewer import view_delivery_status
import csv

# Create an instance of the HashTable to store package data
package_table = HashTable(size=40)

# Load package data from WGUUPS Package File
with open('./data/wguups_package_file.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        package_id = int(row['Package ID'])
        address = row['Address']
        deadline = row['Delivery Deadline']
        city = row['City']
        zip_code = row['Zip']
        weight = float(row['Weight KILO'])
        special_note = row['Special Notes']
        status = "At the hub"  # Initially all packages are at the hub
        start_time = "At the hub"  # Initial start time

        # Insert package data into the hash table, including the new start_time field
        package_table.insert(package_id, address, deadline, city, zip_code, weight, status, special_note, start_time)

# Load distance data from Distance Table
distance_data = []
with open('data/wguups_distance_table.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        try:
            distance_row = [float(x) if x.strip() else 0.0 for x in row[1:]]
            distance_data.append(distance_row)
        except ValueError as e:
            print(f"Error parsing row: {row}, error: {e}")

# Function to get distance between two locations based on their indices in the distance data
def get_distance(location_1_index, location_2_index):
    return distance_data[location_1_index][location_2_index]

# Location indices mapping for accurate distance calculation
location_indices = {
    "4001 South 700 East": 0,
    "1060 Dalton Ave S": 1,
    "1330 2100 S": 2,
    "1488 4800 S": 3,
    "177 W Price Ave": 4,
    "195 W Oakland Ave": 5,
    "2010 W 500 S": 6,
    "2300 Parkway Blvd": 7,
    "233 Canyon Rd": 8,
    "2530 S 500 E": 9,
    "2600 Taylorsville Blvd": 10,
    "2835 Main St": 11,
    "300 State St": 12,
    "3060 Lester St": 13,
    "3148 S 1100 W": 14,
    "3365 S 900 W": 15,
    "3575 W Valley Central Station bus Loop": 16,
    "3595 Main St": 17,
    "380 W 2880 S": 18,
    "410 S State St": 19,
    "4300 S 1300 E": 20,
    "4580 S 2300 E": 21,
    "5025 State St": 22,
    "5100 South 2700 West": 23,
    "5383 South 900 East #104": 24,
    "600 E 900 South": 25,
    "6351 South 900 East": 26
}

# Create instances of the trucks
truck_1 = Truck(truck_id=1)
truck_2 = Truck(truck_id=2)
truck_3 = Truck(truck_id=3)

# --- Phase 1: Loading Truck 1 and Truck 2 ---
current_time = datetime.strptime("08:00 AM", "%I:%M %p")
print(f"\nPhase 1: Loading Truck 1 and Truck 2 at {current_time.strftime('%I:%M %p')}")
truck_1.load_packages([1, 2, 3, 4, 5, 6, 7, 8], package_table, current_time)
truck_2.load_packages([9, 10, 11, 12, 13, 14, 15, 16], package_table, current_time)

# --- Phase 2: Loading Truck 3 ---
current_time = datetime.strptime("09:35 AM", "%I:%M %p")
print("\nPhase 2: Loading Truck 3 at 9:35 AM")
truck_3.load_packages([17, 18, 19, 20, 21, 22, 23, 24], package_table, current_time)

# --- Deliver packages for Truck 1 and Truck 2 ---
truck_1.deliver_packages(package_table, location_indices, get_distance)
print("--------------------------------------------------")
print(f"Final Truck 1 mileage: {truck_1.get_mileage():.2f} miles")

truck_2.deliver_packages(package_table, location_indices, get_distance)
print("--------------------------------------------------")
print(f"Final Truck 2 mileage: {truck_2.get_mileage():.2f} miles")

# Update the address for package #9 at 10:20 AM
corrected_address = {
    'address': '410 S State St',
    'city': 'Salt Lake City',
    'zip_code': '84111'
}
update_time = datetime.strptime("10:20 AM", "%I:%M %p")
if current_time < update_time:
    current_time = update_time
    print("\n--- Address Correction at 10:20 AM ---")
    utils.update_package_address(package_table, 9, corrected_address)

# --- Deliver packages for Truck 3 ---
truck_3.deliver_packages(package_table, location_indices, get_distance)
print("--------------------------------------------------")
print(f"Final Truck 3 mileage: {truck_3.get_mileage():.2f} miles")

# Print the total mileage for all trucks
total_mileage = truck_1.get_mileage() + truck_2.get_mileage() + truck_3.get_mileage()
print("\n--------------------------------------------------")
print(f"End of Day Total Mileage for All Trucks: {total_mileage:.2f} miles")

# Display the hash table to check updates
print("\n--------------------------------------------------")
print("Final Package Status:")
print(package_table)

# Call the view_delivery_status function to allow the user to interact with the system
view_delivery_status(package_table=package_table, truck_1=truck_1, truck_2=truck_2, truck_3=truck_3)
