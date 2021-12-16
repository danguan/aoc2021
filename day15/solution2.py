#! /usr/bin/python3.8
import csv
import sys
from heapq import heappush, heappop
from typing import Dict, List, Tuple


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.directions = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def _reconstruct(
        self,
        grid: List[List[int]],
        came_from: Dict[Tuple[int, int], Tuple[int, int]],
        start_coords: Tuple[int, int],
    ) -> int:
        """Returns sum of path value starting from start_coords.

        Args:
            grid: Grid of weights for traveling to each square.
            came_from: Mapping of coord to coord that it came from with
                lowest overall weight.
            start_coords: (row, col) tuple to start reconstruction from.

        Returns:
            Sum of value of path from start_coords until path ends.
        """
        path_value = 0

        while start_coords in came_from:
            path_value += grid[start_coords[0]][start_coords[1]]
            start_coords = came_from[start_coords]
        return path_value

    def _a_star(self, grid: List[List[int]]) -> int:
        """Performs A* algorithm on grid to get from top left to bot right.

        Args:
            grid: Grid of weights for traveling to each square.

        Returns:
            Minimum weight to get from top left to bottom right.
        """
        R = len(grid)
        C = len(grid[0])

        def manhattan(
            coords_1: Tuple[int, int], coords_2: Tuple[int, int]
        ) -> int:
            return abs(coords_2[0] - coords_1[0]) + abs(
                coords_2[1] - coords_1[1]
            )

        discovered = []
        heappush(discovered, (manhattan((0, 0), (R - 1, C - 1)), (0, 0)))
        came_from = {}
        g_score = {}
        f_score = {}
        for r in range(R):
            for c in range(C):
                g_score[(r, c)] = sys.maxsize
                f_score[(r, c)] = sys.maxsize
        g_score[(0, 0)] = 0
        f_score[(0, 0)] = manhattan((0, 0), (R - 1, C - 1))

        while discovered:
            _, (curr_r, curr_c) = heappop(discovered)
            if (curr_r, curr_c) == (R - 1, C - 1):
                return self._reconstruct(grid, came_from, (curr_r, curr_c))

            for r_add, c_add in self.directions:
                new_r = curr_r + r_add
                new_c = curr_c + c_add

                if R > new_r >= 0 and C > new_c >= 0:
                    tentative_g_score = (
                        g_score[(curr_r, curr_c)] + grid[new_r][new_c]
                    )
                    if tentative_g_score < g_score[(new_r, new_c)]:
                        came_from[(new_r, new_c)] = (curr_r, curr_c)
                        g_score[(new_r, new_c)] = tentative_g_score
                        f_score[(new_r, new_c)] = tentative_g_score + manhattan(
                            (new_r, new_c), (R - 1, C - 1)
                        )
                        heappush(
                            discovered,
                            (f_score[(new_r, new_c)], (new_r, new_c)),
                        )
        return -1

    def solve(self, times_larger: int):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            grid = []
            orig_grid = []

            for row in csv_reader:
                orig_grid.append([int(num) for num in row[0]])

            for added_row in range(times_larger):
                for row in orig_grid:
                    grid_row = []

                    for added_col in range(times_larger):
                        for num in row:
                            total = int(num) + added_row + added_col

                            while total > 9:
                                total -= 9
                            else:
                                grid_row.append(total)

                    grid.append(grid_row)
            assert len(grid) == 500
            assert len(grid[0]) == 500

            print(self._a_star(grid))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve(5)
