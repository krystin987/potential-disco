from datetime import datetime, timedelta

class Truck:
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []  # Packages currently loaded
        self.unloaded_packages = []  # Packages left due to full capacity
        self.current_location_index = 0
        self.speed = 18  # Speed in miles per hour
        self.miles_driven = 0.0
        self.start_time = datetime.strptime("08:00 AM", "%I:%M %p")
        self.current_time = self.start_time

    def return_to_hub(self, get_distance, current_time):
        """Return the truck to the hub."""
        if self.current_location_index != 0:  # Not at the hub
            print(f"Truck {self.truck_id} returning to hub.")
            distance_to_hub = get_distance(self.current_location_index, 0)
            travel_time_to_hub = timedelta(hours=distance_to_hub / self.speed)
            self.current_time = current_time + travel_time_to_hub
            self.miles_driven += distance_to_hub
            self.current_location_index = 0
            print(
                f"Truck {self.truck_id} arrived at hub at {self.current_time.strftime('%I:%M %p')}, total miles driven: {self.miles_driven:.2f}")

    def load_packages(self, package_ids, package_table, current_time):
        for package_id in package_ids:
            if len(self.packages) < 16:  # Check capacity
                self.packages.append(package_id)
                package = package_table.lookup(package_id)
                if package:
                    package['start_time'] = current_time.strftime("%I:%M %p")
                    package['status'] = "En route"
                print(f"Truck {self.truck_id}: Loaded package {package_id} at {current_time.strftime('%I:%M %p')}")
            else:
                print(f"Truck {self.truck_id} is full. Cannot load package {package_id}.")
                self.unloaded_packages.append(package_id)  # Record unloaded packages

    def reload_packages(self, package_table, location_indices, distance_data, get_distance):
        print(f"Truck {self.truck_id} returning to hub to reload leftover packages.")
        self.current_location_index = 0  # Simulate returning to hub
        for package_id in self.unloaded_packages[:]:
            if len(self.packages) < 16:  # Try reloading
                self.packages.append(package_id)
                package = package_table.lookup(package_id)
                if package:
                    package['status'] = "En route"
                print(f"Truck {self.truck_id}: Reloaded package {package_id}.")
                self.unloaded_packages.remove(package_id)  # Remove from unloaded
            else:
                break

    def deliver_packages(self, package_table, location_indices, get_distance, distance_data, stop_time=None):
        for package_id in self.packages:
            package = package_table.lookup(package_id)
            if not package or package['status'].startswith("Delivered"):
                continue  # Skip missing or already delivered packages

            package_address = package['address']
            package_location_index = location_indices.get(package_address)
            if package_location_index is None or package_location_index >= len(distance_data):
                continue  # Skip invalid package addresses

            # Calculate travel time
            distance = get_distance(self.current_location_index, package_location_index)
            travel_time = timedelta(hours=distance / self.speed)
            potential_time = self.current_time + travel_time

            # Stop if the delivery goes past the stop_time
            if stop_time and potential_time > stop_time:
                break

            # Deliver the package
            self.current_time = potential_time  # Update truck's current time
            self.miles_driven += distance
            self.current_location_index = package_location_index

            delivery_time = self.current_time.strftime("%I:%M %p")
            self.update_package_status(package_table, package_id, delivery_time)
            print(
                f"Truck {self.truck_id}: Delivered package {package_id} at {delivery_time}, total miles driven: {self.miles_driven:.2f}")

    @staticmethod
    def update_package_status(package_table, package_id, delivery_time):
        """Update the status of a delivered package in the package table."""
        package = package_table.lookup(package_id)
        if package:
            package['status'] = f"Delivered at {delivery_time}"
            package['delivery_time'] = delivery_time
        else:
            print(f"Package {package_id} not found.")

    # Truck class method
    def deliver_single_package(self, package_id, package_table, location_indices, get_distance, distance_data,
                               current_time):
        package = package_table.lookup(package_id)
        if package and package['status'] == "At the hub":
            location_index = location_indices[package['address']]
            distance = get_distance(self.current_location_index, location_index)
            travel_time = timedelta(hours=distance / self.speed)
            self.current_time = current_time + travel_time
            self.miles_driven += distance
            self.current_location_index = location_index

            delivery_time = self.current_time.strftime('%I:%M %p')
            package['status'] = f"Delivered at {delivery_time}"
            package['delivery_time'] = delivery_time
            print(
                f"Truck {self.truck_id}: Delivered package {package_id} at {delivery_time}, total miles driven: {self.miles_driven:.2f}")

    def clear_packages(self):
        self.packages = []
        print(f"Truck {self.truck_id}: Cleared all packages after delivery.")

    def get_mileage(self):
        return self.miles_driven
