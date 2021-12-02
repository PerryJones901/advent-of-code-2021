# Part 1
with open('day_02_input.txt') as f:
    command_list = [x for x in f.read().splitlines()]

h_distance = 0
depth = 0

for command in command_list:
    action, units = command.split(' ')
    units_int = int(units)

    if action == 'forward':
        h_distance += units_int
    elif action == 'down':
        depth += units_int
    elif action == 'up':
        depth -= units_int

print('Part 1:')
print(f'Horizontal distance: {h_distance}')
print(f'Depth: {depth}')

print(f'Product: {h_distance * depth}')

# Part 2
h_distance = 0
depth = 0
aim = 0

for command in command_list:
    action, units = command.split(' ')
    units_int = int(units)

    if action == 'forward':
        h_distance += units_int
        depth += aim * units_int
    elif action == 'down':
        aim += units_int
    elif action == 'up':
        aim -= units_int

print('Part 2:')
print(f'Horizontal distance: {h_distance}')
print(f'Depth: {depth}')

print(f'Product: {h_distance * depth}')
