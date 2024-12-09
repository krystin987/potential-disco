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

def handle_package_nine(package_table, truck, corrected_address, current_time, location_indices, get_distance, distance_data):
    """
    Handles all operations for Package 9: address correction, hub return, loading, and delivery.
    """
    # Wait for address correction
    update_time = datetime.strptime("10:20 AM", "%I:%M %p")
    if current_time < update_time:
        print(f"Waiting for address correction at {update_time.strftime('%I:%M %p')}. Current time is {current_time.strftime('%I:%M %p')}.")
        current_time = update_time

    # Update Package 9's address
    package = package_table.lookup(9)
    if package:
        package.update(corrected_address)
        print(f"Package 9 address updated to: {corrected_address['address']}.")

    # Ensure Truck 1 is at the hub
    truck.return_to_hub(get_distance, current_time)

    # Load Package 9 and deliver it
    # print(f"Truck {truck.truck_id}: Loading Package 9 at {truck.current_time.strftime('%I:%M %p')}.")
    truck.load_packages([9], package_table, truck.current_time)
    truck.deliver_single_package(9, package_table, location_indices, get_distance, distance_data, truck.current_time)

    return truck.current_time