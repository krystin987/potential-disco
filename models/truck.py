from datetime import datetime, timedelta

class Truck:
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []  # List of package IDs assigned to this truck
        self.current_location_index = 0  # Starting point: WGUPS Hub (index 0)
        self.speed = 18  # Speed in miles per hour
        self.miles_driven = 0.0
        self.start_time = datetime.strptime("08:00 AM", "%I:%M %p")
        self.current_time = self.start_time

    def load_packages(self, package_ids):
        for package_id in package_ids:
            if len(self.packages) < 16:
                self.packages.append(package_id)
                print(f"Truck {self.truck_id}: Loaded package {package_id}")
            else:
                print(f"Truck {self.truck_id} is full. Cannot load package {package_id}.")

    def deliver_packages(self, package_table, location_indices, get_distance):
        for package_id in self.packages:
            package = package_table.lookup(package_id)
            if not package:
                print(f"Package {package_id} not found.")
                continue

            package_address = package['address']
            if package_address in location_indices:
                package_location_index = location_indices[package_address]
                distance = get_distance(self.current_location_index, package_location_index)

                if distance == float('inf'):
                    print(f"Skipping delivery for package {package_id} due to invalid location indices.")
                    continue

                travel_time = timedelta(hours=distance / self.speed)
                self.current_time += travel_time
                self.miles_driven += distance
                self.current_location_index = package_location_index

                delivery_time = self.current_time.strftime("%I:%M %p")
                self.update_package_status(package_table, package_id, delivery_time)
                print(
                    f"Truck {self.truck_id}: Delivered package {package_id}, total miles driven: {self.miles_driven:.2f}")
            else:
                print(f"Address for package {package_id} not found in location index mapping.")

    def update_package_status(self, package_table, package_id, delivery_time):
        package = package_table.lookup(package_id)
        if package:
            package['status'] = f"Delivered at {delivery_time}"
            print(f"Package {package_id} delivered at {delivery_time}.")
        else:
            print(f"Package {package_id} not found.")

    def clear_packages(self):
        self.packages = []
        print(f"Truck {self.truck_id}: Cleared all packages after delivery.")

    def get_mileage(self):
        return self.miles_driven