from typing import List

EPSILON = 0.01 # Useful for floating point errors

with open('day_07_input.txt') as f:
    input_numbers = [int(x) for x in f.read().splitlines()[0].split(',')]

def median(input: List[int]) -> int:
    sorted_list = sorted(input)
    median_index = len(sorted_list) / 2.0
    if abs(median_index - int(median_index)) < EPSILON:
        return sorted_list[int(median_index)]
    else:
        return sorted_list[int(median_index)] + sorted_list[int(median_index)] // 2

def mean(input: List[int]) -> float:
    return sum(input) / len(input)

def total_fuel_needed_for_position(input: List[int], target_position: int, part1: bool) -> int:
    fuel_spent = 0
    for crab_position in input:
        distance = abs(target_position - crab_position)
        if part1:
            fuel_for_crab = distance
        else:
            fuel_for_crab = (distance * (distance + 1)) // 2
        fuel_spent += fuel_for_crab
    return fuel_spent

# TFW you cannot find a good function name
def get_least_fuel_by_changing_index_by_one_each_time_from_starting_index(input: List[int], starting_index: int, increasing: bool):
    if increasing:
        increment = 1
    else:
        increment = -1
    
    current_index = starting_index
    least_fuel = total_fuel_needed_for_position(input, current_index, part1=False)

    while(True):
        current_index += increment
        fuel = total_fuel_needed_for_position(input, current_index, part1=False)
        if (fuel < least_fuel):
            least_fuel = fuel
        else:
            break
    return least_fuel

def least_fuel_needed(input: List[int], part1: bool) -> int:
    if part1:
        return total_fuel_needed_for_position(input, median(input), part1=True)

    # Some kind of binary search will be nicer - but gonna roll with brute force from mean
    average = mean(input)
    
    average_rounded_up = int(average) + 1
    average_rounded_down = int(average)

    fuel_at_average_rounded_up = total_fuel_needed_for_position(input, average_rounded_up, part1=False)
    fuel_at_average_rounded_down = total_fuel_needed_for_position(input, average_rounded_down, part1=False)

    if (fuel_at_average_rounded_down < fuel_at_average_rounded_up):
        return get_least_fuel_by_changing_index_by_one_each_time_from_starting_index(input, average_rounded_down, increasing=False)
    else:
        return get_least_fuel_by_changing_index_by_one_each_time_from_starting_index(input, average_rounded_up, increasing=True)

#~~~~~~~ Part 1 ~~~~~~~#
answer = least_fuel_needed(input_numbers, part1=True)

print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = least_fuel_needed(input_numbers, part1=False)

print(f'Part 2 answer: {answer}')
