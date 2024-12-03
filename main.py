# Student ID: 010826054
from datetime import timedelta, datetime

from models.hash_table import HashTable
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

        # Insert package data into the hash table
        package_table.insert(package_id, address, deadline, city, zip_code, weight, status)


# Truck Class
class Truck:
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []  # List of package IDs assigned to this truck
        self.current_location = "4001 South 700 East"  # Starting point: WGUPS Hub
        self.speed = 18  # Speed in miles per hour
        self.miles_driven = 0
        self.start_time = datetime.strptime("08:00 AM", "%I:%M %p")
        self.current_time = self.start_time

    def load_package(self, package_id):
        if len(self.packages) < 16:
            self.packages.append(package_id)
        else:
            print(f"Truck {self.truck_id} is full. Cannot load package {package_id}.")

    def deliver_packages(self):
        for package_id in self.packages:
            # Simulate driving to the package location and delivering
            # For simplicity, we'll assume each delivery takes 15 minutes
            delivery_time = self.current_time.strftime("%I:%M %p")
            deliver_package(package_id, delivery_time)
            self.current_time += timedelta(minutes=15)

# Function to simulate delivering packages
def deliver_package(package_id, delivery_time):
    """
    Updates the delivery status of a package.
    :param package_id: Unique identifier of the package
    :param delivery_time: Time of delivery
    """
    package = package_table.lookup(package_id)
    if package:
        package['status'] = f"Delivered at {delivery_time}"
        print(f"Package {package_id} delivered at {delivery_time}.")
    else:
        print(f"Package {package_id} not found.")

# Create instances of the trucks
truck_1 = Truck(truck_id=1)
truck_2 = Truck(truck_id=2)
truck_3 = Truck(truck_id=3)

# Load packages onto trucks (simple distribution for now)
for package_id in range(1, 41):  # Assuming 40 packages, with IDs ranging from 1 to 40
    if package_id <= 16:
        truck_1.load_package(package_id)
    elif package_id <= 32:
        truck_2.load_package(package_id)
    else:
        truck_3.load_package(package_id)

# Deliver packages using each truck
truck_1.deliver_packages()
truck_2.deliver_packages()
truck_3.deliver_packages()

# Display the hash table to check updates
print(package_table)
