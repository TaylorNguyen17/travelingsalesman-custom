from routing import *


class Truck:
    def __init__(self, truck_id, starting_location=0, start_time=None, is_time_sensitive=False, speed=18, capacity=16):
        # is_time_sensitive refers to if the truck runs two separate routes, one for time-sensitive packages
        # and one for non-time-sensitive packages.
        self.truck_id = truck_id
        self.current_location = starting_location  # Default: location 0, the hub.
        self.cargo = []  # List of packages.
        self.mileage = 0
        self.start_time = start_time
        self.current_time = start_time  # The truck's internal clock. Use for timestamping.
        self.is_time_sensitive = is_time_sensitive  # Default: False.
        self.speed = speed  # Default: 18
        self.capacity = capacity  # Default: 16.
        self.destinations = set()  # Set of destinations to visit.
        self.time_sensitive_destinations = set()  # Subset of destinations to visit first.

    def load_package(self, package):
        """
        Load package onto truck, update package's attributes,
        and add package's delivery address to truck's destinations.

        :param package: Package object.
        """
        # Update package attributes.
        package.delivery_status = f'en route on truck {self.truck_id}'
        package.truck = self.truck_id

        self.cargo.append(package)  # Add package to cargo list.

        # Update truck's destinations sets.
        destination = package.destination_address
        if package.destination_address is not None:  # Don't add null addresses to the destination sets.
            if self.is_time_sensitive and package.delivery_deadline != "EOD":
                self.time_sensitive_destinations.add(destination)  # Note: Will be subset of destinations.
            self.destinations.add(destination)  # Add package's destination to truck's destinations.

    def deliver_package(self, package, location):
        """
        Deliver package by updating package attributes and discard the location from truck's destinations.

        :param package: Package object.
        :param location: Current location.
        """
        # Update package attributes.
        package.delivery_status = f'delivered at {self.current_time.strftime("%H:%M %p")}'
        package.delivery_time = self.current_time
        package.delivered_to = location

        # Discard current location from the destination sets
        self.destinations.discard(self.current_location)
        if self.current_location in self.time_sensitive_destinations:
            self.time_sensitive_destinations.discard(self.current_location)  # Discard prevents key error.

        self.cargo.remove(package)  # Remove the package from the cargo.

    def update_mileage_and_time(self, next_destination, distance_matrix):
        """
        Update the truck's mileage based on the next destination.
        Next destination calculation is easier than previous destination because previous destination data
        is not stored.

        Also set next destination as current location, simulating movement.

        Also update the truck's internal clock, simulating the passage of time.

        :param next_destination: Next destination.
        :param distance_matrix: Either a 2D weight matrix or a nested dictionary.
        """
        # Calculate travel distance and time based on current location and next destination.
        distance = distance_matrix[self.current_location][next_destination]
        travel_time = distance / self.speed

        self.mileage += distance  # Update the mileage.

        self.current_location = next_destination  # Update the current location.

        if self.current_time:  # Error handling: time cannot be updated if time has not been initialized.
            self.current_time += datetime.timedelta(hours=travel_time)  # Update the truck's internal clock.

    def return_to_hub(self, hub_location, distance_matrix):
        """
        Method to return truck to a specified location, for code readability.

        :param hub_location: The location ID of the hub.
        :param distance_matrix: The weight matrix.
        """
        self.update_mileage_and_time(hub_location, distance_matrix)  # Simulates travel by updating mileage and time.

    def print_status(self):
        """
        Debugging code. Prints all important attributes.

        """
        print(f"Truck ID: {self.truck_id}")
        print(f"Current Location: {self.current_location}")
        print(f"Mileage: {self.mileage:.2f} miles")  # Display mileage up to two decimal places
        print(f"Speed: {self.speed} mph")
        print(f"Capacity: {self.capacity} packages")
        print(f"Start Time: {self.start_time.strftime('%H:%M %p')}") if self.start_time else print(
            "Start Time: Not set")
        print(f"Current Time: {self.current_time.strftime('%H:%M %p')}") if self.current_time else print(
            "Current Time: Not set")
        print(f"Is Time Sensitive: {'Yes' if self.is_time_sensitive else 'No'}")
        print("Destinations:", self.destinations)
        print("Time-Sensitive Destinations:", self.time_sensitive_destinations)
        print("Cargo:")
        for package in self.cargo:
            print(
                f"  Package ID: {package.package_id}, "
                f"Destination: {package.destination_address}, "
                f"Delivery Status: {package.delivery_status}, "
                f"Delivery Time: {package.delivery_time}, "
                f"Delivery Deadline: {package.delivery_deadline}")

    def start_route(self, weight_matrix):
        """
        Set the start time of the route and also initializes the current time.

        """
        self.current_time = self.start_time
        nearest_neighbor_routing(self, weight_matrix)
