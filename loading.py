from routing import *


def load_high_priority_packages(trucks, package_objects, loading_list):
    """
    Load high-priority packages based on special instructions (Packages that must be on truck 2 or truck 3).

    :param trucks: Dictionary of truck objects keyed by truck ID.
    :param package_objects: Dictionary of package objects keyed by package ID.
    :param loading_list: List of package IDs to be loaded.
    """
    for package_id in loading_list[:]:  # Iterate over a copy to safely modify the original list
        package = package_objects[package_id]

        # Check for special instructions designating packages for Truck 2.
        if "Can only be on truck 2" in package.special_instructions:
            if can_load_package_and_group(package, trucks[2]):  # Cargo capacity check.
                # Load all associated packages.
                load_package_and_group(package_id, trucks[2], package_objects, loading_list)

        # Check for special instructions for delayed packages including wrong address packages to load onto Truck 3.
        elif "Delayed on flight---will not arrive to depot until 9:05 am" in package.special_instructions or \
                "Wrong address listed" in package.special_instructions:
            if can_load_package_and_group(package, trucks[3]):
                load_package_and_group(package_id, trucks[3], package_objects, loading_list)


# General helper function that determines if a group is too large to fit in the truck.
def can_load_package_and_group(package, truck):
    """
    Check if a package and its group can be loaded onto the truck without exceeding capacity.

    :param package: The package object being considered for loading.
    :param truck: The truck object.
    :return: True if the package and its group can be loaded, False otherwise.
    """
    total_group_size = 1  # Start with the current package
    # Combine both sets and subtract 1 to not count the current package
    combined_group = package.linked_packages.union(package.address_group)
    total_group_size += len(combined_group) - 1

    return len(truck.cargo) + total_group_size <= truck.capacity


# General helper function that loads package and all possible groupings.
def load_package_and_group(package_id, truck, package_objects, loading_list):
    """
    Load a package and its linked packages (both special instruction and same address) onto the truck.
    Look at the linked packages' linked packages and load those packages too.

    :param package_id: The package ID being loaded.
    :param truck: The truck object.
    :param package_objects: Dictionary of all package objects.
    :param loading_list: List of package IDs that need to be loaded.
    """

    package = package_objects[package_id]

    # Load the original package
    truck.load_package(package)
    loading_list.remove(package_id)

    # Load linked packages and their address groups
    if package.grouping:
        # Load all linked packages
        for linked_package_id in package.linked_packages:
            if linked_package_id in loading_list:
                linked_package = package_objects[linked_package_id]
                truck.load_package(package_objects[linked_package_id])
                loading_list.remove(linked_package_id)

                # Load address group members of the linked package
                for address_group_member_id in linked_package.address_group:
                    if address_group_member_id in loading_list and address_group_member_id != linked_package_id:
                        address_group_member = package_objects[address_group_member_id]
                        truck.load_package(address_group_member)
                        loading_list.remove(address_group_member_id)

    # Load address group members of the original package
    for linked_package_id in package.address_group:
        if linked_package_id in loading_list:
            truck.load_package(package_objects[linked_package_id])
            loading_list.remove(linked_package_id)
    # NOTE: This code does not scale well. If packages have a long chain of unique dependencies deeper than two layers,
    # this code will not add all the links together. Consider enhancing with a recursive function or another algorithm
    # such as a complete BFS or DFS to find the complete group. Such a code might require redesigning the dependencies
    # to be pointers to other objects rather than just a simple list of IDs.


