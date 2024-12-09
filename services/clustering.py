def assign_packages_to_clusters(package_table, location_indices, max_capacity=16):
    """
    Assign packages to clusters manually based on address proximity. Validate clusters for truck capacity.

    :param package_table: HashTable containing all package data
    :param location_indices: Dictionary mapping addresses to indices in the distance data
    :param max_capacity: Maximum capacity per truck (default is 16)
    :return: Tuple of truck package lists (truck_1_packages, truck_2_packages, truck_3_packages, special_case_packages)
    """
    # Define clusters based on manual proximity analysis
    cluster_1 = ["4001 South 700 East", "195 W Oakland Ave", "1330 2100 S",
                 "177 W Price Ave", "2530 S 500 E", "300 State St", "3595 Main St"]
    cluster_2 = ["1060 Dalton Ave S", "233 Canyon Rd", "2010 W 500 S",
                 "1488 4800 S", "2600 Taylorsville Blvd", "2835 Main St", "3365 S 900 W"]
    cluster_3 = ["2300 Parkway Blvd", "410 S State St", "3148 S 1100 W",
                 "5025 State St", "5100 South 2700 West", "6351 South 900 East"]

    # Assign packages to clusters
    truck_1_packages = []
    truck_2_packages = []
    truck_3_packages = []
    special_case_packages = []

    for package_id in range(1, 41):  # Assuming 40 packages in total
        package = package_table.lookup(package_id)
        if package:
            address = package['address'].strip()
            print(f"Processing package {package_id} with address: {address}")
            if address in cluster_1:
                truck_1_packages.append(package_id)
                print(f"Assigned package {package_id} to Truck 1 (Cluster 1).")
            elif address in cluster_2:
                truck_2_packages.append(package_id)
                print(f"Assigned package {package_id} to Truck 2 (Cluster 2).")
            elif address in cluster_3:
                truck_3_packages.append(package_id)
                print(f"Assigned package {package_id} to Truck 3 (Cluster 3).")
            else:
                special_case_packages.append(package_id)
                print(f"Package {package_id} could not be assigned to a cluster. Added to special cases.")

    # Validate clusters for capacity
    if len(truck_1_packages) > max_capacity or len(truck_2_packages) > max_capacity or len(truck_3_packages) > max_capacity:
        print("Warning: Clusters exceed truck capacity. Attempting redistribution...")
        truck_1_packages, truck_2_packages, truck_3_packages = balance_clusters(
            [truck_1_packages, truck_2_packages, truck_3_packages], max_capacity)

    return truck_1_packages, truck_2_packages, truck_3_packages, special_case_packages

def balance_clusters(clusters, max_capacity):
    """
    Redistribute packages between clusters to balance them under the max capacity.

    :param clusters: List of clusters (list of lists of package IDs)
    :param max_capacity: Maximum capacity per truck
    :return: Balanced clusters
    """
    # Flatten all clusters into one list of packages
    all_packages = [pkg for cluster in clusters for pkg in cluster]
    redistributed_clusters = [[] for _ in clusters]

    print("\nRedistributing packages to balance clusters...")

    # Distribute packages evenly across clusters
    for i, package in enumerate(all_packages):
        cluster_index = i % len(clusters)
        redistributed_clusters[cluster_index].append(package)

    # Print redistributed clusters for debugging
    for i, cluster in enumerate(redistributed_clusters):
        print(f"Cluster {i + 1} after redistribution: {cluster}")
        if len(cluster) > max_capacity:
            print(f"Warning: Cluster {i + 1} still exceeds max capacity with {len(cluster)} packages.")

    return redistributed_clusters

def reassign_special_packages(
    special_case_packages,
    truck_1_packages,
    truck_2_packages,
    truck_3_packages,
    package_table,
    location_indices,
    distance_data,
    get_distance,
    max_capacity=16,
):
    print("\nReassigning special-case packages...")
    for package_id in special_case_packages[:]:  # Iterate over a copy
        package = package_table.lookup(package_id)
        if package:
            address = package['address']
            address_index = location_indices.get(address)

            if address_index is not None:
                # Prioritize trucks dynamically based on capacity and deadline proximity
                distances = [
                    (get_distance(0, address_index), len(truck_1_packages), "Truck 1"),
                    (get_distance(0, address_index), len(truck_2_packages), "Truck 2"),
                    (get_distance(0, address_index), len(truck_3_packages), "Truck 3"),
                ]

                # Sort trucks by nearest distance and available capacity
                sorted_trucks = sorted(distances, key=lambda x: (x[0], x[1]))

                for distance, capacity, truck in sorted_trucks:
                    if capacity < max_capacity:
                        print(f"Package {package_id} reassigned to {truck} based on proximity and capacity.")
                        if truck == "Truck 1":
                            truck_1_packages.append(package_id)
                        elif truck == "Truck 2":
                            truck_2_packages.append(package_id)
                        elif truck == "Truck 3":
                            truck_3_packages.append(package_id)
                        special_case_packages.remove(package_id)
                        break
                else:
                    print(f"Package {package_id} could not be reassigned. Leaving at hub.")