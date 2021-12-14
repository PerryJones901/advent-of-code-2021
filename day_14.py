#~~~~~~~ Part 1 ~~~~~~~#
from typing import Dict, List

with open('day_14_input.txt') as f:
    input_sections = [x for x in f.read().split('\n\n')]

def get_insertion_rule_map(input_section: str) -> Dict[str, str]:
    insertion_rule_map = {}
    input_lines = input_section.split('\n')
    for input_line in input_lines:
        pair, result = input_line.split(' -> ')
        insertion_rule_map[pair] = result
    return insertion_rule_map

def get_next_frequency_maps(single_freq_map: Dict[str, int], pair_freq_map: Dict[str, int], insertion_map: Dict[str, str]):
    new_single_freq_map = single_freq_map.copy()

    new_pair_freq_map = pair_freq_map.copy()
    possible_pairs = [k for k, v in pair_freq_map.items()]

    for pair in possible_pairs:
        # If we have AB -> C, then:
        # 1. Increment C in the new_single_freq_map by how many times we saw AB
        # 2. Increment AC and CB in the new_pair_freq_map by how many times we saw AB
        # 3. Decrement AB in the new_pair_freq_map by how many times we saw AB (took me WAY too long to realise we needed to do this)

        freq_of_pair = pair_freq_map[pair]
        insertion_char = insertion_map[pair]

        new_single_freq_map.setdefault(insertion_char, 0)
        new_single_freq_map[insertion_char] += freq_of_pair

        new_first_pair = pair[0] + insertion_char
        new_pair_freq_map.setdefault(new_first_pair, 0)
        new_pair_freq_map[new_first_pair] += freq_of_pair

        new_second_pair = insertion_char + pair[1]
        new_pair_freq_map.setdefault(new_second_pair, 0)
        new_pair_freq_map[new_second_pair] += freq_of_pair

        new_pair_freq_map[pair] -= freq_of_pair
    return new_single_freq_map, new_pair_freq_map

def get_max_minus_min_after_n_turns(sections: List[str], n: int) -> int:
    polymer = sections[0]
    insertion_rule_map = get_insertion_rule_map(sections[1])

    single_freq_map = {}
    for char in polymer:
        single_freq_map.setdefault(char, 0)
        single_freq_map[char] += 1
    
    pair_freq_map = {}
    for index in range(len(polymer) - 1):
        pair = polymer[index]+polymer[index+1]
        pair_freq_map.setdefault(pair, 0)
        pair_freq_map[pair] += 1
    
    for turn in range(n):
        single_freq_map, pair_freq_map = \
            get_next_frequency_maps(single_freq_map, pair_freq_map, insertion_rule_map)

    frequencies = [v for k, v in single_freq_map.items()]
    min_freq = min(frequencies)
    max_freq = max(frequencies)
    return max_freq - min_freq

answer = get_max_minus_min_after_n_turns(input_sections, 10)
print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_max_minus_min_after_n_turns(input_sections, 40)
print(f'Part 2 answer: {answer}')
