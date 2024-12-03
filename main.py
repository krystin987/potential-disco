# Student ID: 010826054

from models.hash_table import HashTable
from models.truck import Truck
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

        # Insert package data into the hash table
        package_table.insert(package_id, address, deadline, city, zip_code, weight, status)




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
truck_1.deliver_packages(package_table)
print(f"Final Truck 1 mileage: {truck_1.miles_driven} miles")
truck_2.deliver_packages(package_table)
print(f"Final Truck 2 mileage: {truck_2.miles_driven} miles")
truck_3.deliver_packages(package_table)
print(f"Final Truck 3 mileage: {truck_3.miles_driven} miles")


# Display the hash table to check updates
print(package_table)

# Function to view the delivery status of any package and the total mileage of all trucks
def view_delivery_status():
    while True:
        print("\n--- Package Delivery Status Viewer ---")
        print("1. View package status by ID")
        print("2. View total mileage of all trucks")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                package_id = int(input("Enter the package ID: "))
                package = package_table.lookup(package_id)
                if package:
                    print(f"\nPackage ID: {package['package_id']}")
                    print(f"Address: {package['address']}, {package['city']}, {package['zip_code']}")
                    print(f"Deadline: {package['deadline']}")
                    print(f"Weight: {package['weight']} kg")
                    print(f"Status: {package['status']}\n")
                else:
                    print("\nPackage not found.\n")
            except ValueError:
                print("\nInvalid package ID. Please enter a numeric value.\n")

        elif choice == '2':
            total_mileage = truck_1.miles_driven + truck_2.miles_driven + truck_3.miles_driven
            print(f"\nTotal mileage of all trucks: {total_mileage:.2f} miles\n")

        elif choice == '3':
            print("Exiting viewer.")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.\n")

# Call the view_delivery_status function to allow the user to interact with the system
view_delivery_status()