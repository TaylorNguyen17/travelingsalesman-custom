import datetime


class Package:
    def __init__(self, package_id, address, city, zip_code, deadline, weight, special_instructions, address_to_index):
        self.package_id = package_id
        self.destination_address = None if special_instructions == "Wrong address listed" else address_to_index.get(
            address, None)  # Remove wrong addresses (package #9) so loading and routing logic is unaffected.
        self.delivery_city = city
        self.delivery_zip = zip_code
        self.delivery_deadline = deadline
        self.package_weight = weight
        self.special_instructions = special_instructions
        # All packages loaded at the start of the day.
        self.load_time = datetime.datetime(2023, 1, 1, 8, 0)
        self.truck = None  # The truck ID this package will be loaded onto.
        self.delivery_time = None  # Timestamp at time of delivery.
        self.delivered_to = None  # Location ID at time of delivery for verification purposes.
        self.delivery_status = 'at the hub'  # Default status
        self.grouping = False  # Default value for whether this package is linked to others via special instruction.
        self.linked_packages = set()  # Set of all packages linked to this package via special instruction.
        self.address_group = set()  # Set of all packages linked to this package via similar address.

    def add_linked_package(self, package_id):
        """
        Add a linked package ID to this package's linked_packages set.
        The set is designed to be bidirectional with other group members, but NOT self-inclusive.

        :param package_id: Package ID of other package.
        """
        self.linked_packages.add(package_id)
        self.grouping = True  # Grouping value will determine if load/delivery logic requires checking groups

    def add_address_group_package(self, package_id):
        """
        Add a package ID to this package's address_group set.
        The set represents all package IDs that have the same delivery address as this package.
        The set is bidirectional with other group members and IS self-inclusive.

        :param package_id: Package ID of other package.
        """
        self.address_group.add(package_id)

    def update_address(self, new_delivery_address, new_city, new_zip):
        """
        Special method to update delivery address attributes.

        :param new_delivery_address: New delivery address.
        :param new_city: New city.
        :param new_zip: New zip code.
        """
        self.destination_address = new_delivery_address
        self.delivery_city = new_city
        self.delivery_zip = new_zip

    def print_package_details(self):
        # For debugging purposes.
        print(f"Package ID: {self.package_id}")
        print(f"Destination Address: {self.destination_address}")
        print(f"Delivery Deadline: {self.delivery_deadline}")
        print(f"Delivery Time: {self.delivery_time}")
        print(f"Special Instructions: {self.special_instructions}")
        print(f"Delivery Status: {self.delivery_status}")
        print(f"Grouping: {self.grouping}")
        print(f"Linked Packages: {self.linked_packages}")
        print(f"Address Group: {self.address_group}")


def look_up(package_id, package_objects):
    """
    Returns important package information in the form of a dictionary.

    :param package_id: Package ID.
    :param package_objects: List of package objects.
    :return:
    """
    package = package_objects.get(package_id, None)
    if package:
        return {
            'ID': package.package_id,
            'Address': package.destination_address,
            'City': package.delivery_city,
            'Zip': package.delivery_zip,
            'Deadline': package.delivery_deadline,
            'Weight': package.package_weight,
            'Status': package.delivery_status,
        }
    return None
