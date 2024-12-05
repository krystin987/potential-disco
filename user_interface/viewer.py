from datetime import datetime


def normalize_time_input(user_time_str):
    """
    Normalizes the user's time input to handle various formats.
    Examples:
    - "10am" -> "10:00 AM"
    - "1030 pm" -> "10:30 PM"
    - "10.30am" -> "10:30 AM"
    - "9:00 am" -> "09:00 AM"
    """
    # Remove any spaces, colons, or periods
    user_time_str = user_time_str.replace(" ", "").replace(".", "").replace(":", "")

    # Extract time and am/pm
    if "am" in user_time_str.lower():
        suffix = "AM"
        time_str = user_time_str.lower().replace("am", "")
    elif "pm" in user_time_str.lower():
        suffix = "PM"
        time_str = user_time_str.lower().replace("pm", "")
    else:
        raise ValueError("Invalid time format. Please include AM or PM.")

    # Pad with leading zero if necessary and add ":00" for whole hours
    if len(time_str) <= 2:
        time_str = f"{int(time_str):02d}:00"
    elif len(time_str) == 3:
        time_str = f"{time_str[0]}:{time_str[1:]}"
    elif len(time_str) == 4:
        time_str = f"{time_str[:2]}:{time_str[2:]}"
    else:
        raise ValueError("Invalid time format. Please enter a valid time.")

    # Return the formatted time with the appropriate suffix
    return f"{time_str} {suffix}"


def view_delivery_status(package_table, truck_1, truck_2, truck_3):
    while True:
        try:
            # Prompt user for a specific time to view the package statuses
            user_time_str = input("\nEnter the time to view package status (e.g., 10am, 1030pm, or 'exit' to quit): ")
            if user_time_str.lower() == 'exit':
                print("Exiting viewer.")
                break

            # Normalize the input time
            normalized_time_str = normalize_time_input(user_time_str)

            # Parse the normalized input time
            user_time = datetime.strptime(normalized_time_str, "%I:%M %p")

            print("\n--- Package Status at", normalized_time_str, "---")

            # Check the status of each package in the hash table
            for package_id in range(1, 41):  # Assuming 40 packages, with IDs from 1 to 40
                package = package_table.lookup(package_id)
                if not package:
                    continue

                # Determine the status of the package
                status = "At the hub"
                if package['status'].startswith("Delivered"):
                    delivery_time = datetime.strptime(package['status'].split(" at ")[1], "%I:%M %p")
                    if user_time >= delivery_time:
                        status = f"Delivered at {delivery_time.strftime('%I:%M %p')}"
                elif package['status'] == "En route":
                    status = "En route"

                # Display package information
                print(f"Package ID: {package_id}")
                print(f"Address: {package['address']}, {package['city']}, {package['zip_code']}")
                print(f"Deadline: {package['deadline']}")
                print(f"Weight: {package['weight']} kg")
                print(f"Status: {status}\n")

            # Calculate and display total mileage at the given time
            total_mileage = 0.0

            # Truck 1 mileage
            if truck_1.current_time <= user_time:
                total_mileage += truck_1.get_mileage()

            # Truck 2 mileage
            if truck_2.current_time <= user_time:
                total_mileage += truck_2.get_mileage()

            # Truck 3 mileage
            if truck_3.current_time <= user_time:
                total_mileage += truck_3.get_mileage()

            print(f"Total mileage of all trucks at {normalized_time_str}: {total_mileage:.2f} miles\n")

        except ValueError:
            print("Invalid time format. Please enter a valid time in the format 'hh:mm AM/PM' or similar.")