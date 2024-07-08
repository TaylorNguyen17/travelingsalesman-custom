from package import *


def create_packages_from_hash_table(package_hash_table, address_to_id_dict):
    """
    Parse the hash table and create package objects. Convert delivery addresses to location IDs.

    :param package_hash_table: Package hash table.
    :param address_to_id_dict: Dictionary mapping addresses to location indices.
    :return: A dictionary of package objects.
    """
    package_objects = {}  # Key: package ID, Value: package object.

    # Create package objects.
    for bucket in package_hash_table.table:
        for kv in bucket:
            package_id = kv[0]
            package_data = package_hash_table.search(package_id)
            if package_data is not None:  # Error handling.
                package = Package(package_id, package_data[1], package_data[2], package_data[4], package_data[5],
                                  package_data[6], package_data[7], address_to_id_dict)
                package_objects[package_id] = package

    return package_objects


def group_packages_by_similar_address(package_objects):
    """
    Create a dictionary of all delivery locations and all packages destined for those location.
    Update package attributes to store links bidirectionally for easy access.

    :param package_objects: A dictionary of package objects.
    :return: A dictionary where the key is a location ID and the value is a list of package IDs.
    """
    address_groups = {}  # Key: address ID, Value: all package IDs that will be delivered to that location.
    for package_id, package in package_objects.items():
        if package.destination_address is not None:  # Ignore wrong address packages.
            location_id = package.destination_address
            if location_id not in address_groups:
                address_groups[location_id] = set()  # Initialize location ID if it does not exist.
            address_groups[location_id].add(package_id)  # Add package ID to that location ID.
            for existing_package_id in address_groups[location_id]:  # All package IDs for that location so far.
                package_objects[existing_package_id].add_address_group_package(package_id)  # Update package attributes.
                package.add_address_group_package(existing_package_id)  # Update package attributes for initial package.
    return address_groups


def link_packages_by_special_instructions(package_objects):
    """
    Update package attributes to store special instruction links bidirectionally for easy access.

    :param package_objects: A dictionary of package objects.
    """
    for package_id, package in package_objects.items():
        # Check for special instructions.
        if "Must be delivered with" in package.special_instructions:
            # Extract linked package IDs
            linked_ids = package.special_instructions.split("Must be delivered with")[1].strip().split(", ")

            # Initialize a set for the merged group.
            merged_group = set(linked_ids)
            merged_group.add(package_id)  # The set now includes the original package ID.

            # Include linked IDs from already processed packages.
            for linked_id in linked_ids:
                if linked_id in package_objects and package_objects[linked_id].grouping:  # Pull group members' links.
                    merged_group.update(package_objects[linked_id].linked_packages)  # Merge with the set.

            # Update linked_packages for all packages in the merged group
            for pkg_id in merged_group:
                if pkg_id != package_id:  # The attribute set will not include the package itself.
                    package.add_linked_package(pkg_id)  # Updates package attributes.
                if pkg_id in package_objects:  # Error handling.
                    for other_pkg_id in merged_group:
                        if other_pkg_id != pkg_id:
                            package_objects[pkg_id].add_linked_package(other_pkg_id)  # Make all links bidirectional.
