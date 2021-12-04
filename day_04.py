from typing import List

with open('day_04_input.txt') as f:
    input_blocks = [x for x in f.read().split('\n\n')]

class BingoCell():
    def __init__(self, number: str):
        self.number = number
        self.marked = False

class BingoBoard():
    def __init__(self, id: int, grid: List[List[BingoCell]]):
        self.id = id
        self.grid = grid

    def check_num(self, number_called: str):
        for row in self.grid:
            for cell in row:
                if cell.number == number_called:
                    cell.marked = True

    def has_won(self) -> bool:
        # rows
        for row_index in range(5):
            has_won = True
            for column_index in range(5):
                if self.grid[row_index][column_index].marked is False:
                    has_won = False
            if has_won:
                return True

        # columns
        for column_index in range(5):
            has_won = True
            for row_index in range(5):
                if self.grid[row_index][column_index].marked is False:
                    has_won = False
            if has_won:
                return True

        return False
    
    def sum_of_unmarked(self) -> int:
        sum = 0
        for row in self.grid:
            for cell in row:
                if cell.marked == False:
                    sum += int(cell.number)
        return sum

def get_bingo_calls(input_blocks: List[str]) -> List[str]:
    return input_blocks[0].split(',')

def get_bingo_boards(input_blocks: List[str]) -> List[BingoBoard]:
    return [get_bingo_board(index, input_block) for index, input_block in enumerate(input_blocks)]

def get_bingo_board(id: int, input_block: str) -> BingoBoard:
    grid_split_on_spaces = [row.split(' ') for row in input_block.split('\n')]
    grid = [[x for x in row if x != ''] for row in grid_split_on_spaces]
    return BingoBoard(id, [[BingoCell(x) for x in row] for row in grid])

bingo_calls = get_bingo_calls(input_blocks)
bingo_boards = get_bingo_boards(input_blocks[1:])

#~~~~~~~ Part 1 ~~~~~~~#

for bingo_call in bingo_calls:
    winner_decided = False
    for board in bingo_boards:
        board.check_num(bingo_call)
        if board.has_won():
            winner_decided = True
            answer = board.sum_of_unmarked() * int(bingo_call)
            break
    if(winner_decided):
        break

print(f'Part 1 Answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#

list_of_boards_yet_to_win = [x for x in range(len(bingo_boards))]

for bingo_call in bingo_calls:
    for board in bingo_boards:
        if board.id not in list_of_boards_yet_to_win:
            continue

        board.check_num(bingo_call)
        if board.has_won():
            list_of_boards_yet_to_win.remove(board.id)
            if len(list_of_boards_yet_to_win) == 0:
                # At the last board!
                answer = board.sum_of_unmarked() * int(bingo_call)
                break

    if(len(list_of_boards_yet_to_win) == 0):
        break

print(f'Part 2 Answer: {answer}')
