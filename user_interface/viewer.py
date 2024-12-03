def view_delivery_status(package_table, truck_1, truck_2, truck_3):
    while True:
        print("--- Package Delivery Status Viewer ---")
        print("1. View package status by ID")
        print("2. View total mileage of all trucks")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                package_id = int(input("Enter the package ID: "))
                package = package_table.lookup(package_id)
                if package:
                    print(f"Package ID: {package['package_id']}")
                    print(f"Address: {package['address']}, {package['city']}, {package['zip_code']}")
                    print(f"Deadline: {package['deadline']}")
                    print(f"Weight: {package['weight']} kg")
                    print(f"Status: {package['status']}")
                else:
                    print("Package not found.")
            except ValueError:
                print("Invalid package ID. Please enter a numeric value.")

        elif choice == '2':
            total_mileage = truck_1.miles_driven + truck_2.miles_driven + truck_3.miles_driven
            print(f"Total mileage of all trucks: {total_mileage:.2f} miles")

        elif choice == '3':
            print("Exiting viewer.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
