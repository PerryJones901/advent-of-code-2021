from typing import List

with open('day_05_input.txt') as f:
    input_lines = [x for x in f.read().splitlines()]

DIMENSION_OF_GRID = 991 # Found by manualling looking at input file

class Line():
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def get_lines(input: List[str], exclude_diagonals: bool) -> List[Line]:
    lines = []
    for input_line in input:
        split_on_arrow = input_line.split(' -> ')
        x1, y1 = [int(a) for a in split_on_arrow[0].split(',')]
        x2, y2 = [int(a) for a in split_on_arrow[1].split(',')]

        if exclude_diagonals:
            if x1 == x2 or y1 == y2:
                lines.append(Line(x1, y1, x2, y2))
        else:
            lines.append(Line(x1, y1, x2, y2))
    return lines

def get_new_grid(dimension: int) -> List[List[int]]:
    # The following line caused me so much pain, due to duplicating the same row reference
    # return [[0] * dimension] * dimension

    # There's likely a nicer way to make a 2d array of zeros
    return [[0 for x in range(dimension)] for y in range(dimension)]

def sign(n: int) -> int:
    return (n > 0) - (n < 0)

def count_number_of_entries_geq_2(grid: List[List[int]]) -> int:
    count = 0
    for row in grid:
        for entry in row:
            if entry >= 2:
                count += 1

    return count

def get_number_of_danger_zones(exclude_diagonals: bool) -> int:
    lines = get_lines(input_lines, exclude_diagonals=exclude_diagonals)
    grid = get_new_grid(DIMENSION_OF_GRID)

    for line in lines:
        delta_x = line.x2 - line.x1
        delta_y = line.y2 - line.y1

        current_x = line.x1
        current_y = line.y1
        x_increment = sign(delta_x)
        y_increment = sign(delta_y)

        while(True):
            grid[current_y][current_x] += 1
            if((current_x == line.x2 and current_y == line.y2)):
                break
            current_x += x_increment
            current_y += y_increment

    # Count number of points where its >= 2
    return count_number_of_entries_geq_2(grid)

#~~~~~~~ Part 1 ~~~~~~~#
answer = get_number_of_danger_zones(exclude_diagonals=True)

print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_number_of_danger_zones(exclude_diagonals=False)

print(f'Part 2 answer: {answer}')
