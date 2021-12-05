#! /usr/bin/python3.8
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            grid = [[0 for _ in range(1000)] for _ in range(1000)]
            overlap = 0

            for row in csv_reader:
                x1 = row[0]
                y1, x2 = row[1].split(" -> ")
                y2 = row[2]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                if x1 != x2 and y1 != y2:
                    continue
                elif x1 == x2:
                    lower = min(y1, y2)
                    higher = max(y1, y2)
                    for y in range(lower, higher + 1):
                        grid[y][x1] += 1
                elif y1 == y2:
                    lower = min(x1, x2)
                    higher = max(x1, x2)
                    for x in range(lower, higher + 1):
                        grid[y1][x] += 1

            for r in range(len(grid)):
                for c in range(len(grid[r])):
                    if grid[r][c] >= 2:
                        overlap += 1

            print(overlap)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
