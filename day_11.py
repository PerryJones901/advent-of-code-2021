#~~~~~~~ Part 1 ~~~~~~~#

from typing import List

DIMENSION = 10
POSITION_DELTAS = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]

def get_starting_grid():
    with open('day_11_input.txt') as f:
        return [[int(char) for char in line] for line in f.read().splitlines()]

def is_in_bounds(row: int, col: int):
    return 0 <= row < DIMENSION and 0 <= col < DIMENSION

def flash_at(row: int, col: int, grid: List[List[int]]):
    # Slight hack - we'll assume '10' means 'wants to flash, but hasn't yet'
    # As this octopus is flashing, let's increment to above 10:
    grid[row][col] += 1

    for row_delta, col_delta in POSITION_DELTAS:
        search_row = row + row_delta
        search_col = col + col_delta
        if is_in_bounds(search_row, search_col):
            grid[search_row][search_col] += 1
            # If the search octopus' energy hits 10, great - it's now about to flash
            # If the search octopus' energy hits 11, it means it was on 10 - therefore hasn't flashed.
            if 10 <= grid[search_row][search_col] <= 11:
                flash_at(search_row, search_col, grid)

def start_turn(grid: List[List[int]]):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            grid[row][col] += 1
            if grid[row][col] == 10:
                flash_at(row, col, grid)

def get_flashed_count_and_reset_flashed_cells(grid: List[List[int]]) -> int:
    flash_count = 0
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if grid[row][col] > 9:
                flash_count += 1
                grid[row][col] = 0
    return flash_count

def number_of_flashes_in_n_turns(n: int, grid: List[List[int]]):
    total_flash_count = 0
    for turn_number in range(n):
        start_turn(grid)
        total_flash_count += get_flashed_count_and_reset_flashed_cells(grid)
    return total_flash_count

answer = number_of_flashes_in_n_turns(100, get_starting_grid())

print(f'Part 1 answer: {answer}')


#~~~~~~~ Part 2 ~~~~~~~#

def get_is_fully_flashed_and_reset_flashed_cells(grid: List[List[int]]) -> int:
    flash_count = 0
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if grid[row][col] > 9:
                flash_count += 1
                grid[row][col] = 0

    return flash_count == DIMENSION * DIMENSION

def get_round_when_synced(grid: List[List[int]]):
    turn_number = 0
    while(True):
        turn_number += 1
        start_turn(grid)
        if get_is_fully_flashed_and_reset_flashed_cells(grid):
            break
    return turn_number

answer = get_round_when_synced(get_starting_grid())

print(f'Part 2 answer: {answer}')
