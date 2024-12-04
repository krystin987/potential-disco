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

    def load_package(self, package_id):
        if len(self.packages) < 16:
            self.packages.append(package_id)
            print(f"Truck {self.truck_id}: Loaded package {package_id} at {self.current_time.strftime('%I:%M %p')}")
        else:
            print(f"Truck {self.truck_id} is full. Cannot load package {package_id}.")

    def load_packages_time_slot(self, package_ids, start_time):
        """
        Load packages onto the truck during a specific time slot.
        :param package_ids: List of package IDs to load
        :param start_time: The starting time of the loading slot
        """
        self.current_time = start_time
        for package_id in package_ids:
            self.load_package(package_id)

    def deliver_packages(self, package_table, location_indices, get_distance):
        for package_id in self.packages:
            package = package_table.lookup(package_id)
            if not package:
                print(f"Package {package_id} not found.")
                continue

            package_address = package['address']
            if package_address in location_indices:
                package_location_index = location_indices[package_address]
                distance_to_location = get_distance(self.current_location_index, package_location_index)
                travel_time = timedelta(hours=distance_to_location / self.speed)
                self.current_time += travel_time
                self.miles_driven += distance_to_location
                self.current_location_index = package_location_index

                delivery_time = self.current_time.strftime("%I:%M %p")
                package['status'] = f"Delivered at {delivery_time}"
                print(f"Truck {self.truck_id}: Delivered package {package_id} at {delivery_time}, total miles driven: {self.miles_driven:.2f}")
            else:
                print(f"Address for package {package_id} not found in location index mapping.")

    def get_mileage(self):
        return self.miles_driven

    def clear_packages(self):
        self.packages = []
        print(f"Truck {self.truck_id} has been unloaded and is now ready for the next load.")
