This project contains a few algorithms that give a solution to a custom traveling salesman problem. The classic traveling salesman problem is an np-complete problem where the task is to find an optimal path through a 2D grid of destination.

This version of this problem in this project is enhanced to mimic a more realistic business problem - optimal package delivery routing.


The custom ruleset are as follows:

•  Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.

•  The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.

•  There are no collisions.

•  Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.

•  Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.

•  The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to a truck at the hub). This time is factored into the calculation of the average speed of the trucks.

•  There is up to one special note associated with a package.

•  The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m.

•  The distances provided in the “WGUPS Distance Table” are equal regardless of the direction traveled.

•  The day ends when all 40 packages have been delivered.


A distance table that contains distances from each of the destinations is provided. This project implements a Floyd-Warshall algorithm to optimize this table by searching for multiple-leg routes that are more efficient than straight shot paths.

A package file is also provided that details different delivery deadlines and complicated dependencies.


The overall project strategy was to group packages together logically for maximum efficiency (each destination is visited by only one truck, package groups are assigned to trucks by time-sensitivity/clustering, etc.)
The selected algorithm is a custom nearest neighbor.

In addition, as this project is designed to show off proficiency in data structures and algorithms, an custom hash table is implemented in order to store and manage data.
