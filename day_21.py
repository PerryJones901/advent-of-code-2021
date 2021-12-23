#~~~~~~~ Part 1 ~~~~~~~#
from typing import Dict

def get_starting_positions():
    with open('day_21_input.txt') as f:
        return [int(line.split(' starting position: ')[1]) for line in f.read().splitlines()]

class Dice():
    def __init__(self) -> None:
        self.value = 100
        self.num_rolls = 0

    def roll_dice(self) -> int:
        self.num_rolls += 1
        self.value = (self.value % 100) + 1
        return self.value

def get_next_roll(last_roll):
    return (last_roll % 100) + 1

def get_part_1_answer():
    player_1_pos, player_2_pos = get_starting_positions()
    player_1_score, player_2_score = 0, 0

    dice = Dice()
    while (player_1_score < 1000 and player_2_score < 1000):
        player_1_turn_roll = 0
        for i in range(3):
            player_1_turn_roll += dice.roll_dice()
        
        player_1_pos = ((player_1_pos + player_1_turn_roll - 1) % 10) + 1
        player_1_score += player_1_pos

        if player_1_score >= 1000:
            break

        player_2_turn_roll = 0
        for i in range(3):
            player_2_turn_roll += dice.roll_dice()
        
        player_2_pos = ((player_2_pos + player_2_turn_roll - 1) % 10) + 1
        player_2_score += player_2_pos
        
        if player_2_score >= 1000:
            break
    
    return min([player_1_score, player_2_score]) * dice.num_rolls

answer = get_part_1_answer()
print(f'Part 1 answer: {answer}')


#~~~~~~~ Part 2 ~~~~~~~#
WIN_SCORE = 21

def get_dice_rolls_total_to_num_universes() -> Dict[int, int]:
    map = {}
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                sum = i + j + k
                map.setdefault(sum, 0)
                map[sum] += 1
    return map

def get_num_wins_for_each_player( \
    p1_pos: int, \
    p1_score: int, \
    p2_pos: int, \
    p2_score: int, \
    just_rolled: int, \
    is_p1_turn: bool, \
    dice_roll_to_num_universes: Dict[int, int] \
):
    p1_wins = 0
    p2_wins = 0

    if is_p1_turn:
        p1_pos = ((p1_pos + just_rolled - 1) % 10) + 1
        p1_score += p1_pos
        if p1_score >= WIN_SCORE:
            return [1, 0]

    else:
        p2_pos = ((p2_pos + just_rolled - 1) % 10) + 1
        p2_score += p2_pos
        if p2_score >= WIN_SCORE:
            return [0, 1]
    
    for roll_total in dice_roll_to_num_universes.keys():
        p1_wins_from_now, p2_wins_from_now = get_num_wins_for_each_player( \
            p1_pos, \
            p1_score, \
            p2_pos, \
            p2_score, \
            roll_total, \
            (not is_p1_turn), \
            dice_roll_to_num_universes \
        )

        p1_wins += (p1_wins_from_now * dice_roll_to_num_universes[roll_total])
        p2_wins += (p2_wins_from_now * dice_roll_to_num_universes[roll_total])

    return [p1_wins, p2_wins]

def get_part_2_answer():
    p1_pos, p2_pos = get_starting_positions()
    dice_rolls_total_to_num_universes = get_dice_rolls_total_to_num_universes()

    p1_wins = 0
    p2_wins = 0
    for roll_total in dice_rolls_total_to_num_universes:
        p1_wins_from_now, p2_wins_from_now = get_num_wins_for_each_player(p1_pos, 0, p2_pos, 0, roll_total, True, dice_rolls_total_to_num_universes)
        p1_wins += (p1_wins_from_now * dice_rolls_total_to_num_universes[roll_total])
        p2_wins += (p2_wins_from_now * dice_rolls_total_to_num_universes[roll_total])
    
    return max([p1_wins, p2_wins])

answer = get_part_2_answer()
print(f'Part 2 answer: {answer}')
