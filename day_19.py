from typing import List
from enum import Enum
import numpy
from numpy.typing import NDArray
from collections import Counter

SCANNER_PAIRING_THRESHOLD = 12

def get_scanner_sections():
    with open('day_19_input.txt') as f:
        return f.read().split('\n\n')

# Displacement map is a map from tuple of vertex indices to displacement
# E.g. if list of vertices is [[1,2,4], [2,6,9]], then map[(0,1)] = [1,4,5], as vertex[0] and vertex[1] are displaced by that amount
def get_displacement_map(beacon_matrix: NDArray):
    num_vertices = beacon_matrix.shape[1]
    map_of_displacement_from_vertex_at_index_a_to_b = {}
    for i in range(num_vertices-1):
        vertex_a = beacon_matrix[:,i]
        for j in range(i + 1, num_vertices):
            vertex_b = beacon_matrix[:,j]
            map_of_displacement_from_vertex_at_index_a_to_b[(i, j)] = vertex_b - vertex_a
    # NOTE: I will now fill the rest of the map (e.g. where i > j), but this is mostly redundant and doubles memory usage
    for i in range (1, num_vertices):
        for j in range(0, i):
            map_of_displacement_from_vertex_at_index_a_to_b[(i, j)] = -1 * map_of_displacement_from_vertex_at_index_a_to_b[(j, i)]
    return map_of_displacement_from_vertex_at_index_a_to_b

class Scanner():
    def __init__(self, id: int, beacon_matrix: NDArray) -> None:
        self.id = id
        # displacement map finds displacement between all vertices s.t. v_1_index < v_2_index.
        # if v_1_index == v_2_index, then displacement is 0 (same vertex!)
        # if v_1_index > v_2_index, then do -displacement of v_2_index to v_1_index

        self.update_beacon_matrix(beacon_matrix)
        self.matrix_values_relative_to_S_0 = False

    def update_beacon_matrix(self, beacon_matrix: NDArray):
        self.beacon_matrix = beacon_matrix
        self.displacement_map = get_displacement_map(beacon_matrix)
        self.matrix_values_relative_to_S_0 = True

    def set_location(self, location: NDArray):
        self.location = location

    def get_displacement(self, index_of_a: int, index_of_b: int):
        if index_of_a < index_of_b:
            return self.displacement_map[(index_of_a, index_of_b)]
        elif index_of_b < index_of_a:
            return -1 * self.displacement_map[(index_of_b, index_of_a)]
        else:
            return numpy.zeros((3, 1), dtype=int)
    
    def get_vertex_at(self, index: int) -> NDArray:
        return self.beacon_matrix[:,index]

class Face(Enum):
    # Default face is positive x direction
    X_POSITIVE = 0
    X_NEGATIVE = 1
    Y_POSITIVE = 2
    Y_NEGATIVE = 3
    Z_POSITIVE = 4
    Z_NEGATIVE = 5

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class Rotation(Enum):
    # Always anticlockwise
    NONE = 0
    DEG90 = 1
    DEG180 = 2
    DEG270 = 3

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

def get_transformation_matrix(face: Face, rotation: Rotation):
    identity = numpy.identity(3, int)

    if face == Face.X_POSITIVE:
        face_transform = identity
    elif face == Face.X_NEGATIVE:
        face_transform = numpy.matrix(
            [[-1, 0, 0],
             [ 0,-1, 0],
             [ 0, 0, 1]])
    elif face == Face.Y_POSITIVE:
        face_transform = numpy.matrix(
            [[ 0,-1, 0],
             [ 1, 0, 0],
             [ 0, 0, 1]])
    elif face == Face.Y_NEGATIVE:
        face_transform = numpy.matrix(
            [[ 0, 1, 0],
             [-1, 0, 0],
             [ 0, 0, 1]])
    elif face == Face.Z_POSITIVE:
        face_transform = numpy.matrix(
            [[ 0, 0,-1],
             [ 0, 1, 0],
             [ 1, 0, 0]])
    elif face == Face.Z_NEGATIVE:
        face_transform = numpy.matrix(
            [[ 0, 0, 1],
             [ 0, 1, 0],
             [-1, 0, 0]])

    if rotation == Rotation.NONE:
        rotation_transform = identity
    elif rotation == Rotation.DEG90:
        rotation_transform = numpy.matrix(
            [[ 1, 0, 0],
             [ 0, 0,-1],
             [ 0, 1, 0]])
    elif rotation == Rotation.DEG180:
        rotation_transform = numpy.matrix(
            [[ 1, 0, 0],
             [ 0,-1, 0],
             [ 0, 0,-1]])
    elif rotation == Rotation.DEG270:
        rotation_transform = numpy.matrix(
            [[ 1, 0, 0],
             [ 0, 0, 1],
             [ 0,-1, 0]])

    return rotation_transform * face_transform

