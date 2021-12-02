#! /usr/bin/python3.6
import csv
import sys
from collections import deque


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self, window_size: int):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            d = deque()
            d_sum = 0
            prev_sum = sys.maxsize
            increment = 0

            for row in csv_reader:
                val = int(row[0])
                if len(d) == window_size:
                    prev_sum = d_sum
                    d_sum -= d.popleft()

                d.append(val)
                d_sum += val

                if d_sum > prev_sum:
                    increment += 1

        print(increment)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve(3)
