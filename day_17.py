from math import ceil, floor, sqrt

class Region():
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def in_region(self, x, y):
        return self.x_min <= x <= self.x_max \
            and self.y_min <= y <= self.y_max

def get_input_region() -> Region:
    with open('day_17_input.txt') as f:
        input_line = f.read()
        string = input_line.replace('target area: ', '')
        x_part, y_part = string.split(', ')

        x_nums = x_part.split('=')[1]
        x_min, x_max = x_nums.split('..')

        y_nums = y_part.split('=')[1]
        y_min, y_max = y_nums.split('..')

        return Region(int(x_min), int(x_max), int(y_min), int(y_max))

def get_nth_tri_num(n: int) -> int:
    return (n * (n + 1)) // 2

def get_num_trajectories_which_reach_region() -> int:
    # The following map gives us a list of initial velocity_x values that end up in bounds for a given time t
    # We are going to ignore times t where the projectile ends up travelling vertically (i.e. velocity in x direction = 0)
    #   We will deal with that case after
    
    map_from_t_to_v_initial_x = {}
    map_from_t_to_v_initial_y = {}

    region = get_input_region()
    vel_x_min = ceil((-1.0 + sqrt(1 + 4*2*region.x_min)) / 2.0)
    vel_x_max = region.x_max
    vel_y_min = region.y_min
    vel_y_max = -region.y_min
    min_n_where_tri_n_is_in_bounds = None
    max_n_where_tri_n_is_in_bounds = None

    # For x
    for init_vel_x in range(vel_x_min, vel_x_max + 1):
        # Assume all region squares in positive x
        vel_x = init_vel_x
        x_displacement = 0
        time = 0
        while (vel_x != 0):
            time += 1
            x_displacement += vel_x
            if (x_displacement > region.x_max):
                break
            if region.x_min <= x_displacement:
                map_from_t_to_v_initial_x.setdefault(time, [])
                map_from_t_to_v_initial_x[time].append(init_vel_x)
            vel_x -= 1
    
    # For y
    for init_vel_y in range(vel_y_min, vel_y_max + 1):
        # Assume all region squares in negative y
        if init_vel_y > 0:
            # skip to part where we are at y = 0
            time = 2*init_vel_y + 1
            vel_y = -init_vel_y - 1
        else:
            time = 0
            vel_y = init_vel_y
        y_displacement = 0
        while (True):
            time += 1
            y_displacement += vel_y
            if (y_displacement < region.y_min):
                break
            if y_displacement <= region.y_max:
                map_from_t_to_v_initial_y.setdefault(time, [])
                map_from_t_to_v_initial_y[time].append(init_vel_y)
            vel_y -= 1
    
    # Now, find all time values t where there exists at least one velocity which gets in bounds at that time
    t_keys = list(set([k for k, v in map_from_t_to_v_initial_x.items()]) & set([k for k, v in map_from_t_to_v_initial_y.items()]))
    good_traj_vel_x_to_vel_y = {}
    for t in t_keys:
        # We can pair any x velocity at time t with any other y velocity at time t that makes the projectile in bounds
        # We'll call any pair which end up in bounds a 'good trajectory'
        for init_x_vel in map_from_t_to_v_initial_x[t]:
            good_traj_vel_x_to_vel_y.setdefault(init_x_vel, set())
            good_traj_vel_x_to_vel_y[init_x_vel].update(map_from_t_to_v_initial_y[t])
    
    # If x region contains a triangle number, then the smallest such triangle number will be vel_x_min'th triangle number
    min_pos_tri_num = get_nth_tri_num(vel_x_min)
    num = floor((-1.0 + sqrt(1 + 4*2*region.x_max)) / 2.0) # solving x = n(n+1)/2 for n
    max_pos_tri_num = get_nth_tri_num(num)
    if region.x_min <= min_pos_tri_num <= max_pos_tri_num <= region.x_max:
        min_n_where_tri_n_is_in_bounds = vel_x_min
        max_n_where_tri_n_is_in_bounds = num

    # For an nth triangle number that sits within the x bounds, find all values of init_vel_y which end up within bounds any time
    #   after the projectile starts moving vertically
    if min_n_where_tri_n_is_in_bounds != None and max_n_where_tri_n_is_in_bounds != None:
        for n in range(min_n_where_tri_n_is_in_bounds, max_n_where_tri_n_is_in_bounds + 1):
            # At time t > n, x vel is 0, so we are travelling straight up/down.
            y_vels = [y_init_vel for time, init_y_vels in map_from_t_to_v_initial_y.items() for y_init_vel in init_y_vels if time > n]
            good_traj_vel_x_to_vel_y.setdefault(n, set())
            good_traj_vel_x_to_vel_y[n].update(y_vels)
    
    total = 0
    for y_init_vel in [v for k, v in good_traj_vel_x_to_vel_y.items()]:
        total += len(y_init_vel)
    return total

#~~~~~~~ Part 1 ~~~~~~~#
answer = get_nth_tri_num((-get_input_region().y_min) - 1)
print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_num_trajectories_which_reach_region()
print(f'Part 2 answer: {answer}')
