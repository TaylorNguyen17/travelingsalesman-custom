import csv
import os


# Utility functions to read the distance table and create data structures from it.
# Original distance table has been manually cleaned up and split: A simple list of addresses for index mapping
# and a weight matrix for optimizing.
def read_addresses(file_path):
    """
    Read addresses from a CSV file. Assumes each line in the CSV contains one address.

    :param file_path: Path to the CSV file.
    :return: List of addresses.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")  # Error handling
    addresses = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Assuming the csv contains only one row
            # Cleans the data by removing leading space and truncating the newline and zipcode.
            return [address.split('\n')[0].strip() for address in row]
    return addresses


def create_mappings(addresses):
    """
    Create index-to-address and address-to-index mappings.

    :param addresses: List of addresses.
    :return: Tuple of two dictionaries (id_to_address_dict, address_to_id_dict).
    """
    # Enumerate creates the indices from the csv, dictionaries are created both ways for easy lookup.
    index_to_address = {index: address for index, address in enumerate(addresses)}
    address_to_index = {address: index for index, address in enumerate(addresses)}
    return index_to_address, address_to_index


def read_weight_matrix(file_path):
    """
    Read a weight matrix from a CSV file. Assumes no 'inf' weights.

    :param file_path: Path to the CSV file.
    :return: A 2D list representing the weight matrix.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")  # Error handling
    matrix = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            matrix.append([float(x) for x in row])
    return matrix


# Utility function to read the package file.
# Uses the hashtable module to store the data directly into the custom chaining hashtable.
def read_and_store_package_data(file_path, hash_table):
    """
    Read a package file containing ID, delivery address, city, state, zip code, deadline, weight,
    and special instructions.
    Adds a special column for grouping information.

    :param file_path: Path to the CSV file.
    :param hash_table: Hash table for data to be inserted into.
    :return: None. Hash table will be directly updated with data.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")  # Error handling
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Creates a list for package data
            package_data = [
                row[0],  # id
                row[1],  # address
                row[2],  # city
                row[3],  # state
                row[4],  # zip
                row[5],  # deadline
                row[6],  # weight
                row[7],  # special_instructions
            ]
            hash_table.insert(package_data[0], package_data)