def iteratively_load_truck_1(truck, weight_matrix, package_objects, loading_list, address_groups, min_load):
    """
    Iteratively loads packages onto Truck 1 based on proximity to the starting location and tests the route.
    Group packages are added only if their destinations are already in the truck's destinations or
    match the current location.

    :param truck: The Truck 1 object.
    :param weight_matrix: The weight matrix representing distances.
    :param package_objects: Dictionary of all package objects.
    :param loading_list: List of package IDs that need to be loaded.
    :param address_groups: Dictionary linking package IDs to their delivery addresses.
    :param min_load: The minimum cargo load before the function is allowed to return.
    :return: The updated Truck 1 object after loading.
    """
    # Sort locations by proximity to the hub.
    distances_from_hub = {index: distance for index, distance in enumerate(weight_matrix[0]) if index != 0}
    sorted_distances = sorted(distances_from_hub.items(), key=lambda x: x[1])

    for location_id, _ in sorted_distances:  # Start from the closest location.
        for package_id in address_groups[location_id]:  # Get the packages destined for this location.
            if package_id in loading_list:  # Check that these packages are unloaded.
                package = package_objects[package_id]  # Locate the package object with the package ID.
                # Check that the entire group has delivery addresses either at this location or at closer locations.
                if can_load_entire_group(package, truck, package_objects, location_id, sorted_distances):
                    # Load package and all linked packages.
                    load_package_and_group(package_id, truck, package_objects, loading_list)
                    # Simulate a round trip to see how long it would take.
                    return_time = check_return_time(truck, weight_matrix)
                    # If the minimum cargo load is met and the return time is later than 9:05 AM, then the cargo list
                    # is finalized. Else, continue to load.
                    if len(truck.cargo) >= min_load and return_time > datetime.time(9, 5):
                        return truck
                else:
                    break  # This location's packages are ineligible to be loaded.
            else:
                break  # This location's packages have already been loaded
    return truck


# Helper function for truck 1 loading: checking whether the group member's destination is within the current acceptable
# range. The acceptable range is defined as a distance equal to or closer than the current location being explored.
def can_load_group_member(package_id, package_objects, truck, location_id, sorted_distances):
    """
    Determines is a package's destination address is closer than the current location being explored for loading.

    :param package_id: The package ID.
    :param package_objects: The dictionary of packages.
    :param truck: The truck 1 object.
    :param location_id: The current location being explored for loading.
    :param sorted_distances: A sorted list of tuples containing location IDs and their corresponding distances from the
    hub.
    :return: True if the package's destination address is acceptable for loading.
    """
    package = package_objects[package_id]  # Grab the package object.
    sorted_distances_dict = dict(sorted_distances)  # Convert the list of tuples to a dictionary for quick lookup.

    # Get the package's destination address distance from the hub.
    package_distance_from_hub = sorted_distances_dict.get(package.destination_address, float('inf'))
    # Get the current location's distance from the hub.
    location_id_distance_from_hub = sorted_distances_dict.get(location_id, float('inf'))

    return (package.destination_address in truck.destinations or
            package_distance_from_hub <= location_id_distance_from_hub)


# Helper function for truck 1 loading: checking if a package and all of its dependencies should be loaded.
def can_load_entire_group(package, truck, package_objects, location_id, sorted_distances, visited=None):
    """
    Recursively check if the entire group of a package can be loaded onto the truck. The criteria are that all packages
    linked through chains of dependencies are being delivered to locations closer than the current location being
    explored.

    :param package: The package object being considered for loading.
    :param truck: The truck object.
    :param package_objects: Dictionary of all package objects.
    :param location_id: Current location of loading algorithm.
    :param sorted_distances: A sorted dictionary of distances from the hub.
    :param visited: Set of already checked package IDs to avoid infinite recursion.
    :return: True if the entire group can be loaded, False otherwise.
    """
    if visited is None:
        visited = set()  # Initialize a set of locations that have already been checked.

    # Add the current package to the visited set
    visited.add(package.package_id)

    # Check if package itself is in a group that cannot be loaded
    if package.grouping:  # If package is part of a linked group.
        for linked_package_id in package.linked_packages:  # Check for linked package IDs that haven't been checked.
            if linked_package_id not in visited:
                linked_package = package_objects[linked_package_id]  # Grab the linked package object.
                # Check if the package is eligible to be added.
                if not can_load_group_member(linked_package_id, package_objects, truck, location_id, sorted_distances):
                    return False
                    # Recursively check the linked package's group members while passing updated visited set.
                if not can_load_entire_group(linked_package, truck, package_objects, location_id, sorted_distances,
                                             visited):
                    return False

    # Check address group members
    for linked_package_id in package.address_group:
        if linked_package_id not in visited:
            linked_package = package_objects[linked_package_id]
            # Address group members should theoretically be okay, however they can have their own dependencies that
            # need to be checked for thoroughness.
            if not can_load_group_member(linked_package_id, package_objects, truck, location_id, sorted_distances):
                return False
                # Recursively check the address group package's group members
            if not can_load_entire_group(linked_package, truck, package_objects, location_id, sorted_distances,
                                         visited):
                return False

    return True


