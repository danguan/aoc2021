#! /usr/bin/python3.8
import csv
from typing import List
from heapq import heappush, heappop
from collections import deque


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def _getBasinSize(self, caves: List[List[int]], row: int, col: int) -> int:
        """Finds the size of the basin at the current row/col of caves.

        Args:
            caves: Matrix representing cave height structure.
            row: Row to start processing from.
            col: Col to start processing from.

        Returns:
            Size of basin joined to starting coordinate.
        """
        q = deque([(row, col)])
        basin_size = 0

        while q:
            r, c = q.popleft()

            for d in self.directions:
                new_r = r + d[0]
                new_c = c + d[1]

                if (
                    len(caves) > new_r >= 0
                    and len(caves[row]) > new_c >= 0
                    and caves[new_r][new_c] > 0
                    and caves[new_r][new_c] != 10
                ):
                    caves[new_r][new_c] *= -1
                    basin_size += 1
                    q.append((new_r, new_c))
        return basin_size

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            caves = []
            basins = []  # Treat as a heap

            for row in csv_reader:
                # Increase heights by 1 to avoid 0s
                curr_row = [int(num) + 1 for num in row[0]]
                caves.append(curr_row)

            for r in range(len(caves)):
                for c in range(len(caves[r])):
                    # Original height was 9 or location is already processed
                    if caves[r][c] == 10 or caves[r][c] < 0:
                        continue

                    heappush(basins, self._getBasinSize(caves, r, c))
                    if len(basins) == 4:
                        heappop(basins)
            print(basins[0] * basins[1] * basins[2])


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
