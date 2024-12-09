from datetime import datetime, timedelta


def update_package_address(package_table, package_id, new_address, current_time):
    """
    Update the address of a package in the hash table.
    :param current_time:
    :param package_table: HashTable containing all packages
    :param package_id: Unique identifier of the package
    :param new_address: Dictionary with new address details
    """
    package = package_table.lookup(package_id)
    if package:
        package['address'] = new_address['address']
        package['city'] = new_address['city']
        package['zip_code'] = new_address['zip_code']
        print(f"Package {package_id} address updated to: {new_address['address']}, {new_address['city']}, {new_address['zip_code']} at {current_time.strftime('%I:%M %p')}.")

def handle_package_nine(package_table, corrected_address, truck_1, current_time, location_indices, get_distance, distance_data):
    """
    Handles the address correction, loading, and delivery of Package 9 after the address is updated at 10:20 AM.
    Ensures Truck 1 returns to the hub if not already there.
    :param package_table: HashTable containing all packages
    :param corrected_address: Dictionary with corrected address details
    :param truck_1: Truck instance handling Package 9
    :param current_time: Current simulation time
    :param location_indices: Dictionary mapping addresses to distance table indices
    :param get_distance: Function to calculate distance between locations
    :param distance_data: Distance data for locations
    :return: Updated current_time after handling Package 9
    """
    update_time = datetime.strptime("10:20 AM", "%I:%M %p")

    # Perform address correction and prepare for Package 9 delivery
    package_9 = package_table.lookup(9)
    if package_9 and not package_9['status'].startswith("Delivered"):
        if current_time < update_time:
            current_time = update_time
            print("\n--- Address Correction at 10:20 AM ---")
            update_package_address(package_table, 9, corrected_address, current_time)

        # Ensure Truck 1 is at the hub before loading package 9
        if truck_1.current_location_index != 0:  # Not at the hub
            print(f"Truck {truck_1.truck_id} returning to hub to load package 9.")
            distance_to_hub = get_distance(truck_1.current_location_index, 0)
            travel_time_to_hub = distance_to_hub / truck_1.speed
            current_time += timedelta(hours=travel_time_to_hub)
            truck_1.miles_driven += distance_to_hub
            truck_1.current_location_index = 0
            print(f"Truck {truck_1.truck_id} arrived at hub at {current_time.strftime('%I:%M %p')}, total miles driven: {truck_1.miles_driven:.2f}")

        # Load Package 9 onto Truck 1 and attempt delivery
        truck_1.load_packages([9], package_table, current_time)
        print(f"Truck {truck_1.truck_id}: Loaded package 9 at {current_time.strftime('%I:%M %p')}")
        truck_1.deliver_single_package(9, package_table, location_indices, get_distance, distance_data, current_time)

    return current_time