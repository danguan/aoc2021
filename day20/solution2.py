#! /usr/bin/python3.8
import csv
from typing import List


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _pad_grid(self, grid: List[List[str]], padding: int, row_size: int):
        """Pads input grid with dark pixel rows based on `padding`.

        Args:
            grid: 2-D array of light pixels ("#") and dark pixels (".").
            padding: Number of rows of dark pixels to add to the grid.
            row_size: Size of a typical non-padded row.
        """
        for _ in range(padding):
            grid.append(["." for _ in range(row_size + ((padding) * 2))])

    def _get_default_val(self, ie_algo: str) -> int:
        """Yields default value for "out of bounds" grid elements.

        Based on the notion that the first iteration will always have all
        darkened pixels in infinite region, but afterwards will all turn to
        ie_algo[0] and then ie_algo[0] or ie_algo[-1] based on the value from
        previous iteration.

        Args:
            ie_algo: Image enhancement algorithm, i.e. a string of indices
                determining the light/dark status of pixels with binary number
                representations resulting in those indices.

        Returns:
            Current value of "out of bounds" or pixels in the infinite space.
        """
        iteration = 1
        current_ie_algo_index = 0
        if iteration == 1:
            iteration += 1
            yield 0

        while True:
            if ie_algo[current_ie_algo_index] == "#":
                current_ie_algo_index = -1
                yield 1
            else:
                current_ie_algo_index = 0
                yield 0

    def _get_dec(
        self,
        grid: List[List[str]],
        r: int,
        c: int,
        default_val: int,
    ) -> int:
        """Gets decimal value of 9 pixels centered at (r, c) on grid.

        Args:
            grid: 2-D array of light pixels ("#") and dark pixels (".").
            r: Row of center pixel on grid.
            c: Column of center pixel on grid.
            default_val: Default value to use for out of bounds region of grid.

        Returns:
            Decimal form of binary number obtained by taking 9 pixels centered
            on grid[r][c] and flattening the 3 rows into one string.
        """
        decimal_val = 0

        for row in range(r - 1, r + 2):
            for col in range(c - 1, c + 2):
                decimal_val <<= 1
                if len(grid) > row >= 0 and len(grid[0]) > col >= 0:
                    decimal_val += 1 if grid[row][col] == "#" else 0
                else:
                    decimal_val += default_val

        return decimal_val

    def _enhance(
        self, grid: List[List[str]], ie_algo: str, default_val: int
    ) -> List[List[str]]:
        """Enhance original grid image using image enhancement algo once.

        Args:
            grid: 2-D array of light pixels ("#") and dark pixels (".").
            ie_algo: Image enhancement algorithm, i.e. a string of indices
                determining the light/dark status of pixels with binary number
                representations resulting in those indices.
            default_val: Default value to use for out of bounds region of grid.

        Returns:
            New instance of grid, which has been enhanced once using the input
            image enhancement algorithm.
        """
        new_grid = [
            ["." for _ in range(len(grid[0]))] for _ in range(len(grid))
        ]

        for r in range(len(grid)):
            for c in range(len(grid[0])):
                dec_val = self._get_dec(grid, r, c, default_val)
                new_grid[r][c] = ie_algo[dec_val]

        return new_grid

    def _count_lit(self, grid: List[List[str]]) -> int:
        """Counts number of lit pixels are present on grid.

        Args:
            grid: 2-D array of light pixels ("#") and dark pixels (".").

        Returns:
            Number of "#" characters seen in grid.
        """
        count = 0

        for r in range(len(grid)):
            for c in range(len(grid[0])):
                count += 1 if grid[r][c] == "#" else 0

        return count

    def solve(self, iterations: int):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            ie_algo = next(csv_reader)[0]
            grid = []

            next(csv_reader)  # Skip empty row
            row = next(csv_reader)  # First non-empty row
            row_size = len(row[0])

            self._pad_grid(grid, iterations, row_size)

            grid.append(
                ["." for _ in range(iterations)]
                + list(row[0])
                + ["." for _ in range(iterations)]
            )

            for row in csv_reader:
                grid.append(
                    ["." for _ in range(iterations)]
                    + list(row[0])
                    + ["." for _ in range(iterations)]
                )

            self._pad_grid(grid, iterations, row_size)
            default_val = self._get_default_val(ie_algo)

            for _ in range(1, iterations + 1):
                grid = self._enhance(grid, ie_algo, next(default_val))

            print(self._count_lit(grid))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve(50)
