# Student ID: 010826054
from datetime import datetime, timedelta

from models.hash_table import HashTable
from models.truck import Truck
from services.clustering import assign_packages_to_clusters
from user_interface.viewer import view_delivery_status
import csv

# Main program for delivering packages according to specified requirements

# Create an instance of the HashTable to store package data
package_table = HashTable(size=40)  # Assuming 40 packages as an average per day

# Load package data from WGUUPS Package File
# Replace 'wguups_package_file.csv' with the actual path to the package data
with open('./data/wguups_package_file.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        package_id = int(row['Package ID'])
        address = row['Address']
        deadline = row['Delivery Deadline']
        city = row['City']
        zip_code = row['Zip']
        weight = float(row['Weight KILO'])
        status = "At the hub"  # Initially all packages are at the hub
        special_note = row.get('page 1 of 1 Page Special Notes', "").strip()
        # Insert package data into the hash table
        package_table.insert(package_id, address, deadline, city, zip_code, weight, status, special_note)

# Load distance data from WGUPS Distance Table
# Assuming 'wgups_distance_table.csv' has a matrix of distances between locations
# Replace with the actual path to the distance data
distance_data = []

with open('data/wguups_distance_table.csv', mode='r') as file:
    reader = csv.reader(file)
    headers_skipped = False
    for row in reader:
        # Skip the first row containing headers
        if not headers_skipped:
            headers_skipped = True
            continue

        # Skip the first column and convert the remaining values to float
        try:
            distance_row = [float(x) if x.strip() else 0.0 for x in
                            row[1:]]  # Skip the first column with location names
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

# Assign packages to trucks based on clustering logic
truck_1_packages, truck_2_packages, truck_3_packages = assign_packages_to_clusters(package_table, location_indices)

# Create instances of the trucks
truck_1 = Truck(truck_id=1)
truck_2 = Truck(truck_id=2)
truck_3 = Truck(truck_id=3)

# Phase 1: Load and Deliver Packages for Truck 1 and Truck 2
print("Phase 1: Loading Truck 1 and Truck 2")
truck_1.load_packages(range(1, 17))  # Load packages 1 to 16
truck_2.load_packages(range(17, 33))  # Load packages 17 to 32

# Deliver packages using Truck 1 and Truck 2
print("Starting Phase 1 Delivery")
truck_1.deliver_packages(package_table, location_indices, get_distance)
print(f"Truck 1 mileage after first delivery: {truck_1.get_mileage():.2f} miles")
truck_2.deliver_packages(package_table, location_indices, get_distance)
print(f"Truck 2 mileage after first delivery: {truck_2.get_mileage():.2f} miles")

# Phase 2: Loading Truck 3 at 9:35 AM
print("Phase 2: Loading Truck 3 at 9:35 AM")
truck_3.load_packages(range(33, 41))  # Load packages 33 to 40

# Phase 3: Deliver Packages using Truck 3 (After Truck 1 Returns to Hub)
print("\nStarting Phase 3: Truck 3 Takes Over, Truck 1 Returns to Hub")
truck_1.clear_packages()  # Unload Truck 1 packages after completion
truck_3.deliver_packages(package_table, location_indices, get_distance)
print(f"Truck 3 mileage after delivery: {truck_3.get_mileage():.2f} miles")

# Phase 4: Optionally Reload Truck 1 or Truck 2 (if more deliveries exist)
print("\nPhase 4: Reloading Truck 1 or Truck 2 for Remaining Deliveries")
# Optionally reload Truck 1 or Truck 2 for additional deliveries

print("\n--------------------------------------------------")
print("Final Package Status:")
print(package_table)

# Call the view_delivery_status function to allow the user to interact with the system
view_delivery_status(package_table=package_table, truck_1=truck_1, truck_2=truck_2, truck_3=truck_3)
