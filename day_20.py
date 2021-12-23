from typing import List, Tuple

def get_input_sections():
    with open('day_20_input.txt') as f:
        return f.read().split('\n\n')

def get_nine_pixel_str_at(row: int, col: int, image: List[str], void_pixel: str) -> str:
    height = len(image)
    width = len(image[0])
    deltas = [-1,0,1]
    output = ''

    for row_diff in deltas:
        row_str = ''

        for col_diff in deltas:
            search_row = row + row_diff
            search_col = col + col_diff

            if search_row < 0 or search_row >= height:
                row_str += void_pixel
            elif search_col < 0 or search_col >= width:
                row_str += void_pixel
            else:
                row_str += image[search_row][search_col]

        output += row_str
    return output

def get_pixel(nine_pixel_str: str, algorithm_str: str) -> str:
    bin_str = nine_pixel_str.replace('.','0').replace('#','1')
    number = int(bin_str, 2)
    return algorithm_str[number]

def extend_image_boundary(image: List[str], void_pixel: str) -> List[str]:
    width_of_original = len(image[0])
    dot_border = (void_pixel * (width_of_original + 2))
    new_image = [dot_border]
    for line in image:
        new_image.append(f'{void_pixel}{line}{void_pixel}')
    new_image.append(dot_border)
    return new_image

def get_next_image(image: List[str], algorithm_str: str, current_void_pixel: str) -> Tuple[List[str], str]:
    extended_image = extend_image_boundary(image, current_void_pixel)
    void_pixel = current_void_pixel
    new_image = []

    height = len(extended_image)
    width = len(extended_image[0])
    for row in range(height):
        row_str = ''
        for col in range(width):
            pixel_str = get_nine_pixel_str_at(row, col, extended_image, void_pixel)
            row_str += get_pixel(pixel_str, algorithm_str)
        new_image.append(row_str)

    new_void_pixel = get_pixel((void_pixel * 9), algorithm_str)
    return (new_image, new_void_pixel)

def get_lit_pixel_count(image, current_void_pixel) -> int:
    if current_void_pixel == '#':
        raise Exception('Infinitely many #')
    count = 0
    for row in image:
        count += row.count('#')
    return count

def get_num_of_lit_pixels_on_n_iterations(n: int) -> int:
    sections = get_input_sections()
    algorithm_str = sections[0]
    image = sections[1].split('\n')
    void_pixel = '.'
    for i in range(n):
        image, void_pixel = get_next_image(image, algorithm_str, current_void_pixel=void_pixel)

    return get_lit_pixel_count(image, void_pixel)


#~~~~~~~ Part 1 ~~~~~~~#
answer = get_num_of_lit_pixels_on_n_iterations(2)
print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_num_of_lit_pixels_on_n_iterations(50)
print(f'Part 2 answer: {answer}')
