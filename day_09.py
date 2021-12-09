from typing import List

with open('day_09_input.txt') as f:
    input_grid = [[int(num) for num in row] for row in f.read().splitlines()]

POSITION_DELTAS = [[-1, 0], [0, 1], [1, 0], [0, -1]]

def is_in_bounds(row: int, col: int, row_dim: int, col_dim: int):
    return 0 <= row < row_dim and 0 <= col < col_dim

def get_risk_level(row: int, col: int, grid: List[List[int]]):
    row_dim = len(grid)
    col_dim = len(grid[0])

    value = grid[row][col]
    for row_delta, col_delta in POSITION_DELTAS:
        if is_in_bounds(row + row_delta, col + col_delta, row_dim, col_dim):
            if value >= grid[row + row_delta][col + col_delta]:
                return 0

    return value + 1

def get_total_risk_level(grid: List[List[int]]):
    total = 0
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            total += get_risk_level(row_index, col_index, grid)
    return total

def is_low_point(row: int, col: int, grid: List[List[int]]):
    row_dim = len(grid)
    col_dim = len(grid[0])

    value_here = grid[row][col]
    for row_delta, col_delta in POSITION_DELTAS:
        if is_in_bounds(row + row_delta, col + col_delta, row_dim, col_dim):
            if value_here >= grid[row + row_delta][col + col_delta]:
                return False

    return True

def add_surrounding_points_to_basin_if_necessary(row: int, col: int, grid: List[List[int]], basin: List[List[int]]):
    row_dim = len(grid)
    col_dim = len(grid[0])

    value_here = grid[row][col]
    for row_delta, col_delta in POSITION_DELTAS:
        if is_in_bounds(row + row_delta, col + col_delta, row_dim, col_dim):
            value_at_search_point = grid[row + row_delta][col + col_delta]
            if value_here < value_at_search_point < 9:
                point = [row + row_delta, col + col_delta]
                if point in basin:
                    continue
                else:
                    basin.append(point)
                    add_surrounding_points_to_basin_if_necessary(row + row_delta, col + col_delta, grid, basin)

def get_basin_size_at_low_point(row: int, col: int, grid: List[List[int]]):
    basin = [[row, col]]

    add_surrounding_points_to_basin_if_necessary(row, col, grid, basin)

    return len(basin)

def get_basin_score(grid: List[List[int]]):
    low_points = []
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if is_low_point(row_index, col_index, grid):
                low_points.append([row_index, col_index])

    # For calculating basin sizes:
    #   1. Go to low point
    #   2. Recursion in each direction:
    #       2.a. If new value is more than previous but less than 9, then it's in the basin too.
    #            Add to basin list. Iterate on that point too.
    #       2.b. If new value doesn't satisfy above, continue.
    basin_sizes = []
    for low_point in low_points:
        basin_sizes.append(get_basin_size_at_low_point(low_point[0], low_point[1], grid))
    
    score = 1
    for i in range(3):
        max_size = max(basin_sizes)
        basin_sizes.remove(max_size)
        score *= max_size

    return score

#~~~~~~~ Part 1 ~~~~~~~#
answer = get_total_risk_level(input_grid)

print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_basin_score(input_grid)

print(f'Part 2 answer: {answer}')
