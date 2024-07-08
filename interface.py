import datetime
from package import look_up


def user_interface(package_objects, trucks, index_to_address, hash_table):
    """
    User interface loop for package status lookup and total mileage display.

    :param package_objects: Dictionary of package objects.
    :param trucks: Dictionary of truck objects.
    :param index_to_address: Dictionary that maps indices to addresses.
    :param hash_table: A hash table containing the initial data.
    """
    while True:
        print("\nCommands: \n 1. Lookup Package Status (Enter 'lookup') \n 2. View Total Mileage (Enter 'mileage') \n "
              "3. View Status of All Packages at Specific Time (Enter 'status') \n 4. Exit (Enter 'exit')")
        command = input("Enter command: ").lower()

        # Single package lookup inquiry.
        if command == 'lookup':
            package_id = input("Enter package ID: ")
            if package_id not in package_objects:
                print("Invalid package ID. Please try again.")  # User error handling.
                continue
            time_input = input("Enter time (HH:MM format): ")
            try:
                hour, minute = map(int, time_input.split(':'))
                # Convert to datetime for comparison purposes.
                specific_time = datetime.datetime(2023, 1, 1, hour, minute)
            except ValueError:
                print("Invalid time format. Please enter time in HH:MM format.")  # User error handling.
                continue

            lookup_package_status_at_time(package_objects, package_id, specific_time, index_to_address, hash_table,
                                          trucks)

        # Fleet mileage inquiry.
        elif command == 'mileage':
            display_total_mileage(trucks)

        # Status of all packages inquiry.
        elif command == 'status':
            time_input = input("Enter time (HH:MM format): ")
            try:
                hour, minute = map(int, time_input.split(':'))
                specific_time = datetime.datetime(2023, 1, 1, hour, minute)
            except ValueError:
                print("Invalid time format. Please enter time in HH:MM format.")
                continue

            display_all_packages_status_at_time(package_objects, specific_time, trucks)

        # End program.
        elif command == 'exit':
            break
        else:
            print("Invalid command. Please try again.")


def lookup_package_status_at_time(package_objects, package_id, specific_datetime, index_to_address, hash_table, trucks):
    """
    Displays the status of a package at a specific datetime.

    :param package_objects: Dictionary of package objects.
    :param package_id: The ID of the package to look up.
    :param specific_datetime: The specific datetime to check the package status.
    :param index_to_address: A dictionary that maps location indices to addresses.
    :param hash_table: A hash table storing the initial data.
    :param trucks: A dictionary containing truck objects.
    """
    # Get package info.
    package_info = look_up(package_id, package_objects)
    if package_info:  # Error handling.
        package = package_objects[package_id]

        address = index_to_address.get(package_info['Address'])
        city = package_info['City']
        zip_code = package_info['Zip']

        if package.delivery_time <= specific_datetime:
            # Package has been delivered by user time.
            status = f"Delivered at {package.delivery_time.strftime('%H:%M %p')}"
        # If the package has been loaded but not delivered by user time.
        elif specific_datetime >= package.load_time:
            if package.truck == 3:
                if specific_datetime < trucks[3].start_time:
                    # Truck 3 has not left the hub yet.
                    status = f"'Loaded' on Truck 3 and waiting at hub since {package.load_time.strftime('%H:%M %p')}."
                else:
                    # Truck 3 is making deliveries.
                    status = f"En route on Truck 3 since {trucks[3].start_time.strftime('%H:%M %p')}."
            else:
                # Package is being delivered.
                status = f"En route on Truck {package.truck} since {package.load_time.strftime('%H:%M %p')}."
        # If the package has not been loaded because the user specified a time before the start of the day...
        else:
            status = "At the hub"

        # Handle wrong address packages to reflect what the address would read at certain times of the day.
        # If user time is before the correction time.
        if specific_datetime < datetime.datetime(2023, 1, 1, 10, 20):
            # Search the original hash table for the original delivery address.
            package_data = hash_table.search(package_id)
            if package_data[7] == "Wrong address listed":
                # Override with original delivery address if this is a wrong address package.
                address = package_data[1]
                city = package_data[2]
                zip_code = package_data[4]

        print(f"Package ID: {package_info['ID']}, "
              f"Address: {address},"
              f" City: {city}, "
              f"Zip: {zip_code}, "
              f"Deadline: {package_info['Deadline']}, "
              f"Weight: {package_info['Weight']}, "
              f"Status at {specific_datetime.strftime('%H:%M %p')}: {status}")
    else:
        print(f"No package found with ID {package_id}.")  # Error handling.


