from typing import Dict, List

with open('day_08_input.txt') as f:
    input_lines = [x for x in f.read().splitlines()]

MAP_FROM_DIGIT_TO_SEGMENTS_LETTERS = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg',
}

FREQUENCY_OF_SEGMENT_IN_THE_TEN_DIGITS = {
    'a': 8, # a appears 8 times etc
    'b': 6,
    'c': 8,
    'd': 7,
    'e': 4,
    'f': 9,
    'g': 7,
}

SEGMENT_LETTERS = 'abcdefg'

def get_number_of_special_four_digit_output_values(input: List[str]):
    count = 0
    for line in input:
        four_digits_encoded_in_line = line.split(' | ')[1].split(' ')
        for digit_encoded in four_digits_encoded_in_line:
            if len(digit_encoded) <= 4 or len(digit_encoded) == 7:
                count += 1
    
    return count

def get_new_possible_segment_map():
    # Key: Original position
    # Value: Possible new positions (want to make these singular)
    return { char: SEGMENT_LETTERS for char in SEGMENT_LETTERS }

def mark_segment_map(decimal_digit: int, pattern: str, possible_segment_map: Dict[str, str]):
    for segment_letter in MAP_FROM_DIGIT_TO_SEGMENTS_LETTERS[decimal_digit]:
        possible_segment_map[segment_letter] = ''.join([char for char in possible_segment_map[segment_letter] if char in pattern])

def mark_definite_value_in_segment_map(from_value: str, to_value: str, possible_segment_map: Dict[str, str]):
    possible_segment_map[from_value] = to_value
    all_other_letters = SEGMENT_LETTERS.replace(from_value, '')
    for letter in all_other_letters:
        possible_segment_map[letter] = possible_segment_map[letter].replace(to_value, '')

def cross_off_found_values(possible_segment_map: Dict[str, str]):
    for letter in SEGMENT_LETTERS:
        if len(possible_segment_map[letter]) == 1:
            # possible_segment_map[letter] should be crossed off all other letters
            all_other_letters = SEGMENT_LETTERS.replace(letter, '')
            for other_letter in all_other_letters:
                possible_segment_map[other_letter] = possible_segment_map[other_letter].replace(possible_segment_map[letter], '')

def get_reverse_dict(dict: Dict[str, str]):
    return {v: k for k, v in dict.items()}

def get_output_value(input_line: str) -> int:
    split_line = input_line.split(' | ')
    unique_patterns = split_line[0].split(' ')
    four_digits_encoded = split_line[1].split(' ')
    possible_segment_map = get_new_possible_segment_map()

    # First sweep - frequency analysis
    concat_patterns = ''.join(unique_patterns)
    for char in SEGMENT_LETTERS:
        if concat_patterns.count(char) == 4:
            # e maps to this char
            mark_definite_value_in_segment_map('e', char, possible_segment_map)
        elif concat_patterns.count(char) == 6:
            # b maps to this char
            mark_definite_value_in_segment_map('b', char, possible_segment_map)
        elif concat_patterns.count(char) == 9:
            # f maps to this char
            mark_definite_value_in_segment_map('f', char, possible_segment_map)

    # Second sweep - get the unique values
    for pattern in unique_patterns:
        if len(pattern) == 2:
            mark_segment_map(1, pattern, possible_segment_map)
        elif len(pattern) == 3:
            mark_segment_map(7, pattern, possible_segment_map)
        elif len(pattern) == 4:
            mark_segment_map(4, pattern, possible_segment_map)
        elif len(pattern) == 7:
            # this does absolutely nothing, but I have an itch to leave this
            mark_segment_map(8, pattern, possible_segment_map)
        cross_off_found_values(possible_segment_map)

    # Assume it's all good at this point!
    # Now onto the four_digits part:
    decoder_map = get_reverse_dict(possible_segment_map)
    decoded_patterns = [''.join(sorted(''.join([decoder_map[char] for char in digits_encoded]))) for digits_encoded in four_digits_encoded]
    
    pattern_to_decimal_digit_map = get_reverse_dict(MAP_FROM_DIGIT_TO_SEGMENTS_LETTERS)
    decimal_digits = [str(pattern_to_decimal_digit_map[pattern]) for pattern in decoded_patterns]
    output_value = int(''.join(decimal_digits))
    return output_value

def get_sum_of_output_values(input: List[str]) -> int:
    total = 0
    for line in input:
        total += get_output_value(line)
    return total

#~~~~~~~ Part 1 ~~~~~~~#
answer = get_number_of_special_four_digit_output_values(input_lines)

print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_sum_of_output_values(input_lines)

print(f'Part 2 answer: {answer}')
