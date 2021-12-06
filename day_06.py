from typing import List

with open('day_06_input.txt') as f:
    input_numbers = [int(x) for x in f.read().splitlines()[0].split(',')]

BIRTH_NUMBER = 8
GIVEN_BIRTH_NUMBER = 6

def get_day_0_state_map() -> List[int]:
    map_from_state_to_number_of_fish = [0 for x in range(BIRTH_NUMBER + 1)] # states 0, 1, 2, ... 8
    for fish_number in input_numbers:
        map_from_state_to_number_of_fish[fish_number] += 1
    return map_from_state_to_number_of_fish

def get_next_day_state_map(current_state: List[int]):
    next_day_state_map = [0 for x in range(BIRTH_NUMBER + 1)] # states 0, 1, 2, ... 8

    for current_state_value, number_of_fish in enumerate(current_state):
        if current_state_value == 0:
            next_day_state_map[BIRTH_NUMBER] += number_of_fish
            next_day_state_map[GIVEN_BIRTH_NUMBER] += number_of_fish
        else:
            next_day_state_map[current_state_value - 1] += number_of_fish

    return next_day_state_map

def state_on_day_n(n: int):
    current_state = get_day_0_state_map()
    day_number = 0
    while(day_number < n):
        day_number += 1
        current_state = get_next_day_state_map(current_state)

    return current_state

#~~~~~~~ Part 1 ~~~~~~~#
answer = sum(state_on_day_n(80))

print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = sum(state_on_day_n(256))

print(f'Part 2 answer: {answer}')
