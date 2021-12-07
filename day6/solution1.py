#! /usr/bin/python3.8
import csv
from collections import defaultdict


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self, days: int):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            input_row = next(csv_reader)

            counts = defaultdict(int)

            for num_str in input_row:
                counts[int(num_str)] += 1

            for _ in range(days):
                days_below_count = counts[8]

                for days_left in range(8, 0, -1):
                    temp = counts[days_left - 1]
                    counts[days_left - 1] = days_below_count
                    days_below_count = temp

                # Process rollover from 0 to 6, 8
                counts[6] += days_below_count
                counts[8] = days_below_count

            print(sum([counts[num] for num in range(9)]))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve(80)
