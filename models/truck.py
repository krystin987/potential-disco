from datetime import datetime, timedelta
from services.delivery import deliver_package

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

    def deliver_packages(self, package_table):
        for package_id in self.packages:
            # Simulate driving to the package location and delivering
            # For simplicity, we'll assume each delivery takes 15 minutes
            self.miles_driven += 5.0  # Increment miles driven by 5 miles per delivery
            print(
                f"Truck {self.truck_id}: Delivered package {package_id}, total miles driven (debug): {self.miles_driven}")

            delivery_time = self.current_time.strftime("%I:%M %p")
            deliver_package(package_table, package_id, delivery_time)
            self.current_time += timedelta(minutes=15)
