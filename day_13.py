#~~~~~~~ Part 1 ~~~~~~~#

from typing import List

with open('day_13_input.txt') as f:
    input_sections = [x for x in f.read().split('\n\n')]

def get_dot_coords(input_section: str) -> List[List[int]]:
    return [[int(coord) for coord in x.split(',')] for x in input_section.split('\n')]

def get_dots_after_fold(along_x: bool, num: int, list_of_dots: List[List[int]]) -> List[List[str]]:
    # 6, True -> fold along x = 6
    # 5, False -> fold along y = 5 etc

    folded_dot_list = list_of_dots.copy()
    for dot in list_of_dots:
        if along_x and dot[0] > num:
            folded_dot_list.remove(dot)
            new_dot = [2*num - dot[0], dot[1]]
            if new_dot not in folded_dot_list:
                folded_dot_list.append(new_dot)
        
        elif not along_x and dot[1] > num:
            folded_dot_list.remove(dot)
            new_dot = [dot[0], 2*num - dot[1]]
            if new_dot not in folded_dot_list:
                folded_dot_list.append(new_dot)
    return folded_dot_list
    
def get_fold_instructions(input_section: str) -> List[str]:
    input_lines = input_section.split('\n')
    lines_to_fold_over = [x.replace('fold along ', '') for x in input_lines]
    return lines_to_fold_over

def get_num_dots_after_first_fold(input_sections: List[str]) -> int:
    dots = get_dot_coords(input_sections[0])
    instructions = get_fold_instructions(input_sections[1])

    instruction = instructions[0]
    split_instruction = instruction.split('=')
    dots = get_dots_after_fold(split_instruction[0] == 'x', int(split_instruction[1]), dots)

    return len(dots)


answer = get_num_dots_after_first_fold(input_sections)

print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#

def print_dots_after_folds(input_sections: List[str]) -> int:
    dots = get_dot_coords(input_sections[0])
    instructions = get_fold_instructions(input_sections[1])

    for instruction in instructions:
        split_instruction = instruction.split('=')
        dots = get_dots_after_fold(split_instruction[0] == 'x', int(split_instruction[1]), dots)

    x_max = max([dot[0] for dot in dots])
    y_max = max([dot[1] for dot in dots])

    for y in range(y_max + 1):
        row_str = ''
        for x in range(x_max + 1):
            if [x, y] in dots:
                row_str += '#'
            else:
                row_str += '.'
        print(row_str)

print('Part 2 answer:')
print_dots_after_folds(input_sections)
