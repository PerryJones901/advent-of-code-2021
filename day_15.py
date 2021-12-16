# WARNING - Very inefficient. Takes ~ 30 mins on a 100 x 100 grid!

from typing import List

ARBITUARY_MAX = 1000000000000

class Vertex():
    def __init__(self, value, grid_row, grid_col):
        self.value = value
        self.dist = ARBITUARY_MAX
        self.prev = None
        self.pos = [grid_row, grid_col]

def get_index_to_put_in_queue(vertices: List[Vertex], low: int, high: int, dist: int):
    if high == low + 1:
        if dist < vertices[low].dist:
            return low
        else:
            return high

    mid = (high + low) // 2
    if vertices[mid].dist == dist:
        return mid
    elif vertices[mid].dist > dist:
        return get_index_to_put_in_queue(vertices, low, mid, dist)
    else:
        return get_index_to_put_in_queue(vertices, mid, high, dist)
        
class VertexQueue():
    def __init__(self, vertices: List[Vertex]):
        self.vertices = vertices
    
    def update_vertex(self, vertex: Vertex):
        if len(self.vertices) <= 1:
            return
        self.vertices.remove(vertex)
        new_index = get_index_to_put_in_queue(self.vertices, 0, len(self.vertices)-1, vertex.dist)
        self.vertices.insert(new_index, vertex)

    def pop(self) -> Vertex:
        return self.vertices.pop(0)

POSITION_DELTAS = [[-1, 0], [0, 1], [1, 0], [0, -1]]

def get_modified_row_by_step(row: List[int], step: int) -> List[int]:
    return [(((cell - 1 + step) % 9) + 1) for cell in row]

def get_modified_row(row: List[int]) -> List[int]:
    new_row = []
    for step in range(5):
        new_row += get_modified_row_by_step(row, step)
    return new_row

def get_vertex_grid(is_part_1: bool):
    with open('day_15_input.txt') as f:
        if is_part_1:
            value_grid = [[int(cell) for cell in row] for row in f.read().splitlines()]
        else:
            input_grid = [[int(cell) for cell in row] for row in f.read().splitlines()]
            input_grid_rows_extended = [get_modified_row(row) for row in input_grid]
            value_grid = []
            for step in range(5):
                value_grid += [get_modified_row_by_step(row, step) for row in input_grid_rows_extended]

        vertex_grid = []
        for row_ind, row in enumerate(value_grid):
            row = []
            for col_ind, value in enumerate(value_grid[row_ind]):
                row.append(Vertex(value, row_ind, col_ind))
            vertex_grid.append(row)
        return vertex_grid

def is_in_bounds(coords: List[int], row_dim: int, col_dim: int):
    return 0 <= coords[0] < row_dim and 0 <= coords[1] < col_dim

def get_shortest_path_length(grid: List[List[Vertex]]):
    # Using Dijkstra's Algorithm
    source = grid[0][0]
    target = grid[-1][-1]
    row_dim = len(grid)
    col_dim = len(grid[0])

    queue = VertexQueue([vertex for row in grid for vertex in row])
    source.dist = 0

    while len(queue.vertices) > 0:
        u = queue.pop()

        if u == target:
            return u.dist

        for row_delta, col_delta in POSITION_DELTAS:
            search_pos = [u.pos[0] + row_delta, u.pos[1] + col_delta]
            if not is_in_bounds(search_pos, row_dim, col_dim):
                continue
            neighbour = grid[search_pos[0]][search_pos[1]]
            if neighbour not in queue.vertices:
                continue
            alt_dist = u.dist + neighbour.value
            if alt_dist < neighbour.dist:
                neighbour.dist = alt_dist
                neighbour.prev = u
                queue.update_vertex(neighbour)


#~~~~~~~ Part 1 ~~~~~~~#
answer = get_shortest_path_length(get_vertex_grid(is_part_1=True))
print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_shortest_path_length(get_vertex_grid(is_part_1=False))
print(f'Part 2 answer: {answer}')
