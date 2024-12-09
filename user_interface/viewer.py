from datetime import datetime
import re


# Helper function to normalize user time input (e.g., accepting lower case or input without periods)
def normalize_time_input(input_time):
    # Remove unnecessary characters (spaces, dots, colons) and make lowercase
    input_time = re.sub(r"[ .:]", "", input_time).lower()

    # Match against common time formats (e.g., 10am, 1000am, 10:00am)
    if "am" in input_time or "pm" in input_time:
        # Extract the numerical part and am/pm suffix
        time_part = re.sub(r"\D", "", input_time)
        period = "am" if "am" in input_time else "pm"

        # Handle different lengths of time_part (e.g., 10 vs 1000)
        if len(time_part) == 1 or len(time_part) == 2:
            # Assume it's an hour only (e.g., 10am, 3pm)
            formatted_time = f"{time_part}:00 {period.upper()}"
        elif len(time_part) == 3 or len(time_part) == 4:
            # Handle hour and minute (e.g., 930am, 0945pm)
            hour = time_part[:-2]
            minute = time_part[-2:]
            formatted_time = f"{hour}:{minute} {period.upper()}"
        else:
            raise ValueError("Invalid time format")
    else:
        raise ValueError("Invalid time format")

    return formatted_time


# Helper function to determine package status at a given time
def get_package_status_at_time(package, user_time):
    if 'delivery_time' in package and package['delivery_time']:
        delivery_time = datetime.strptime(package['delivery_time'], "%I:%M %p")
        if user_time >= delivery_time:
            return f"Delivered at {package['delivery_time']}"
    if 'start_time' in package and package['start_time'] != "At the hub":
        start_time = datetime.strptime(package['start_time'], "%I:%M %p")
        if user_time >= start_time:
            return "En route"
    return "At the hub"


def view_delivery_status(package_table, truck_1, truck_2, truck_3):
    while True:
        print("\n--- Package Delivery Status Viewer ---")
        print("1. View package status at a specific time")
        print("2. View package status by ID")
        print("3. View total mileage of all trucks")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            # User inputs time to check the status of all packages
            input_time = input("Enter the time (e.g., 10:20am or 3:45pm): ").strip().lower()
            try:
                # Normalize time input to match our data format (e.g., 08:00 AM)
                normalized_time = normalize_time_input(input_time)
                user_time = datetime.strptime(normalized_time, "%I:%M %p")

                print(f"\n--- Package Status at {normalized_time} ---")
                for package_id in range(1, package_table.size + 1):
                    package = package_table.lookup(package_id)
                    if package:
                        delivery_status = get_package_status_at_time(package, user_time)
                        print(f"Package ID: {package['package_id']}, Address: {package['address']}, "
                              f"Deadline: {package['deadline']}, Status: {delivery_status}")

            except ValueError:
                print("Invalid time format. Please enter the time in a valid format (e.g., 10:20am or 3:45pm).")

        elif choice == '2':
            # User inputs package ID to view its current status
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

        elif choice == '3':
            # View the total mileage of all trucks
            total_mileage = truck_1.get_mileage() + truck_2.get_mileage() + truck_3.get_mileage()
            print(f"\nTotal mileage of all trucks: {total_mileage:.2f} miles")

        elif choice == '4':
            # Exit the viewer
            print("Exiting viewer.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")