def get_ops_map_to_matrix():
    # Only need to calculate the 24 matrices once
    output = {}
    for face in Face:
        for rotation in Rotation:
            output[(face, rotation)] = get_transformation_matrix(face, rotation)
    return output

def get_scanners() -> List[Scanner]:
    # Load beacon matrices from file
    scanners = []
    for index, section in enumerate(get_scanner_sections()):
        relative_positions_of_beacons_strs = section.split('\n')[1:]
        relative_positions_of_beacons = []
        for line in relative_positions_of_beacons_strs:
            x, y, z = line.split(',')
            relative_positions_of_beacons.append([int(x), int(y), int(z)])

        rel_pos_matrix = numpy.asmatrix( \
            numpy.array(relative_positions_of_beacons).transpose() \
        )

        scanner = Scanner(index, rel_pos_matrix)
        scanners.append(scanner)
    return scanners

def convert_scanners_to_be_relative_to_this_one( \
    scanner: Scanner, \
    scanners: List[Scanner], \
    ops_map
) -> bool:
    dis_map_1_values = [str(v.tolist()) for k, v in scanner.displacement_map.items()]
    for i in range(len(scanners)):
        if scanner.id == i:
            continue
        second_scanner = scanners[i]
        if second_scanner.matrix_values_relative_to_S_0:
            continue

        # So second_scanner has yet to be paired with another scanner
        for face in Face:
            for rotation in Rotation:
                transform_matrix = ops_map[(face, rotation)]
                transformed_vertices = transform_matrix * second_scanner.beacon_matrix
                displacement_map = get_displacement_map(transformed_vertices)
        
                dis_map_2_values = [str(v.tolist()) for k, v in displacement_map.items()]

                intersection = list((Counter(dis_map_1_values) & Counter(dis_map_2_values)).elements())

                # This section is highly unoptimised :(
                if len(intersection) >= SCANNER_PAIRING_THRESHOLD * (SCANNER_PAIRING_THRESHOLD - 1):
                    # Now convert second_scanner to coords of scanner
                    # We have transformed matrices, just need to find how much we need to translate by
                    # Shouldn't need too many iters:
                    displacement_map_1_strs = {k: str(v.tolist()) for k, v in scanner.displacement_map.items()}
                    displacement_map_2_strs = {k: str(v.tolist()) for k, v in displacement_map.items()}

                    # Below we find the keys which relate to the vertex clusters that match up (note that we count the same vertex twice technically)
                    map_1_keys_in_intersection = [k for k, v in displacement_map_1_strs.items() if v in intersection]
                    map_2_keys_in_intersection = [k for k, v in displacement_map_2_strs.items() if v in intersection]

                    map_1_indices_of_vertices_in_cluster = sorted(list(set([k[0] for k in map_1_keys_in_intersection] + [k[1] for k in map_1_keys_in_intersection])))
                    map_2_indices_of_vertices_in_cluster = sorted(list(set([k[0] for k in map_2_keys_in_intersection] + [k[1] for k in map_2_keys_in_intersection])))

                    # We can now pick up the vertex cluster in both scanner and second_scanner
                    # As these two clusters have a 1 to 1 mapping, and there exists a translation which maps one cluster onto the other:
                    #   Start by grabbing any vertex of scanner's cluster (say, the first one), then the first vertex in second_scanner's cluster.
                    #   Find the difference, then translate all vertices in second_scanner's cluster by same amount to see if it matches up with
                    #   first clutter. Eventually we will find an exact match, at which point we update second_scanner's variables

                    # The following is a list of the vertex strings of the scanner cluster
                    scanner_vertex_cluster_strs = sorted([str(scanner.beacon_matrix[:,index].tolist()) for index in map_1_indices_of_vertices_in_cluster])

                    just_any_singular_vertex_in_scanner_cluster = scanner.beacon_matrix[:,map_1_indices_of_vertices_in_cluster[0]]
                    for key in map_2_indices_of_vertices_in_cluster:
                        translation_vector = just_any_singular_vertex_in_scanner_cluster - transformed_vertices[:,key]
                        translated_vectors = [transformed_vertices[:,index] + translation_vector for index in map_2_indices_of_vertices_in_cluster]
                        second_scanner_vertex_cluster_strs = sorted([str(item.tolist()) for item in translated_vectors])
                        if scanner_vertex_cluster_strs == second_scanner_vertex_cluster_strs:
                            flatten_array = [item for sublist in translation_vector.tolist() for item in sublist]

                            trans_vec = numpy.asmatrix(numpy.array([flatten_array])).transpose()
                            second_scanner.set_location(trans_vec)
                            new_beacon_matrix = transformed_vertices + numpy.tile(trans_vec, (1, transformed_vertices.shape[1]))
                            second_scanner.update_beacon_matrix(new_beacon_matrix)
                            convert_scanners_to_be_relative_to_this_one(second_scanner, scanners, ops_map)


