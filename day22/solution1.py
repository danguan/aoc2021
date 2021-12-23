#! /usr/bin/python3.8
import csv
from typing import List


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _process_step(
        self,
        grid: List[List[List[int]]],
        step: List[int],
        on_lights: int,
        hi_bound: int,
    ) -> int:
        """Turns lights on or off according to step and returns # of lights on.

        Args:
            grid: 3-D grid containing current light statuses (on/off).
            step: List containing in order: [on/off status, low x bound,
                high x bound, low y bound, high y bound, low z bound, high z
                bound].
            on_lights: Initial number of lights on on the grid.
            hi_bound: Higher bound of grid dimensions for all axes. Scaled to
                lo_bound being scaled to 0.

        Returns:
            Number of lights that are on after processing current step.
        """
        on, x_lo, x_hi, y_lo, y_hi, z_lo, z_hi = step

        for x in range(max(x_lo, 0), min(x_hi, hi_bound) + 1):
            for y in range(max(y_lo, 0), min(y_hi, hi_bound) + 1):
                for z in range(max(z_lo, 0), min(z_hi, hi_bound) + 1):
                    if grid[x][y][z] == 0 and on:
                        grid[x][y][z] = on
                        on_lights += 1
                    elif grid[x][y][z] == 1 and not on:
                        grid[x][y][z] = 0
                        on_lights -= 1

        return on_lights

    def solve(self, lo_bound: int, hi_bound: int):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            size = hi_bound - lo_bound
            grid = [
                [[0 for _ in range(size + 1)] for _ in range(size + 1)]
                for _ in range(size + 1)
            ]
            steps = []

            for row in csv_reader:
                on_str, x_str = row[0].split(" ")
                on = 1 if on_str == "on" else 0
                x_bound_str = x_str.split("=")[1].split("..")
                x_lo, x_hi = [int(num) for num in x_bound_str]
                y_bound_str = row[1].split("=")[1].split("..")
                y_lo, y_hi = [int(num) for num in y_bound_str]
                z_bound_str = row[2].split("=")[1].split("..")
                z_lo, z_hi = [int(num) for num in z_bound_str]
                step = [on, x_lo, x_hi, y_lo, y_hi, z_lo, z_hi]

                for val_idx in range(1, len(step)):
                    step[val_idx] -= lo_bound
                steps.append(step)

            on_lights = 0
            # Scaling hi_bound based on lo_bound scaling to 0
            hi_bound -= lo_bound

            for step in steps:
                on_lights = self._process_step(grid, step, on_lights, hi_bound)
            print(steps[0:3])

            print(on_lights)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve(-50, 50)
