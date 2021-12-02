#! /usr/bin/python3.6
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            prev = 9999
            increment = 0

            for row in csv_reader:
                if int(row[0]) > prev:
                    increment += 1
                prev = int(row[0])

        print(increment)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
