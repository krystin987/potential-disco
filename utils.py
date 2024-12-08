def update_package_address(package_table, package_id, new_address):
    """
    Update the address of a package in the hash table.
    :param package_table: HashTable containing all packages
    :param package_id: Unique identifier of the package
    :param new_address: Dictionary with new address details
    """
    package = package_table.lookup(package_id)
    if package:
        package['address'] = new_address['address']
        package['city'] = new_address['city']
        package['zip_code'] = new_address['zip_code']
        print(f"Package {package_id} address updated to: {new_address['address']}, {new_address['city']}, {new_address['zip_code']}.")