# Part 1
with open('day_01_input.txt') as f:
    list = [int(x) for x in f.read().splitlines()]

times_increased = 0
for i, depth in enumerate(list):
    if i == 0:
        continue
    if list[i] > list[i-1]:
        times_increased = times_increased + 1

print(f'Part 1: Times increased is {str(times_increased)}')

# Part 2
times_increased = 0
for i, depth in enumerate(list):
    # We want to compare element at i with element at i+3.
    # We can start at i = 0, but we must stop when i+3 == (len(list) - 1)
    if i + 3 >= len(list):
        break
    if list[i] < list[i+3]:
        times_increased = times_increased + 1

print(f'Part 2: Times increased is {str(times_increased)}')
