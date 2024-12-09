def optimize_route(truck, location_indices, get_distance, package_table):
    """
    Optimize the delivery route using a nearest-neighbor approach.

    :param truck: The truck instance with packages to deliver.
    :param location_indices: Dictionary mapping addresses to distance table indices.
    :param get_distance: Function to calculate distances between two locations.
    :param package_table: The hash table storing package details.
    :return: Optimized list of package IDs for delivery.
    """
    optimized_route = []
    current_location_index = 0  # Start at the hub

    while truck.packages:
        nearest_package = None
        min_distance = float('inf')

        for package_id in truck.packages:
            package = package_table.lookup(package_id)
            if not package:
                continue

            package_location_index = location_indices.get(package['address'])
            distance = get_distance(current_location_index, package_location_index)

            if distance < min_distance:
                nearest_package = package_id
                min_distance = distance

        # Add the nearest package to the optimized route
        optimized_route.append(nearest_package)
        truck.packages.remove(nearest_package)
        current_location_index = location_indices[package_table.lookup(nearest_package)['address']]

    return optimized_route