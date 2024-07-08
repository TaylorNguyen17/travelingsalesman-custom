# My name is Taylor Nguyen and welcome to my C950 project!
# Student ID: 010507238, email: tngu670@wgu.edu

from package_creator import *
from utils import *
from floydwarshall import *
from hashtable import *
from truck import *
from loading import *
from routing import *
from interface import *

# Create a dictionary to convert delivery addresses to simple location IDs so that algorithms are simpler.
# Create dictionary to convert indices back to delivery addresses for UI calls.
addresses_file_path = 'WGUPS Locations Index.csv'  # File path for simple list of delivery addresses.
addresses = read_addresses(addresses_file_path)  # Reads CSV.
id_to_address_dict, address_to_id_dict = create_mappings(addresses)  # Creates two dictionaries for quick conversion.

# Optimize weight matrix via Floyd Warshall algo.
adjacency_file_path = 'WGUPS Adjacency Matrix.csv'  # File path for cleaned up weight matrix.
weight_matrix = read_weight_matrix(adjacency_file_path)  # Read CSV.
# Creates two matrices, one for distance and one for path reconstruction (for verification purposes)
shortest_paths, next_nodes = floyd_warshall(weight_matrix)

package_file_path = 'WGUPS Package File.csv'  # File path for cleaned up package data.
package_hash_table = HashTable()  # Initialize custom chaining hash table.
read_and_store_package_data(package_file_path, package_hash_table)  # Populates hash table from CSV.

# Process hash table data to create package objects and create package links.
# Create a dictionary of package objects from hash table.
package_objects = create_packages_from_hash_table(package_hash_table, address_to_id_dict)
# Create a dictionary of locations and packages that deliver to them.
# Also update package attributes to link by similar delivery address.
address_groups = group_packages_by_similar_address(package_objects)
# Update package attributes to link by special instructions.
link_packages_by_special_instructions(package_objects)

start_time = datetime.datetime(2023, 1, 1, 8, 0)  # Initialize start time to 8:00 AM.
truck1 = Truck(1, start_time=start_time)  # Early morning, short-route, round trip.
truck2 = Truck(2, start_time=start_time, is_time_sensitive=True)  # Early morning, long-route, double route.
truck3 = Truck(3, is_time_sensitive=True)  # Delayed start, long-route, double route.
# Note: Double route refers to the truck distinguishing between high and low priority delivery locations.
# First route focuses on time-sensitive packages. Second route delivers the rest.

trucks = {  # Create a dictionary of trucks.
    1: truck1,
    2: truck2,
    3: truck3
}

loading_list = []  # Copy the package_objects dictionary keys, use to track the loading of packages.
for package in package_objects:
    loading_list.append(package)

# Load packages that MUST be on trucks 2 or 3.
load_high_priority_packages(trucks, package_objects, loading_list)

# Iteratively load packages onto truck 1, test the route, and add more until the round trip is past 9:05 AM.
# A minimum load of 8 packages does not allow wiggle room in Trucks 2 and 3. A minimum load of 9 is selected.
# Increasing the minimum load allows for more wiggle room but pushes back the start time for Truck 3, which is
# a time-sensitive truck.
iteratively_load_truck_1(truck1, shortest_paths, package_objects, loading_list, address_groups, 9)

# Deliver the packages on truck 1.
truck1.start_route(shortest_paths)
# Return Truck 1 to the hub.
truck1.return_to_hub(0, shortest_paths)
# Simulate transferring driver to Truck 3 by setting Truck 3's start time to Truck 1's return time.
truck3.start_time = truck1.current_time

# Load Truck 2 to full or near full capacity.
load_the_rest_of_truck_2(truck2, package_objects, loading_list)

# Truck 2's first round of deliveries, targeting only locations with time-sensitive packages for rapid delivery.
truck2.start_route(shortest_paths)

# Truck 2's second round of deliveries for the rest of its cargo.
nearest_neighbor_routing(truck2, shortest_paths)

# Load Truck 3 with all other packages not yet loaded.
load_remaining_packages_on_truck_3(truck3, package_objects, loading_list)

# Truck 3's first round of deliveries, targeting only locations with time-sensitive packages for rapid delivery.
truck3.start_route(shortest_paths)

# Simulate the passage of time in case wrong address packages have not yet been corrected at 10:20 AM.
if truck3.current_time < datetime.datetime(2023, 1, 1, 10, 20):
    truck3.current_time = datetime.datetime(2023, 1, 1, 10, 20)

# Manually handle the wrong address for package #9. Since there is no CSV file containing this information, it cannot
# be automated.
package_9 = package_objects['9']  # Identify package object with ID number 9.
package_9.update_address(19, "Salt Lake City", 84111)  # Update package #9's address.
truck3.destinations.add(package_9.destination_address)  # Update Truck 3's destinations.

# Truck 3's second round of deliveries for the rest of its cargo, including corrected addresses.
nearest_neighbor_routing(truck3, shortest_paths)

# Initiate UI
user_interface(package_objects, trucks, id_to_address_dict, package_hash_table)

# Secret developer code below to check correct and successful deliveries. Default on for project submission.
print_all_packages_eod(package_objects)
