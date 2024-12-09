# Student ID: 010826054

from datetime import datetime

import utils
from models.hash_table import HashTable
from models.truck import Truck
from user_interface.viewer import view_delivery_status
import csv
from services.clustering import assign_packages_to_clusters, reassign_special_packages
from routing.routing import optimize_route

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
    try:
        return distance_data[location_1_index][location_2_index]
    except IndexError:
        print(f"Invalid indices: {location_1_index}, {location_2_index}")
        return float('inf')  # Use infinity to indicate an invalid distance

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

# Assign packages to clusters
print("\nAssigning packages to clusters...")
truck_1_packages, truck_2_packages, truck_3_packages, special_case_packages = assign_packages_to_clusters(package_table, location_indices)

# Reassign special-case packages
print("\nReassigning special-case packages...")
reassign_special_packages(
    special_case_packages,
    truck_1_packages,
    truck_2_packages,
    truck_3_packages,
    package_table,
    location_indices,
    distance_data,
    get_distance
)
print("Special-case package reassignment completed.")

# Display cluster assignments
print("\nCluster Assignments:")
print(f"Truck 1 Packages: {truck_1_packages}")
print(f"Truck 2 Packages: {truck_2_packages}")
print(f"Truck 3 Packages: {truck_3_packages}")
print(f"Special Case Packages: {special_case_packages}")

# Exclude Package 9 from initial truck loading
print("\nExcluding Package 9 from Truck 1 packages for initial loading...")
truck_1_packages = [pkg for pkg in truck_1_packages if pkg != 9]
print(f"Truck 1 packages after exclusion: {truck_1_packages}")

# Initialize current time for simulation
current_time = datetime.strptime("08:00 AM", "%I:%M %p")

# Phase 1: Load and deliver Truck 1 and Truck 2
print(f"\nPhase 1: Loading Truck 1 and Truck 2 at {current_time.strftime('%I:%M %p')}")
truck_1.load_packages(truck_1_packages, package_table, current_time)
truck_2.load_packages(truck_2_packages, package_table, current_time)

# Optimize routes before starting deliveries
for truck, packages in [(truck_1, truck_1_packages), (truck_2, truck_2_packages)]:
    print(f"\nOptimizing route for Truck {truck.truck_id}...")
    truck.packages = optimize_route(truck, location_indices, get_distance, package_table)
    print(f"Optimized route for Truck {truck.truck_id}: {truck.packages}")

# Start deliveries for Truck 1 until 10:20 AM
print("\nTruck 1 starting deliveries until 10:20 AM...")
stop_time = datetime.strptime("10:20 AM", "%I:%M %p")
truck_1.deliver_packages(package_table, location_indices, get_distance, distance_data, stop_time)

# Start deliveries for Truck 2
print("\nTruck 2 starting deliveries...")
truck_2.deliver_packages(package_table, location_indices, get_distance, distance_data)

# Handle Package 9 centrally
print("\nHandling Package 9...")
corrected_address = {'address': '410 S State St', 'city': 'Salt Lake City', 'zip_code': '84111'}
current_time = utils.handle_package_nine(
    package_table=package_table,
    truck=truck_1,
    corrected_address=corrected_address,
    current_time=current_time,
    location_indices=location_indices,
    get_distance=get_distance,
    distance_data=distance_data
)

# Reload Truck 1 with leftover packages when it returns for Package 9
print("\nHandling leftover packages...")
truck_1.reload_packages(package_table, location_indices, distance_data, get_distance)

# Continue Truck 1 deliveries for remaining packages
print("\nTruck 1 resuming deliveries after reloading Package 9...")
truck_1.deliver_packages(package_table, location_indices, get_distance, distance_data, stop_time=None)

# Late Pickup Phase: Redistributing remaining packages
print("\nLate Pickup Phase: Redistributing remaining packages...")
if special_case_packages:
    reassign_special_packages(
        special_case_packages,
        truck_1.packages,
        truck_2.packages,
        truck_3.packages,
        package_table,
        location_indices,
        distance_data,
        get_distance
    )

# Trucks return to hub to pick up any remaining packages
for truck in [truck_1, truck_2, truck_3]:
    if truck.unloaded_packages:
        print(f"\nTruck {truck.truck_id} returning to hub for remaining packages...")
        truck.reload_packages(package_table, location_indices, distance_data, get_distance)

# Ensure compliance with two-driver rule
print("\nEnsuring compliance with two-driver rule...")
if truck_1.current_time > truck_2.current_time:
    print("Truck 2 has completed deliveries. Driver assigned to Truck 3.")
    truck_2.return_to_hub(get_distance, truck_2.current_time)
    current_time = truck_2.current_time
else:
    print("Truck 1 has completed deliveries. Driver assigned to Truck 3.")
    truck_1.return_to_hub(get_distance, truck_1.current_time)
    current_time = truck_1.current_time

# Phase 2: Load and deliver Truck 3
print(f"\nPhase 2: Loading Truck 3 at {current_time.strftime('%I:%M %p')}")
truck_3.current_time = current_time
truck_3.load_packages(truck_3_packages, package_table, truck_3.current_time)

# Optimize route for Truck 3
print(f"\nOptimizing route for Truck {truck_3.truck_id}...")
truck_3.packages = optimize_route(truck_3, location_indices, get_distance, package_table)
print(f"Optimized route for Truck {truck_3.truck_id}: {truck_3.packages}")

print("\nTruck 3 starting deliveries...")
truck_3.deliver_packages(package_table, location_indices, get_distance, distance_data, stop_time=None)

# Validate and print the total mileage for all trucks
total_mileage = truck_1.get_mileage() + truck_2.get_mileage() + truck_3.get_mileage()
print(f"\nTotal Mileage for All Trucks: {total_mileage:.2f} miles")

if total_mileage > 140:
    print(f"WARNING: Total mileage exceeded the limit of 140 miles.")
else:
    print(f"Total mileage is within the limit of 140 miles.")

# Interactive viewer
view_delivery_status(package_table=package_table, truck_1=truck_1, truck_2=truck_2, truck_3=truck_3)