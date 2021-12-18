#! /usr/bin/python3.8
import csv
import sys


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _find_highest_y(self, lo_y: int, hi_y: int) -> int:
        """Find highest y position of highest velocity landing in [lo_y, hi_y].

        Given gravity, formula for height at step t is essentially:
            ypos_t = initvelocity_y * t - (t * (t - 1)) / 2

        where t is the number of steps processed.

        Upper range of velocity should be lo_y given that with parabolic shape,
        probe will eventually reach y = 0 with -initvelocity_y velocity, and in
        the following step, will descend below lo_y.

        Args:
            lo_y: Low boundary of target zone's y-coordinates.
            hi_y: High boundary of target zone's y-coordinates.

        Returns:
            Peak y position value at which probe will land within [lo_y, hi_y],
            assuming that y-velocity will decrease by 1 per step.
        """
        total_peak = -sys.maxsize

        def pos_at_t(velocity: int, t: int) -> int:
            return velocity * t - (t * (t - 1)) // 2

        for init_velocity in range(-abs(lo_y), abs(lo_y) + 1):
            curr_peak = -sys.maxsize
            curr_t = 0
            curr_pos = pos_at_t(init_velocity, curr_t)

            while curr_pos >= lo_y:
                curr_peak = max(curr_peak, curr_pos)
                if hi_y >= curr_pos >= lo_y:
                    total_peak = max(total_peak, curr_peak)
                    break
                curr_t += 1
                curr_pos = pos_at_t(init_velocity, curr_t)

        return total_peak

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            x_str, y_str = next(csv_reader)
            x_coord_str = x_str.split("=")[1]
            y_coord_str = y_str.split("=")[1]
            x_coords = [int(num) for num in x_coord_str.split("..")]
            y_coords = [int(num) for num in y_coord_str.split("..")]

            print(self._find_highest_y(y_coords[0], y_coords[1]))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
