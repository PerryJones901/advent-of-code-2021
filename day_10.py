from typing import List

with open('day_10_input.txt') as f:
    input_lines = [x for x in f.read().splitlines()]

OPEN_BRACKETS = '([{<'
CLOSED_BRACKETS = ')]}>'
OPEN_TO_CLOSED_MAP = {
    '(': ')', 
    '[': ']', 
    '{': '}',
    '<': '>',
}
CLOSED_TO_OPEN_MAP = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}
CLOSED_TO_SCORE_MAP_PART_1 = {
    '': 0,
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
CLOSED_TO_SCORE_MAP_PART_2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

# returns '' if there is no invalid closing bracket
def get_first_invalid_closing_bracket(input: str) -> str:
    bracket_stack = []
    for char in input:
        if char in OPEN_BRACKETS:
            bracket_stack.append(char)
        elif char in CLOSED_BRACKETS:
            if len(bracket_stack) == 0:
                return char
            elif bracket_stack[-1] == CLOSED_TO_OPEN_MAP[char]:
                bracket_stack.pop()
            else:
                return char
    return ''

def get_part_1_answer(input: List[str]) -> int:
    invalid_closing_brackets = {
        '': 0, # the case of no invalid closing bracket (ignored in points calculation)
        ')': 0,
        ']': 0,
        '}': 0,
        '>': 0
    }
    for input_line in input:
        closed_bracket = get_first_invalid_closing_bracket(input_line)
        invalid_closing_brackets[closed_bracket] += 1
    score = 0
    for k, v in invalid_closing_brackets.items():
        score += CLOSED_TO_SCORE_MAP_PART_1[k] * v

    return score

# returns 0 if corrupted
def get_part_2_score(input: str) -> str:
    bracket_stack = []
    for char in input:
        if char in OPEN_BRACKETS:
            bracket_stack.append(char)
        elif char in CLOSED_BRACKETS:
            if len(bracket_stack) == 0:
                return 0
            elif bracket_stack[-1] == CLOSED_TO_OPEN_MAP[char]:
                bracket_stack.pop()
            else:
                return 0

    closed_brackets_needed = [OPEN_TO_CLOSED_MAP[char] for char in bracket_stack[::-1]]
    score = 0
    for char in closed_brackets_needed:
        score = (score * 5) + CLOSED_TO_SCORE_MAP_PART_2[char]
    return score

def get_part_2_answer(input: List[str]) -> int:
    scores = []
    for input_line in input:
        score = get_part_2_score(input_line)
        if score == 0:
            continue
        scores.append(score)
    sorted_scores = sorted(scores)
    return sorted_scores[len(sorted_scores) // 2]

#~~~~~~~ Part 1 ~~~~~~~#
answer = get_part_1_answer(input_lines)

print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_part_2_answer(input_lines)

print(f'Part 2 answer: {answer}')
