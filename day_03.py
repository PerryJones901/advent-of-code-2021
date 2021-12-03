from typing import List

#~~~~~~~ Part 1 ~~~~~~~#

with open('day_03_input.txt') as f:
    binary_number_list = [x for x in f.read().splitlines()]

# Setup
quantity_of_binary_numbers = len(binary_number_list)
length_of_the_binary_numbers = len(binary_number_list[0])

map_from_index_to_number_of_ones = [0] * length_of_the_binary_numbers

# Iterate over the binary numbers, counting the 1s at each index
for binary_num in binary_number_list:
    for digit_index, digit in enumerate(binary_num):
        if digit == '1':
            map_from_index_to_number_of_ones[digit_index] += 1

# Find Gamma
gamma_rate_in_binary = ''
for index in range(length_of_the_binary_numbers):
    if map_from_index_to_number_of_ones[index] > 0.5 * quantity_of_binary_numbers:
        gamma_rate_in_binary += '1'
    else:
        gamma_rate_in_binary += '0'
gamma_rate_in_decimal = int(gamma_rate_in_binary, 2)

# Calculate Epsilon from Gamma
epsilon_rate_in_binary = ''.join(list(map(lambda digit: str(1 - int(digit)), gamma_rate_in_binary)))
epsilon_rate_in_decimal = int(epsilon_rate_in_binary, 2)

# Finale
print(f'Gamma rate in binary: {gamma_rate_in_binary}')
print(f'Gamma rate in decimal: {gamma_rate_in_decimal}')

print(f'Epsilon rate in binary: {epsilon_rate_in_binary}')
print(f'Epsilon rate in decimal: {epsilon_rate_in_decimal}')

print(f'Product: {gamma_rate_in_decimal * epsilon_rate_in_decimal}')


#~~~~~~~ Part 2 ~~~~~~~#

# Helpful Functions
def is_1_most_popular_at_index(binary_number_list: List[str], index: int) -> bool:
    length_of_list = len(binary_number_list)
    total_ones = 0
    for binary_num in binary_number_list:
        if binary_num[index] == '1':
            total_ones += 1
    return 2*total_ones >= length_of_list

def get_rating(starting_list: List[str], one_is_most_popular_filter: str) -> str:
    rating_candidates = starting_list + []
    
    for index in range(len(starting_list)):
        if is_1_most_popular_at_index(rating_candidates, index):
            # 1 is the most (or equally as) popular at this position
            rating_candidates = list(filter(lambda binary_num: binary_num[index] == one_is_most_popular_filter, rating_candidates))
        else:
            # 1 is the least popular at this position
            rating_candidates = list(filter(lambda binary_num: binary_num[index] != one_is_most_popular_filter, rating_candidates))

        if len(rating_candidates) == 1:
            return rating_candidates[0]

# Find o_2 and co_2 ratings
o_2_rating_binary = get_rating(binary_number_list, one_is_most_popular_filter='1')
co_2_rating_binary = get_rating(binary_number_list, one_is_most_popular_filter='0')

o_2_rating_decimal = int(o_2_rating_binary, 2)
co_2_rating_decimal = int(co_2_rating_binary, 2)

# Finale
print(f'O_2 rate in binary: {o_2_rating_binary}')
print(f'O_2 rate in decimal: {o_2_rating_decimal}')

print(f'CO_2 rate in binary: {co_2_rating_binary}')
print(f'CO_2 rate in decimal: {co_2_rating_decimal}')

print(f'Product: {o_2_rating_decimal * co_2_rating_decimal}')