# Helper function for truck 1 loading.
def check_return_time(truck, weight_matrix):
    """
    Simulates a round trip delivery route and returns the simulated timestamp.

    :param truck: The truck object.
    :param weight_matrix: The weight matrix representing distances.
    :return: Simulated end time with current cargo.
    """
    current_time = test_route_planning(truck, weight_matrix)
    return current_time.time()


def load_the_rest_of_truck_2(truck, package_objects, loading_list):
    """
    Load truck 2 with linked packages if they can fit. Top off prioritizing single time-sensitive packages with no
    associated packages.

    :param truck: Truck 2 object.
    :param package_objects: Dictionary of all package objects.
    :param loading_list: List of package IDs that need to be loaded.
    """
    # Load linked packages. Assuming linked groups are large, this is a greedy algorithm strategy.
    for package_id in loading_list:
        package = package_objects[package_id]
        if package.grouping:  # If packages have linked IDs.
            # Check if there is cargo space.
            if can_load_package_and_group(package, truck):
                # Load all linked packages.
                load_package_and_group(package_id, truck, package_objects, loading_list)

    # Top off cargo with any time-sensitive packages with no associated packages. This gives Truck 3 more flexibility
    # for its time-sensitive deliveries.
    for package_id in loading_list:
        package = package_objects[package_id]
        if package.delivery_deadline != "EOD" and not package.grouping and len(package.address_group) == 1:
            if can_load_package_and_group(package, truck):
                load_package_and_group(package_id, truck, package_objects, loading_list)

    # Top off cargo with any other packages with no associated packages. This attempts to top off Truck 2.
    for package_id in loading_list:
        package = package_objects[package_id]
        if (not package.grouping) and len(package.address_group) == 1:
            if can_load_package_and_group(package, truck):
                load_package_and_group(package_id, truck, package_objects, loading_list)
    # Note: topping off Truck 2 with non-time-sensitive packages has pros and cons. The pros include it giving more
    # flexibility to the loading of Trucks 1 and 3, allowing Truck 1 to have as little as 8 packages. The cons include
    # it potentially causing the average fleet mileage to go up as Truck 3 generally has more non-time-sensitive
    # packages than Truck 2, meaning that Truck 3 is better suited for additional non-time-sensitive packages. Giving
    # Truck 2 additional non-time-sensitive packages could cause its second route of the day more inefficient than just
    # leaving it on Truck 3.


def load_remaining_packages_on_truck_3(truck, package_objects, loading_list):
    """
    Load the remaining packages onto Truck 3, checking for capacity.

    :param truck: Truck 3 object.
    :param package_objects: Dictionary of all package objects.
    :param loading_list: List of package IDs that need to be loaded.
    """
    for package_id in loading_list[:]:  # Iterate over a copy to safely modify the original list
        package = package_objects[package_id]
        if package.delivery_status == 'at the hub':
            # Check if the package and its group can be loaded onto the truck
            if can_load_package_and_group(package, truck):
                load_package_and_group(package_id, truck, package_objects, loading_list)
            else:
                break  # Stop if truck is full or group cannot be loaded
    # Note: a more dynamic solution might have a balancing function apply in the case that truck 3 exceeds capacity.
    # Additionally, logic could be applied that allows for another round of loading packages later in the day to scale
    # for more than 40 packages without requiring additional drivers and/or trucks.
