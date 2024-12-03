# Student ID: 010826054

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


# Function to simulate delivering packages
# For now, this will simply update the package status to 'Delivered'
# This is where you would include logic to manage trucks and their routes

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

# Function to simulate delivering all packages

def deliver_all_packages():
    for package_id in range(1, 41):  # Assuming 40 packages, with IDs ranging from 1 to 40
        delivery_time = "10:00 AM"  # Set a default or simulated delivery time
        deliver_package(package_id, delivery_time)

# Deliver all packages
deliver_all_packages()