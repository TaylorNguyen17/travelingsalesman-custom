def floyd_warshall(matrix):
    """
    Runs a modified Floyd-Warshall algorithm on the given matrix.
    Keeps track of the path required if a shorter path than the direct route is found using a next-node matrix.

    :param matrix: A weight matrix representing the graph.
    :return: Tuple of (updated matrix with the shortest path, next_node matrix for path reconstruction
    """
    num_vertices = len(matrix)  # Number of vertices in the graph, used in the for loops
    # Initialize the next_node matrix. Matrix is the same size as the weight matrix.
    # If shortest path from a to b is from a to b, then the matrix says 'None'.
    # Else, the next node is recorded.
    next_node = [[None if i == j else j for j in range(num_vertices)] for i in range(num_vertices)]

    # Floyd-Warshall algorithm: three nested loops to iterate through all combinations of pairs of vertices i and j
    # with each possible intermediate vertex k.
    # Modified to also update the next_node matrix.
    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                # Check if the path from i to j through k is shorter than the path from i to j
                if matrix[i][k] + matrix[k][j] < matrix[i][j]:
                    # Update the distance from i and j to the shorter path distance through k
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
                    # Update the next node in the path from i to j to be the next node in the path from i to k
                    next_node[i][j] = next_node[i][k]
    return matrix, next_node  # Next_node matrix was used for data verification during the implementation process.
    # Next_node matrix was not used for final program. Future program could possibly use path reconstruction to
    # provide real-time location tracking of trucks while in transport.

# Original source code included the creation of a sorted nested dictionary for easy access to the next closest location.
# Code still included in final files for future enhancements.
# def weight_matrix_to_nested_dict(matrix):
#     """
#     Converts the weight matrix into a nested dictionary that can be sorted uniquely per row.
#     Assumes no 'inf' values.
#
#     :param matrix: A weight matrix
#     :return: A nested dictionary representing the shortest paths.
#     """
#     output = {}
#     # "i" represents the row of the matrix and enumerate represents the columns and the column indices
#     for i, row in enumerate(matrix):
#         # For each row, initialize a sub-dictionary that will contain the row index and distance value
#         output[i] = {}
#         # "j" is the index from the enumerated row and represents the destination from the weight matrix.
#         # val is the distance value to that destination
#         for j, val in enumerate(row):
#             # Exclude the distance from a location to itself, so if the indices are the same, no entry is added
#             if i != j:
#                 # "i" is the first key, whose value "j" is the second key, whose value is the distance
#                 output[i][j] = val
#     return output
#
#
# def sort_inner_dictionaries(dictionary):
#     """
#     Sorts the inner dictionaries of the output by ascending values.
#
#     :param dictionary: A nested dictionary.
#     :return: The same dictionary but with sorted inner dictionaries.
#     """
#     # Lambda function grabs the value of the inner dictionary.
#     # Sorted sorts the inner key-value pairs based on the lambda function key, which is set to be the distance value.
#     # Sorted returns a list of tuples, so dict() converts the tuples back into a dictionary structure.
#     # The new dictionary is then stored back into the outer dictionary as the value to the top level key.
#     for key in dictionary:
#         dictionary[key] = dict(sorted(dictionary[key].items(), key=lambda item: item[1]))
#     return dictionary
#