def display_all_packages_status_at_time(package_objects, specific_time, trucks):
    """
    Displays the status of all packages at a specific time.

    :param package_objects: Dictionary of package objects.
    :param specific_time: The specific time to check the packages' status.
    :param trucks: List of truck objects.
    """
    truck_cargo_status = {truck_id: [] for truck_id in trucks.keys()}  # Initiate truck cargo lists.
    delivered_packages = []  # Initiate delivered packages list.
    unloaded_packages = []  # Initiate unloaded packages list.

    # Sort packages into display lists.
    for package in package_objects.values():
        # Delivered packages.
        if package.delivery_time and package.delivery_time <= specific_time:
            delivered_packages.append(package.package_id)
        # Packages currently on trucks.
        elif package.truck is not None and specific_time >= package.load_time:
            truck_cargo_status[package.truck].append(package.package_id)
        # Packages that are not loaded nor delivered.
        elif specific_time <= package.load_time:
            unloaded_packages.append(package.package_id)

    # Sort the package lists for easy checking.
    for truck_id in truck_cargo_status:
        truck_cargo_status[truck_id].sort(key=lambda x: int(x))
    delivered_packages.sort(key=lambda x: int(x))
    unloaded_packages.sort(key=lambda x: int(x))

    # Display truck cargo status
    for truck_id, cargo in truck_cargo_status.items():
        print(f"Truck {truck_id} cargo at {specific_time.strftime('%H:%M %p')}: {', '.join(map(str, cargo))}")

    # Display delivered packages
    print(f"Delivered packages by {specific_time.strftime('%H:%M %p')}: {', '.join(map(str, delivered_packages))}")

    # Display unloaded packages
    print(f"Unloaded packages by {specific_time.strftime('%H:%M %p')}: {', '.join(map(str, unloaded_packages))}")


def display_total_mileage(trucks):
    """
    Displays the total mileage traveled by all trucks.

    :param trucks: Dictionary of truck objects.
    """
    total_mileage = 0
    for truck_id, truck in trucks.items():
        total_mileage += truck.mileage
        # Display individual truck mileage.
        print(f"Truck {truck_id} Mileage: {round(truck.mileage, 1)} miles")
    # Display fleet mileage.
    print(f"Total Mileage by All Trucks: {round(total_mileage, 1)} miles")


def print_all_packages_eod(package_objects):
    """
    Prints all package information at the EOD. Used for debugging purposes.

    :param package_objects: List of package objects.
    """
    # Sort package objects by package ID
    sorted_packages = sorted(package_objects.values(), key=lambda p: int(p.package_id))

    for package in sorted_packages:
        # Check if the package has been delivered
        if package.delivery_time:
            # Format the delivery time to a string
            delivery_time_str = package.delivery_time.strftime("%I:%M %p")

            # Initialize delivered_on_time as "Yes" for EOD or if there's no specific deadline
            delivered_on_time = "Yes" if package.delivery_deadline == "EOD" or not package.delivery_deadline else "No"

            # If there's a specific deadline (not EOD), compare delivery time and deadline
            if package.delivery_deadline and package.delivery_deadline != "EOD":
                # Convert deadline to datetime.datetime object if it's a string
                if isinstance(package.delivery_deadline, str):
                    deadline_time = datetime.datetime.combine(package.delivery_time.date(),
                                                              datetime.datetime.strptime(package.delivery_deadline,
                                                                                         "%I:%M %p").time())
                else:
                    deadline_time = datetime.datetime.combine(package.delivery_time.date(), package.delivery_deadline)

                # Check if delivered before the deadline
                delivered_on_time = "Yes" if package.delivery_time <= deadline_time else "No"

            # Compare package's destination address to the location stamp when it was delivered.
            delivered_to_correct_address = "Yes" if package.destination_address == package.delivered_to else "No"

            print(f"ID: {package.package_id}, "
                  f"Correct Address: {delivered_to_correct_address}, "
                  f"Deadline: {package.delivery_deadline}, "
                  f"Delivery: {delivery_time_str}, "
                  f"On Time: {delivered_on_time}")
