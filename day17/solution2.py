#! /usr/bin/python3.8
import csv
from collections import defaultdict
from typing import DefaultDict, List, Tuple


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _get_valid_x_velocities(
        self, lo_x: int, hi_x: int, max_y_time: int
    ) -> DefaultDict[int, List[int]]:
        """Finds all valid x-velocities that land in target area [lo_x, hi_x].

        These x-velocities are formed into a list as part of a larger mapping
        of time -> x-velocities that reach target area in time.

        Since input and examples only cover one case (lo_x > 0 and hi_y < 0),
        this heuristic will be used to omit negative velocity calculations.

        Args:
            lo_x: Low boundary of target zone's x-coordinates.
            hi_x: High boundary of target zone's x-coordinates.
            max_y_time: Maximum time at which a y-velocity can land in the
                target area, to identify all valid x, y velocity combinations.

        Returns:
            Mapping of time needed to reach target area, to valid x-velocities
            that reach the target area in that time.
        """
        valid_x_velocities = defaultdict(list)

        for init_velocity in range(1, abs(hi_x) + 1):
            curr_t = 0
            curr_pos = 0
            curr_velocity = init_velocity

            while curr_pos <= hi_x:
                if hi_x >= curr_pos >= lo_x:
                    valid_x_velocities[curr_t].append(init_velocity)
                curr_t += 1
                curr_pos += curr_velocity
                curr_velocity = max(curr_velocity - 1, 0)

                if curr_t > max_y_time:
                    break

        return valid_x_velocities

    def _get_valid_y_velocities(
        self, lo_y: int, hi_y: int
    ) -> Tuple[DefaultDict[int, List[int]], int]:
        """Finds all valid y-velocities that land in target area [lo_y, hi_y].

        These y-velocities are formed into a list as part of a larger mapping
        of time -> y-velocities that reach target area in time.

        Given gravity, formula for height at step t is essentially:
            ypos_t = initvelocity_y * t - (t * (t - 1)) / 2

        where t is the number of steps processed.

        Upper range of y velocity should be lo_y given that with parabolic
        shape, probe will eventually reach y = 0 with -initvelocity_y velocity,
        and in the following step, will descend below lo_y.

        Since input and examples only cover one case (lo_x > 0 and hi_y < 0),
        this heuristic will be used to omit calculations for lo_y > 0.

        Args:
            lo_y: Low boundary of target zone's y-coordinates.
            hi_y: High boundary of target zone's y-coordinates.

        Returns:
            Tuple containing:
                - Mapping of time needed to reach target area, to valid
                y-velocities that reach the target area in that time.
                - Maximum time at which a y velocity can land in target
                area.

        """

        def pos_at_t(velocity: int, t: int) -> int:
            return velocity * t - (t * (t - 1)) // 2

        valid_y_velocities = defaultdict(list)

        for init_velocity in range(-abs(lo_y), abs(lo_y) + 1):
            curr_t = 0
            curr_pos = 0

            while curr_pos >= lo_y:
                if hi_y >= curr_pos >= lo_y:
                    valid_y_velocities[curr_t].append(init_velocity)
                curr_t += 1
                curr_pos = pos_at_t(init_velocity, curr_t)

        return (valid_y_velocities, max(valid_y_velocities.keys()))

    def _get_valid_velocities(
        self, lo_x: int, hi_x: int, lo_y: int, hi_y: int
    ) -> int:
        """Counts valid velocities landing in target area defined by givens.

        Args:
            lo_x: Low boundary of target zone's x-coordinates.
            hi_x: High boundary of target zone's x-coordinates.
            lo_y: Low boundary of target zone's y-coordinates.
            hi_y: High boundary of target zone's y-coordinates.

        Returns:
            Count of all valid unique (x, y) velocities that land in target
            area with x-bounds [lo_x, hi_x] and y-bounds [lo_y, hi_y].
        """
        y_velocities, max_y_time = self._get_valid_y_velocities(lo_y, hi_y)
        x_velocities = self._get_valid_x_velocities(lo_x, hi_x, max_y_time)
        valid_velocities = set()

        for time in x_velocities:
            if time in y_velocities:
                x_vel_list = x_velocities[time]

                for x_vel in x_vel_list:
                    for y_vel in y_velocities[time]:
                        valid_velocities.add((x_vel, y_vel))

        return len(valid_velocities)

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            x_str, y_str = next(csv_reader)
            x_coord_str = x_str.split("=")[1]
            y_coord_str = y_str.split("=")[1]
            x_coords = [int(num) for num in x_coord_str.split("..")]
            y_coords = [int(num) for num in y_coord_str.split("..")]

            print(
                self._get_valid_velocities(
                    x_coords[0], x_coords[1], y_coords[0], y_coords[1]
                )
            )


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
