import datetime


def find_nearest_neighbor(current_location, destinations, weight_matrix):
    """
    Find the nearest neighbor (the closest destination) from the current location.

    :param current_location: The current location of the truck.
    :param destinations: A set of remaining destinations.
    :param weight_matrix: The nested dictionary representing distances between locations.
    :return: The closest destination.
    """
    # Initialize the default conditions.
    closest_destination = None
    min_distance = float('inf')

    for destination in destinations:  # Destinations is a set that is an attribute of the truck.
        distance = weight_matrix[current_location][destination]
        if distance < min_distance:
            min_distance = distance
            closest_destination = destination

    return closest_destination


def nearest_neighbor_routing(truck, weight_matrix):
    """
    Executes a single round of routing based on the Nearest Neighbor Algorithm.
    Updates mileage and time as well as deliver packages as it routes.
    The route will prioritize depending on if the truck has time sensitive destinations.

    :param truck: The truck object whose route is being planned.
    :param weight_matrix: The 2D weight matrix representing distances between locations.
    """
    # Determine if this round of routing should prioritize time-sensitivity.
    # If time_sensitive_destinations is 0, then either this truck is not time-sensitive or it has already completed
    # its time-sensitive route.
    destinations = truck.time_sensitive_destinations if len(truck.time_sensitive_destinations) > 0 \
        else truck.destinations

    current_location = truck.current_location

    while len(destinations) > 0:  # While there are still places to go
        # Find the next nearest location.
        next_destination = find_nearest_neighbor(current_location, destinations, weight_matrix)
        if next_destination is not None:  # Error handling
            # Set truck's current location to this new destination and update the mileage and time.
            truck.update_mileage_and_time(next_destination, weight_matrix)

            for package in list(truck.cargo):  # Safely iterate over the cargo list because it will be modified.
                # Deliver all packages with a matching destination address to this location.
                if package.destination_address == truck.current_location:
                    truck.deliver_package(package, truck.current_location)
            current_location = truck.current_location  # Update current location for the while loop.
        else:
            break


def test_route_planning(truck, weight_matrix):
    """
    Execute a hypothetical route planning for a given truck during the loading phase.
    This function simulates the route without delivering the packages.

    :param truck: The truck object being loaded.
    :param weight_matrix: The 2D weight matrix representing distances between locations.
    :return: The total time taken to complete the hypothetical route.
    """
    destinations = truck.destinations  # This test route only applies to early morning, non-time-sensitive trucks.
    # Create temporary copies of destinations and time for simulation so that actual attributes are not changed.
    temp_destinations = destinations.copy()
    temp_current_time = truck.current_time

    current_location = truck.current_location

    while temp_destinations:  # Simulate Nearest Neighbor Algorithm.
        next_destination = find_nearest_neighbor(current_location, temp_destinations, weight_matrix)
        if next_destination is not None:
            # Simulate the travel to the next destination and update the total time.
            # Do not call truck's update methods to avoid actually changing attributes.
            distance = weight_matrix[current_location][next_destination]
            travel_time = distance / truck.speed
            temp_current_time += datetime.timedelta(hours=travel_time)
            current_location = next_destination
            temp_destinations.remove(current_location)
        else:
            break  # No more reachable destinations

    # Simulate the return trip to the hub
    if current_location != 0:
        distance_to_hub = weight_matrix[current_location][0]
        travel_time_to_hub = distance_to_hub / truck.speed
        temp_current_time += datetime.timedelta(hours=travel_time_to_hub)

    return temp_current_time
