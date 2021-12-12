from typing import List

with open('day_12_input.txt') as f:
    input_lines = [x for x in f.read().splitlines()]

class Graph():
    def __init__(self, vertices: set[str], edges: List[List[str]]):
        self.vertices = vertices
        self.edges = edges

    def get_all_edges_from_vertex(self, vertex: str) -> List[List[str]]:
        edge_list = []
        for edge in self.edges:
            first, second = edge
            if vertex == first or vertex == second:
                edge_list.append(edge)
        return edge_list

class PathCounter():
    def __init__(self):
        self.count = 0
    
    def increment_count(self):
        self.count += 1

def get_graph(input: List[str]) -> Graph:
    vertices = set()
    edges = []
    for input_line in input:
        first, second = input_line.split('-')
        vertices.update({first, second})
        a, b = sorted([first, second])
        edges.append([a, b])
    return Graph(vertices, edges)

def visit_neighbour_vertices(vertex: str, graph: Graph, nodes_visited: List[str], path_counter: PathCounter, free_to_visit_small_cave_twice: bool):
    # Add current vertex to nodes_visited if lowercase
    nodes_visited_copy = nodes_visited.copy()
    if vertex == vertex.lower() and vertex not in nodes_visited:
        nodes_visited_copy.append(vertex)
    
    # Traverse all edges we can go to
    edges_from_vertex = graph.get_all_edges_from_vertex(vertex)
    for edge in edges_from_vertex:
        first, second = edge
        if first == vertex:
            other_vertex = second
        else:
            other_vertex = first
        if other_vertex == 'end':
            path_counter.increment_count()
            continue
        elif other_vertex not in nodes_visited:
            visit_neighbour_vertices(other_vertex, graph, nodes_visited_copy, path_counter, free_to_visit_small_cave_twice)
        # if other_vertex is small, has been traversed, but free_to_visit_small_cave_twice is True - go to it again    
        elif other_vertex == other_vertex.lower() and other_vertex in nodes_visited_copy and free_to_visit_small_cave_twice:
            if other_vertex != 'start':
                visit_neighbour_vertices(other_vertex, graph, nodes_visited_copy, path_counter, False)

def get_number_of_paths(input: List[str], is_part_2: bool):
    graph = get_graph(input)
    path_counter = PathCounter()

    visit_neighbour_vertices('start', graph, nodes_visited=[], path_counter=path_counter, free_to_visit_small_cave_twice=is_part_2)
    return path_counter.count

#~~~~~~~ Part 1 ~~~~~~~#
answer = get_number_of_paths(input_lines, is_part_2=False)

print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_number_of_paths(input_lines, is_part_2=True)

print(f'Part 2 answer: {answer}')
