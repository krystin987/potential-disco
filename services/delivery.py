def deliver_package(package_table, package_id, delivery_time):
    """
    Updates the delivery status of a package.
    :param package_table: HashTable containing all packages
    :param package_id: Unique identifier of the package
    :param delivery_time: Time of delivery
    """
    package = package_table.lookup(package_id)
    if package:
        package['status'] = f"Delivered at {delivery_time}"
        print(f"Package {package_id} delivered at {delivery_time}.")
    else:
        print(f"Package {package_id} not found.")