#~~~~~~~ Part 1 ~~~~~~~#
def get_number_of_beacons():
    # Step 0: Get Ops map (face, rotation) -> matrix
    ops_map = get_ops_map_to_matrix()

    # Step 1: Get scanners
    scanners = get_scanners()

    # Step 2: Now starting with S_i = S_0 and S_j = S_1, compare lists of displacements.
    #   If intersection magnitute is equal or larger than 12 * 11, then they share beacons.
    #       When this happens:
    #           - We know the transform to get the points merging from S_j to S_i
    #           - We DON'T know the translation yet. At this point, grab the vertex cluster in S_i that is congruent to a cluster in the newly transformed S_j' . 
    #               Take the highest x, then look for highest y, then highest z in each of the clusters. Those points match up. Work out translation.
    #   If not, adjust orientation of S_j by using the transform matrices, and try again
    #   If no luck, move onto S_2...
    convert_scanners_to_be_relative_to_this_one(scanners[0], scanners, ops_map)

    # Step 3: Put all beacon coords in the beacon list
    beacons = set()
    scanners[0].matrix_values_relative_to_S_0 = True
    for scanner in scanners:
        for i in range(scanner.beacon_matrix.shape[1]):
            beacons.add(str(scanner.beacon_matrix[:,i].tolist()))
    return len(list(beacons))

answer = get_number_of_beacons()
print(f'Part 1 answer: {answer}')


#~~~~~~~ Part 2 ~~~~~~~#
def get_manhatten_dist(vertex_1: NDArray, vertex_2: NDArray):
    return numpy.sum(numpy.absolute(vertex_2 - vertex_1))

def get_max_distance():
    ops_map = get_ops_map_to_matrix()
    scanners = get_scanners()
    scanners[0].set_location(numpy.zeros((3, 1), dtype=int))
    convert_scanners_to_be_relative_to_this_one(scanners[0], scanners, ops_map)

    beacons = []
    scanners[0].matrix_values_relative_to_S_0 = True
    for scanner in scanners:
        for i in range(scanner.beacon_matrix.shape[1]):
            beacons.append(scanner.beacon_matrix[:,i])
    
    scanner_locations = [scanner.location for scanner in scanners]
    max_distance = 0
    for i in range(len(scanner_locations) - 1):
        for j in range(i + 1, len(scanner_locations)):
            if i == j:
                continue
            distance = get_manhatten_dist(scanner_locations[i], scanner_locations[j])
            if distance > max_distance:
                max_distance = distance
    
    return max_distance

answer = get_max_distance()
print(f'Part 2 answer: {answer}')
