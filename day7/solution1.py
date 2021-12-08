#! /usr/bin/python3.8
from collections import defaultdict
import csv
import sys


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            input_row = next(csv_reader)

            positions = defaultdict(int)
            total_sum = 0

            for num_str in input_row:
                positions[int(num_str)] += 1
                total_sum += int(num_str)

            min_guess_cost = (-1, sys.maxsize)
            left_count = 0
            mid_count = positions[0]
            right_count = len(input_row) - positions[0]
            left_sum = 0
            right_sum = total_sum

            for guess in range(1, max(positions)):
                left_count += mid_count
                right_sum -= right_count
                mid_count = positions[guess]
                right_count -= mid_count
                left_sum += left_count

                if left_sum + right_sum < min_guess_cost[1]:
                    min_guess_cost = (guess, left_sum + right_sum)
                # Found global min
                else:
                    print(min_guess_cost)
                    return


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
