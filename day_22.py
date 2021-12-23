from typing import List
import re

class Region():
    def __init__(self, is_on: bool, x_min, x_max, y_min, y_max, z_min, z_max) -> None:
        self.is_on = is_on
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
    
    def get_intersection(self, region: "Region", is_on: bool) -> "Region" or None:
        if self.x_max < region.x_min or self.x_min > region.x_max \
            or self.y_max < region.y_min or self.y_min > region.y_max \
            or self.z_max < region.z_min or self.z_min > region.z_max:
                return None
        return Region(
            is_on, \
            x_min=max(self.x_min, region.x_min), \
            x_max=min(self.x_max, region.x_max), \
            y_min=max(self.y_min, region.y_min), \
            y_max=min(self.y_max, region.y_max), \
            z_min=max(self.z_min, region.z_min), \
            z_max=min(self.z_max, region.z_max), \
        )
    
    def fully_contains(self, region: "Region") -> bool:
        # Returns true if self fully contains region
        return self.x_min <= region.x_min \
            and region.x_max <= self.x_max \
            and self.y_min <= region.y_min \
            and region.y_max <= self.y_max \
            and self.z_min <= region.z_min \
            and region.z_max <= self.z_max
    
    def get_atomic_regions_after_carving(self, curve_this_region_out: "Region") -> List["Region"]:
        # 27 potential regions :o (3 x 3 x 3)
        x_ranges = [[curve_this_region_out.x_min, curve_this_region_out.x_max]]
        y_ranges = [[curve_this_region_out.y_min, curve_this_region_out.y_max]]
        z_ranges = [[curve_this_region_out.z_min, curve_this_region_out.z_max]]

        if self.x_min < curve_this_region_out.x_min:
            x_ranges.append([self.x_min, curve_this_region_out.x_min - 1])
        if self.x_max > curve_this_region_out.x_max:
            x_ranges.append([curve_this_region_out.x_max + 1, self.x_max])
        if self.y_min < curve_this_region_out.y_min:
            y_ranges.append([self.y_min, curve_this_region_out.y_min - 1])
        if self.y_max > curve_this_region_out.y_max:
            y_ranges.append([curve_this_region_out.y_max + 1, self.y_max])
        if self.z_min < curve_this_region_out.z_min:
            z_ranges.append([self.z_min, curve_this_region_out.z_min - 1])
        if self.z_max > curve_this_region_out.z_max:
            z_ranges.append([curve_this_region_out.z_max + 1, self.z_max])

        split_regions = []
        for x_range in x_ranges:
            for y_range in y_ranges:
                for z_range in z_ranges:
                    
                    split_regions.append(Region(self.is_on, x_range[0], x_range[1], y_range[0], y_range[1], z_range[0], z_range[1]))

        # We need to delete the carved region
        split_regions.pop(0)
        return split_regions

    def get_volume(self) -> int:
        return (self.x_max - self.x_min + 1) \
            * (self.y_max - self.y_min + 1) \
            * (self.z_max - self.z_min + 1)

def get_reboot_steps(is_part_1: bool) -> List[Region]:
    with open('day_22_input.txt') as f:
        input_lines = f.read().splitlines()
        reboot_steps = []
        for line in input_lines:
            explosive_search = re.search(r'(\w+)\sx=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)', line)
            is_on = explosive_search.group(1) == 'on'
            x_min = int(explosive_search.group(2))
            x_max = int(explosive_search.group(3))
            y_min = int(explosive_search.group(4))
            y_max = int(explosive_search.group(5))
            z_min = int(explosive_search.group(6))
            z_max = int(explosive_search.group(7))

            if is_part_1:
                if -50 <= min(x_min, x_max, y_min, y_max, z_min, z_max) \
                    and max(x_min, x_max, y_min, y_max, z_min, z_max) <= 50:
                        reboot_steps.append(Region(is_on, x_min, x_max, y_min, y_max, z_min, z_max))
            else:
                reboot_steps.append(Region(is_on, x_min, x_max, y_min, y_max, z_min, z_max))

        return reboot_steps

def get_num_on_states(is_part_1: bool):
    reboot_steps = list(get_reboot_steps(is_part_1))
    atomic_regions = []
    i = 0
    for step in reboot_steps:
        i += 1
        next_atomic_regions = atomic_regions.copy()
        ignore_append_step = not step.is_on
        for atomic_region in atomic_regions:
            if step.fully_contains(atomic_region):
                # step will override this guy - we can remove this region
                next_atomic_regions.remove(atomic_region)
                continue
            elif atomic_region.fully_contains(step) and step.is_on == atomic_region.is_on:
                # no reason to add step
                ignore_append_step = True
                break

            intersecting_region = step.get_intersection(atomic_region, step.is_on)
            if intersecting_region == None:
                continue

            # We have a partially intersecting region - let's split atomic_region up into smaller cuboids
            next_atomic_regions.remove(atomic_region)
            new_regions = atomic_region.get_atomic_regions_after_carving(intersecting_region)
            next_atomic_regions.extend(new_regions)
            
        if not ignore_append_step:
            next_atomic_regions.append(step)
        atomic_regions = next_atomic_regions

    on_count = 0
    for atomic_region in atomic_regions:
        if atomic_region.is_on:
            on_count += atomic_region.get_volume()

    return on_count

#~~~~~~~ Part 1 ~~~~~~~#
answer = get_num_on_states(is_part_1=True)
print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_num_on_states(is_part_1=False)
print(f'Part 2 answer: {answer}')
