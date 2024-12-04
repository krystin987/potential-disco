# clustering.py

# Function to assign packages to clusters manually based on address proximity
def assign_packages_to_clusters(package_table, location_indices):
    # Define clusters based on manual proximity analysis
    cluster_1 = ["4001 South 700 East", "195 W Oakland Ave", "1330 2100 S", "177 W Price Ave", "2530 S 500 E", "300 State St", "3595 Main St"]
    cluster_2 = ["1060 Dalton Ave S", "233 Canyon Rd", "2010 W 500 S", "1488 4800 S", "2600 Taylorsville Blvd", "2835 Main St", "3365 S 900 W"]
    cluster_3 = ["2300 Parkway Blvd", "410 S State St", "3148 S 1100 W", "5025 State St", "5100 South 2700 West", "6351 South 900 East"]

    # Assign packages to clusters
    truck_1_packages = []
    truck_2_packages = []
    truck_3_packages = []

    for package_id in range(1, 41):
        package = package_table.lookup(package_id)
        if package:
            if package['address'] in cluster_1:
                truck_1_packages.append(package_id)
            elif package['address'] in cluster_2:
                truck_2_packages.append(package_id)
            elif package['address'] in cluster_3:
                truck_3_packages.append(package_id)

    return truck_1_packages, truck_2_packages, truck_3_packages