import re

def get_snailfish_nums():
    with open('day_18_input.txt') as f:
        return f.read().splitlines()

def get_reduced(snailfish_num: str) -> str:
    changed_last_iteration = True
    while(changed_last_iteration):
        changed_last_iteration = False
        nest_level = 0
        start_ind_of_last_valid_num = -1
        currently_on_num = False
  
        for index, char in enumerate(snailfish_num):
            if char.isnumeric():
                if not currently_on_num:
                    start_ind_of_last_valid_num = index
                    currently_on_num = True
            else:
                currently_on_num = False

            if char == ']':
                nest_level -= 1
            elif char == '[':
                nest_level += 1
                if nest_level >= 5:
                    # We have an EXPLOSION

                    # Find first string of form [<left_num>,<right_num>]
                    explosive_search = re.search(r'\[(\d+),(\d+)\]', snailfish_num[index:])
                    left_num = int(explosive_search.group(1))
                    right_num = int(explosive_search.group(2))
                    explosive_pair_span = explosive_search.span()                    

                    # Right merge first
                    start_index_of_explosive = index + explosive_pair_span[0]
                    end_index_of_explosive = index + explosive_pair_span[1]
                    right_num_to_change_search = re.search(r'\d+', snailfish_num[end_index_of_explosive:])
                    if right_num_to_change_search != None:
                        right_num_to_change = int(right_num_to_change_search.group(0))
                        right_num_to_change_start_index = end_index_of_explosive + right_num_to_change_search.span()[0]
                        right_num_to_change_end_index = end_index_of_explosive + right_num_to_change_search.span()[1]

                        right_num_replacement = right_num_to_change + right_num
                        snailfish_num = snailfish_num[:right_num_to_change_start_index] \
                            + str(right_num_replacement) \
                            + snailfish_num[right_num_to_change_end_index:]

                    # Replace exploded pair with 0
                    snailfish_num = f'{snailfish_num[:start_index_of_explosive]}0{snailfish_num[end_index_of_explosive:]}'

                    # Now left merge
                    left_num_to_change_search = re.search(r'\d+', snailfish_num[start_ind_of_last_valid_num:])
                    if left_num_to_change_search != None:
                        left_num_to_change_start_index = start_ind_of_last_valid_num + left_num_to_change_search.span()[0]
                        left_num_to_change_end_index = start_ind_of_last_valid_num + left_num_to_change_search.span()[1]

                        left_num_replacement = int(left_num_to_change_search.group(0)) + left_num
                        snailfish_num = snailfish_num[:left_num_to_change_start_index] \
                            + str(left_num_replacement) \
                            + snailfish_num[left_num_to_change_end_index:]
                    
                    changed_last_iteration = True
                    break

        if changed_last_iteration:
            continue

        large_number_search = re.search(r'\d{2,}', snailfish_num)
        if large_number_search != None:
            # We have a SPLIT
            big_num_start_index, big_num_end_index = large_number_search.span()
            match = large_number_search.group(0)

            current_num = int(match)
            left_num = current_num // 2
            right_num = current_num - left_num

            snailfish_num = snailfish_num[:big_num_start_index] \
                + f'[{left_num},{right_num}]' \
                + snailfish_num[big_num_end_index:]

            changed_last_iteration = True

    return snailfish_num

def get_magnitude_of_snailfish_num(snailfish_num: str):
    changed_last_iteration = True
    while(changed_last_iteration):
        changed_last_iteration = False
        explosive_search = re.search(r'\[(\d+),(\d+)\]', snailfish_num)
        if explosive_search != None:
            match = explosive_search.group(0)
            left_num = int(explosive_search.group(1))
            right_num = int(explosive_search.group(2))

            magnitude = 3*left_num + 2*right_num
            snailfish_num = snailfish_num.replace(match, str(magnitude), 1)
            changed_last_iteration = True
    return int(snailfish_num)

def get_part_1_answer():
    snailfish_nums_to_sum = get_snailfish_nums()
    num = snailfish_nums_to_sum[0]

    for snailfish_num in snailfish_nums_to_sum[1:]:
        num = get_reduced(f'[{num},{snailfish_num}]')
    return get_magnitude_of_snailfish_num(num)

def get_part_2_answer():
    snailfish_nums_to_sum = get_snailfish_nums()

    max_mag = 0
    for first_ind, first_snailfish_num in enumerate(snailfish_nums_to_sum):
        for second_ind, second_snailfish_num in enumerate(snailfish_nums_to_sum):
            if first_ind == second_ind:
                continue
            num = get_reduced(f'[{first_snailfish_num},{second_snailfish_num}]')
            magnitude = get_magnitude_of_snailfish_num(num)
            if magnitude > max_mag:
                max_mag = magnitude
    return max_mag

#~~~~~~~ Part 1 ~~~~~~~#
answer = answer = get_part_1_answer()
print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_part_2_answer()
print(f'Part 2 answer: {answer}')
